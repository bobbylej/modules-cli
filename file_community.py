import json
import math
from networkx.algorithms import community
from community import community_louvain
from community_metrics import count_outer_exports
from graph import (
    create_louvain_graph,
    create_greedy_graph,
)


def move_files_with_excessive_exports(communities, file_dependencies):
    """
    Moves files with excessive exports to the 'Shared' community.

    Parameters:
        communities (Dict[str, Set[str]]): A dictionary mapping communities ids to sets of filenames.
        file_dependencies (Dict[str, Set[str]]): A dictionary mapping filenames to sets of dependent filenames.

    Returns:
        (Dict[str, Set[str]]): The updated dictionary of communities after moving files with excessive exports to the 'Shared' community.
    """

    # Count outer exports for each file in the communities
    outer_exports = count_outer_exports(communities, file_dependencies)

    # Move files with more than 3 outer exports to the 'Shared' community
    shared_community = []
    files_to_remove = []
    for community in communities.values():
        for file in community:
            if outer_exports[file] >= 3:
                shared_community.append(file)
                files_to_remove.append(file)

    # Remove files with excessive exports from their respective communities
    for file in files_to_remove:
        for community_id in communities.keys():
            if file in communities[community_id]:
                communities[community_id] = list(communities[community_id])
                communities[community_id].remove(file)
                communities[community_id] = frozenset(communities[community_id])

    # Add the 'Shared' community and files with excessive exports to it
    if shared_community:
        communities['Shared'] =(frozenset(shared_community))

    return communities


def convert_partition_to_communities(partition):
    """
    Convert a list of partitions into a dictionary of communities.

    Args:
        partition (partition:dictionary): A list of tuples representing the file and its corresponding community ID.

    Returns:
        (Dict[str, Set[str]]): A dictionary mapping communities ids to sets of filenames.
    """
    communities = {}
    for file, community_id in partition.items():
        if (isinstance(file, str)):
            if communities.get(community_id) is not None:
                communities[community_id].append(file)
            else:
                communities[community_id] = [file]
    return communities

def convert_list_to_communities(list):
    """
    Converts a list to a dictionary of communities.

    Args:
        list (list): The list to be converted.

    Returns:
        dict: A dictionary representing the communities, where the keys are the indices of the list elements and the values are the corresponding list elements.
    """
    communities = {}
    for i in range(len(list)):
        communities[i] = list[i]
    return communities


def detect_communities_for_files_by_greedy_modularity(file_dependencies):
    """
    Detect communities for files by using a greedy modularity algorithm.

    Args:
        file_dependencies (Dict[str, Set[str]]): A dictionary mapping filenames to sets of dependent filenames.

    Returns:
        (Dict[str, Set[str]]): A dictionary mapping communities ids to sets of filenames.
    """
    graph = create_greedy_graph(file_dependencies)

    amount_of_files = len(file_dependencies)
    min_communities = math.ceil(amount_of_files / 30)

    partition = community.greedy_modularity_communities(
        graph, None, 1.5, min_communities
    )

    communities = convert_list_to_communities(partition)

    communities = move_files_with_excessive_exports(communities, file_dependencies)

    return communities


def detect_communities_for_files_by_louvain(file_dependencies):
    """
    Detects communities for files using the Louvain algorithm.

    Args:
        file_dependencies (Dict[str, Set[str]]): A dictionary mapping filenames to sets of dependent filenames.

    Returns:
        (Dict[str, Set[str]]): A dictionary mapping communities ids to sets of filenames.
    """
    graph = create_louvain_graph(file_dependencies)

    # Apply the Louvain algorithm to the graph and obtain the partition
    partition = community_louvain.best_partition(graph, None, "weight", 1.5)

    communities = convert_partition_to_communities(partition)

    communities = move_files_with_excessive_exports(communities, file_dependencies)

    return communities

def save_communities_in_file(communities, filename):
    """
    Write the content of the community to a file in JSON format.

    Args:
        communities (list): A list of communities.
        filename (str): The name of the file to write the content to.

    Returns:
        None
    """
    content = {}
    for community_id, file_community in communities.items():
        content[community_id] = list(file_community)

    with open(filename, "w") as json_file:
        json.dump(content, json_file, indent=2)