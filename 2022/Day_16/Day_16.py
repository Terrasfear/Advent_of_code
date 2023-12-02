import networkx as nx
from pyvis.network import Network
import re

filename = "Input_test"
file = open(filename, 'r')
lines = file.readlines()


def action(path_list, current_path:list, closed_nodes:list, total_pressure_released, time_left):

    for next_node in closed_nodes:
        dist = nx.shortest_path_length(G, current_path[-1], next_node, "weight")

        if dist+1 > time_left:  # not enough time to travel and open the valve, so cleanup
            path_with_pressure = current_path.copy()
            path_with_pressure.append(total_pressure_released)
            if path_list[0][-1] < total_pressure_released:
                path_list.clear()
                path_list.append(path_with_pressure)
            continue

        # going to and opening next_node
        new_time_left = time_left - dist - 1
        new_total_pressure_released = total_pressure_released + G.nodes[next_node]["value"] * new_time_left
        new_current_path = current_path.copy()
        new_current_path.append(next_node)
        new_closed_nodes = closed_nodes.copy()
        new_closed_nodes.remove(next_node)

        if new_time_left == 0 or new_closed_nodes == []: # no further actions possible
            path_with_pressure = new_current_path.copy()
            path_with_pressure.append(new_total_pressure_released)

            if path_list[0][-1] < total_pressure_released:
                path_list.clear()
                path_list.append(path_with_pressure)
            continue

        # next_step
        action(path_list, new_current_path, new_closed_nodes, new_total_pressure_released, new_time_left)


G = nx.Graph()
for line in lines:
    new_node = re.search('Valve ([A-Z][A-Z]) ',line).group(1)

    flow = int(re.search('flow rate=(\d+);',line).group(1))
    edge_targets = re.findall("[A-Z]{2}",line)[1:]

    if new_node == "AA":
        G.add_node(new_node, value=flow, color='red')
    elif flow:
        G.add_node(new_node, value=flow)
    else:
        G.add_node(new_node, value=flow, color='grey')

    for edge_target in edge_targets:
        if edge_target in list(G.nodes):
            G.add_edge(new_node, edge_target, weight=1)

# clean graph by removing nodes with 0 flow and a degree of 2 (bridging with an edge of a higher weight), or a degree of 1
for node in list(G.nodes):
    if node == "AA":    # don't remove start
        continue

    if G.nodes()[node]["value"] == 0:   # valve less node
        if G.degree[node] == 1:
            G.remove_node(node)
            continue

        if G.degree[node] == 2:
            attached_nodes = list(G.neighbors(node))
            new_weight = G.get_edge_data(node, attached_nodes[0])['weight'] + G.get_edge_data(node, attached_nodes[1])['weight']
            G.add_edge(attached_nodes[0], attached_nodes[1], weight=new_weight)
            G.remove_node(node)
            continue


current_path = ["AA"]
closed_nodes = list(G.nodes)
closed_nodes.remove(current_path[-1])
time = 30
pressure_released = 0

path_list = [[0]]
action(path_list, current_path, closed_nodes, pressure_released, time)

pass



# while time_left:
#     node_potentials = [[],[]]
#     for test_node in closed_nodes:
#         if test_node == current_path[-1]:
#             continue
#         if G.nodes[test_node]["value"] == 0:
#             continue
#
#         dist = nx.shortest_path_length(G, current_path[-1], test_node, "weight")
#
#         potential = G.nodes[test_node]["value"]*(time_left-(dist+1))
#
#         print(f"{current_node} -> {test_node}\n\tdistance {dist} minutes\n\tpotential {potential}")
#
#         node_potentials[0].append(test_node)
#         node_potentials[1].append(potential)
#
#
#     break



# net = Network()
# net.from_nx(G)
#
# net.save_graph(filename+".html")