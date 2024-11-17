import matplotlib.pyplot as plt
import networkx as nx

_file = open("Input", 'r')
_lines = [line.removesuffix("\n") for line in _file.readlines()]

G = nx.Graph()

for line in _lines:
    source, targets = line.split(": ")

    for target in targets.split(" "):
        G.add_edge(source, target)

nx.set_node_attributes(G, 1, "graph")

pos = nx.spring_layout(G, seed=4)
nx.draw(G, pos, with_labels=True)
plt.show()

# edges_to_remove = [("pzl", "hfx"), ("bvb", "cmg"), ("nvd", "jqt")]  # for example
edges_to_remove = [("mbk", "qnd"), ("lcm", "ddl"), ("pcs", "rrl")]  # for input determined by plotting
G.remove_edges_from(edges_to_remove)

# find all graphs in second subgraph
graph_2_unvisited = [edges_to_remove[0][0]]
graph_2_visited = []
graph_2_count = 0
while graph_2_unvisited:
    current_node = graph_2_unvisited.pop()
    G.nodes[current_node]['graph'] = 2

    graph_2_unvisited.extend([neighbor for neighbor in G[current_node] if
                              neighbor not in graph_2_visited and neighbor not in graph_2_unvisited])

    graph_2_visited.append(current_node)
    graph_2_count += 1

graph_1_count = len(G) - graph_2_count

print(f"Part 1: {graph_1_count * graph_2_count}")
nx.draw(G, pos, with_labels=True)
plt.show()
