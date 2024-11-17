from math import inf
from operator import add
from string import ascii_letters
import networkx as nx

_file = open("Input", 'r')
_lines = [line.removesuffix('\n') for line in _file.readlines()]

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
slopes = ["<", "^", ">", "v"]


def print_map():
    for row_idx in range(map_size[0]):
        for col_idx in range(map_size[1]):
            if (row_idx, col_idx) in _nodes:
                print(_nodes[(row_idx, col_idx)], end='')
            elif (row_idx, col_idx) in _max_path:
                print("O", end='')
            else:
                print(_terrain_map[(row_idx, col_idx)], end='')
        print()


def fill_maps():
    # closes ends for neighbor detection
    _terrain_map.update({(-1, 1): "#",
                         (map_size[0], map_size[1] - 2): "#"})

    for row_idx, row in enumerate(_lines):
        for col_idx, char in enumerate(row):
            _terrain_map[(row_idx, col_idx)] = char
            if char != "#":
                _not_traversed.append((row_idx, col_idx))

    # to prevent backtracking on the first step
    _not_traversed.remove((0, 1))


def find_nodes():
    _nodes.update({(0, 1): "S",
                   (map_size[0] - 1, map_size[1] - 2): "E"})
    _paths_per_start.update({"S": [], "E": []})

    letters = list(ascii_letters)
    letters.reverse()
    # shuffle(letters)
    letters.remove("S")
    letters.remove("E")
    letters.remove("V")
    letters.remove("v")

    next_name = letters.pop()
    for cord in _not_traversed:
        node = make_node(cord, next_name)
        if node:
            next_name = letters.pop()

    # add reverse couples
    nodes = list(_nodes.keys())
    for cord in nodes:
        _nodes[_nodes[cord]] = cord


# test if coordinate is node, if it is not a registered node, register it.
# returns node name or false
def make_node(cord: (int, int), name) -> (bool or str):
    node = False

    if _terrain_map[cord] in slopes:
        pass
    elif cord in _nodes:
        pass
    else:
        neighbours = [tuple(map(add, cord, direction)) for direction in directions]
        if sum([1 for neighbour in neighbours if _terrain_map[neighbour] in slopes]) > 2:
            node = name
            _nodes[cord] = node
            _paths_per_start[node] = []

    return node


def is_node(cord: (int, int)):
    if cord in _nodes:
        return _nodes[cord]
    else:
        return False


def possible_steps(cord) -> (int, int):
    terrain = _terrain_map[cord]

    # on slope, only one option
    if terrain == ">":
        return [tuple(map(add, cord, directions[0]))]
    elif terrain == "v":
        return [tuple(map(add, cord, directions[1]))]
    elif terrain == "<":
        return [tuple(map(add, cord, directions[2]))]
    elif terrain == "^":
        return [tuple(map(add, cord, directions[3]))]

    possible_destinations = [tuple(map(add, cord, direction)) for direction in directions]

    illegal_step_terrain = ["<", "^", ">", "v"]
    # filter upslope steps
    possible_destinations = [possible_destinations[i] for i in range(4) if
                             _terrain_map[possible_destinations[i]] != illegal_step_terrain[i]]

    # don't step in wall
    possible_destinations = [possible_destination for possible_destination in possible_destinations if
                             _terrain_map[possible_destination] != "#"]

    return possible_destinations


def generate_graph(starting_point, starting_point_name):
    # note that the starting point is not the starting node, but one
    # point further
    path_length = 1
    path = [_nodes[starting_point_name]]
    current_point = starting_point
    while True:
        node = is_node(current_point)
        if node:
            # arrived at node
            # add path
            path.append(current_point)
            _paths[(starting_point_name, node)] = (path_length, path)
            _paths_per_start[starting_point_name].append((starting_point_name, node))

            if _paths_per_start[node] == [] and node != "E":
                next_points = possible_steps(current_point)
                for next_point in next_points:
                    generate_graph(next_point, node)

            break
        else:
            path.append(current_point)

            # finding next step
            next_point = [point for point in possible_steps(current_point) if point != path[-2]]

            if len(next_point) != 1:
                print("error, there should always be 1 next point")
                quit(-1)

            path_length += 1
            current_point = next_point[0]


def make_topological_order(edges_per_vertices):
    S = ["S"]  # vertices without incoming edges
    L = []  # ordered vertices

    edges = sum(edges_per_vertices.values(), [])

    while S:
        n = S.pop()
        L.append(n)

        for edge in [edge for edge in edges if n == edge[0]]:
            m = edge[1]
            edges.remove(edge)

            if len([edge for edge in edges if m == edge[1]]) == 0:
                S.append(m)

    return L


# vertices in topological order
def shortest_dist_DAG(vertices, edges) -> (dict, dict):
    distances = {vert: inf for vert in vertices}
    predecessors = {vert: None for vert in vertices}

    distances[vertices[0]] = 0

    for v in vertices:
        for u in [edge[1] for edge in edges if v == edge[0]]:
            weight = _paths[(v, u)][0]
            if distances[u] > distances[v] + weight:
                distances[u] = distances[v] + weight
                predecessors[u] = v

    return distances, predecessors


def find_longest_distance(graph: nx.Graph, start, end):
    paths = nx.all_simple_paths(graph, start, end)

    min_path_vertices = int(len(graph) * 3/4)

    max_dist = 0
    max_path = []
    for path in paths:
        if len(path) <= min_path_vertices:
            continue

        dist = 0
        for vertex_idx in range(len(path) -1):
            dist += graph.edges[(path[vertex_idx], path[vertex_idx+1])]["weight"]
        if dist > max_dist:
            max_dist = dist
            max_path = path

    return max_dist, max_path

map_size = (len(_lines), len(_lines[0]))

_terrain_map = {}
_not_traversed = []
_max_path = []
_nodes = {}
_paths = {}
_paths_per_start = {}

fill_maps()

find_nodes()

generate_graph((1, 1), "S")

# negate distances
for path in _paths:
    _paths[path] = (-_paths[path][0], _paths[path][1])

# get vertices in topological order
_ordered_vertices = make_topological_order(_paths_per_start.copy())
dists, preds = shortest_dist_DAG(_ordered_vertices, sum(_paths_per_start.values(), []))

print(f"Part 1: {-dists['E']}")

weighted_edges = []
for edge in _paths:
    weighted_edges.append((edge[0], edge[1], -_paths[edge][0]))

G = nx.Graph()

G.add_weighted_edges_from(weighted_edges)

dist, _max_path = find_longest_distance(G, "S", "E")

print(f"Part 2: {dist}")
#6286 too low

pos = nx.spring_layout(G, seed=8)

# nx.draw(G, pos, with_labels=True)
#
# nx.draw_networkx_nodes(G, pos)
#
# nx.draw_networkx_edges(G, pos)
#
# edge_labels = nx.get_edge_attributes(G, "weight")
# nx.draw_networkx_edge_labels(G, pos, edge_labels)


