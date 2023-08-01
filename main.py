import json
from community_metrics import calculate_community_metrics, group_files_to_communities
from file_dependency import get_files_dependencies
from file_community import (
    detect_communities_for_files_by_greedy_modularity,
    detect_communities_for_files_by_louvain,
    save_communities_in_file,
)
from attribute_parser import get_command_attributes

# ------------------- File Dependencies -------------------

args = get_command_attributes()

if args.files is None:
    exit("No files specified")

file_dependencies = get_files_dependencies(
    args.files,
    {
        "excludeRegExp": args.exclude,
        "tsConfig": args.ts_config,
        "fileExtensions": args.extensions,
        "webpackConfig": args.webpack_config,
        "requireConfig": args.require_config,
    },
)

# ------------------- Current Modularity -------------------

communities_current = group_files_to_communities(file_dependencies.keys())
metrics_current = calculate_community_metrics(communities_current, file_dependencies)
save_communities_in_file(communities_current, "./output/communities_current.json")
with open("./output/metrics_current.json", "w") as json_file:
    json.dump(metrics_current, json_file, indent=2)

with open("./output/file_dependencies.json", "w") as json_file:
    json.dump(file_dependencies, json_file, indent=2)

# ------------------- Greedy Modularity -------------------

communities_greedy = detect_communities_for_files_by_greedy_modularity(
    file_dependencies
)
metrics_greedy = calculate_community_metrics(communities_greedy, file_dependencies)
save_communities_in_file(communities_greedy, "./output/communities_greedy.json")
with open("./output/metrics_greedy.json", "w") as json_file:
    json.dump(metrics_greedy, json_file, indent=2)

# ------------------- Louvain -------------------

communities_louvain = detect_communities_for_files_by_louvain(file_dependencies)
metrics_louvain = calculate_community_metrics(communities_louvain, file_dependencies)
save_communities_in_file(communities_louvain, "./output/communities_louvain.json")
with open("./output/metrics_louvain.json", "w") as json_file:
    json.dump(metrics_louvain, json_file, indent=2)
