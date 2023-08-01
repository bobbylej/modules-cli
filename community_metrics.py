import os


def count_outer_exports(communities, file_dependencies):
    """
    Count the number of outer exports for each file in the given communities and file dependencies.

    Parameters:
        communities (Dict[str, Set[str]]): A dictionary mapping communities ids to sets of filenames.
        file_dependencies (Dict[str, Set[str]]): A dictionary mapping filenames to sets of dependent filenames.

    Returns:
        outer_exports (dict): A dictionary containing the count of outer exports for each target file.
    """

    outer_exports = {}
    communities_files = {}

    # for community_id, community in enumerate(communities):
    for community_id, community in communities.items():
        for file in community:
            outer_exports[file] = 0
            communities_files[file] = community_id

    for source_file, target_files in file_dependencies.items():
        source_file_community_id = communities_files.get(source_file)
        if source_file_community_id is not None:
            for target_file in target_files:
                target_file_community_id = communities_files.get(target_file)
                if source_file_community_id != target_file_community_id:
                    outer_exports[target_file] += 1

    return outer_exports


def calculate_community_metrics(communities, file_dependencies):
    """
    Calculates community metrics based on the given communities and file dependencies.

    Args:
        communities (Dict[str, Set[str]]): A dictionary mapping communities ids to sets of filenames.
        file_dependencies (Dict[str, Set[str]]): A dictionary mapping filenames to sets of dependent filenames.

    Returns:
        dict: A dictionary containing community metrics, including the number of files, outer connections, outer imports, outer exports, max outer imports in one file, max outer exports in one file, files with outer imports, and files with outer exports. The metrics are organized by community ID, with an additional "Summary" entry for overall metrics.
    """

    # Initialize the result dictionary
    community_metrics = {}

    # Initialize summary metrics
    total_outer_connections = 0
    total_outer_imports = 0
    total_outer_exports = 0

    communities_files = {}
    outer_imports = {}
    outer_exports = {}
    files_with_outer_imports = {}
    files_with_outer_exports = {}
    max_outer_imports_one_file = {}
    max_outer_exports_one_file = {}

    files_outer_exports = count_outer_exports(communities, file_dependencies)

    for community_id, community in communities.items():
        outer_exports[community_id] = 0
        outer_imports[community_id] = 0
        files_with_outer_imports[community_id] = []
        files_with_outer_exports[community_id] = []
        max_outer_imports_one_file[community_id] = 0
        max_outer_exports_one_file[community_id] = 0

        for file in community:
            communities_files[file] = community_id

    for community_id, community in communities.items():
        # Iterate over the files in the community
        for file in community:
            # Check the dependencies of the file
            dependencies = file_dependencies.get(file, [])
            # Initialize value for outer imports in single file
            outer_imports_in_file = 0
            # Count the number of outer imports and exports
            for dependency in dependencies:
                dependency_community_id = communities_files.get(dependency)
                if dependency_community_id != community_id:
                    outer_imports[community_id] += 1
                    outer_imports_in_file += 1
                    if dependency_community_id is not None:
                        outer_exports[dependency_community_id] += 1
                    if file not in files_with_outer_imports.get(community_id):
                        files_with_outer_imports.get(community_id).append(file)
                    if dependency not in files_with_outer_exports.get(
                        dependency_community_id
                    ):
                        files_with_outer_exports.get(dependency_community_id).append(
                            dependency
                        )

            max_outer_imports_one_file[community_id] = max(
                max_outer_imports_one_file.get(community_id), outer_imports_in_file
            )
            max_outer_exports_one_file[community_id] = max(
                max_outer_exports_one_file.get(community_id),
                files_outer_exports.get(file),
            )

    # Calculate metrics for each community
    for community_id, community in communities.items():
        # Create the metrics dictionary for the community
        community_outer_exports = outer_exports.get(community_id)
        community_outer_imports = outer_imports.get(community_id)
        community_metrics[community_id] = {
            "files": len(community),
            "outerConnections": community_outer_exports + community_outer_imports,
            "outerImports": community_outer_imports,
            "outerExports": community_outer_exports,
            "maxOuterImportsOneFile": max_outer_imports_one_file.get(community_id),
            "maxOuterExportsOneFile": max_outer_exports_one_file.get(community_id),
            "filesWithOuterImports": files_with_outer_imports.get(community_id),
            "filesWithOuterExports": files_with_outer_exports.get(community_id),
        }

        total_outer_imports += community_outer_imports
        total_outer_exports += community_outer_exports
        total_outer_connections += community_outer_exports + community_outer_imports

    # Add summary metrics to the result dictionary
    community_metrics["Summary"] = {
        "communities": len(communities.keys()),
        "outerConnections": total_outer_connections,
        "outerImports": total_outer_imports,
        "outerExports": total_outer_exports,
        "maxOuterImportsOneFile": max(max_outer_imports_one_file.values()),
        "maxOuterExportsOneFile": max(max_outer_exports_one_file.values()),
    }

    return community_metrics


def group_files_to_communities(file_paths):
    """
    Groups the given file paths into communities based on their root directory.

    Args:
        file_paths (List[str]): A list of file paths.

    Returns:
        Dict[str, List[str]]: A dictionary mapping community names to a list of file paths belonging to that community.
    """
    communities = {}

    for file_path in file_paths:
        root_dir = os.path.dirname(file_path)
        community_name = root_dir.split(os.path.sep)[0]

        if community_name not in communities:
            communities[community_name] = []

        communities[community_name].append(file_path)

    return communities
