import networkx as nx
import matplotlib.cm as cm
import matplotlib.pyplot as plt


def create_louvain_graph(file_dependencies):
    """
    Create a Louvain graph.

    Args:
        file_dependencies (Dict[str, Set[str]]): A dictionary mapping filenames to sets of dependent filenames.

    Returns:
        nx.Graph: A Louvain graph with the source files as nodes and the target files as edges.
    """
    graph = nx.karate_club_graph()
    for source_file, target_files in file_dependencies.items():
        for target_file in target_files:
            graph.add_edge(source_file, target_file)
    return graph


def create_greedy_graph(file_dependencies):
    """
    Create a graph representing the file dependencies.

    Parameters:
        file_dependencies (Dict[str, Set[str]]): A dictionary mapping filenames to sets of dependent filenames.

    Returns:
        graph (nx.Graph): The created graph representing the file dependencies.
    """
    graph = nx.Graph()
    for source_file, target_files in file_dependencies.items():
        for target_file in target_files:
            graph.add_edge(source_file, target_file)
    return graph


def draw_louvain_graph(graph, partition):
    """
    Draw a Louvain graph.

    Args:
        graph (networkx.Graph): The graph to be drawn.
        partition (dict): The partition of the nodes in the graph.

    Returns:
        None
    """
    pos = nx.spring_layout(graph)
    cmap = cm.get_cmap("viridis", max(partition.values()) + 1)
    nx.draw_networkx_nodes(
        graph,
        pos,
        partition.keys(),
        node_size=40,
        cmap=cmap,
        node_color=list(partition.values()),
    )
    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    plt.show()


def draw_greedy_graph(
    graph,
    communities
):
    """
    Draw a graph using a greedy algorithm.

    Parameters:
        graph (NetworkX Graph): The graph to be drawn.
        communities (list): A list of communities, where each community is a list of nodes.

    Return:
        None
    """
    pos = nx.spring_layout(graph)
    cmap = cm.get_cmap("viridis", len(communities))
    node_colors = [
        cmap(community_id)
        for community_id, community in enumerate(communities)
        for node in community
    ]
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=40)
    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    plt.show()
