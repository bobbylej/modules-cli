import json

with open('com_dep.json', 'r') as file:
    data = json.load(file)

# Generate the DOT graph
dot_graph = 'digraph dependencies {\n'
for source, targets in data.items():
    for target in targets:
        dot_graph += f'  "{source}" -> "{target}"\n'
dot_graph += '}'

# Save the DOT graph to a file
with open('com_dep.dot', 'w') as dot_file:
    dot_file.write(dot_graph)