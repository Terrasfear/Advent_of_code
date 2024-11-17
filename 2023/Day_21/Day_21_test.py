from math import inf
from heapdict import heapdict
from operator import add, mod
import matplotlib.pyplot as plt

import pickle


def save(filename, *args):
    # Get global dictionary
    glob = globals()
    d = {}
    for v in args:
        # Copy over desired values
        d[v] = glob[v]
    with open(filename, 'wb') as f:
        # Put them in the file
        pickle.dump(d, f)


def load(filename):
    # Get global dictionary
    glob = globals()
    with open(filename, 'rb') as f:
        for k, v in pickle.load(f).items():
            # Set each global variable to the value from the file
            glob[k] = v



_file = open("input")
_lines = [line.removesuffix("\n") for line in _file.readlines()]

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def print_dists(distance_map, floor_plan, height, width):
    for row in range(height):
        for col in range(width):
            if (row, col) in distance_map and distance_map[(row, col)] != inf:
                print(f"{distance_map[(row, col)]}", end="\t")
            else:
                print(f"{floor_plan[(row, col)]}", end="\t")
        print()


def print_reachable(distance_map, floor_plan, height, width, max_steps):
    even_odd = max_steps % 2

    for row in range(height):
        for col in range(width):
            if ((row, col) in distance_map and distance_map[(row, col)] <= max_steps and
                    distance_map[(row, col)] % 2 == even_odd):
                print(f"O", end="")
            else:
                print(f"{floor_plan[(row, col)]}", end="")
        print()


def print_floor_plan_inf(floor_plan: dict, original_shape: (int, int), start: (int, int), print_range: (range, range)):
    original_height, original_width = original_shape
    print_height_range, print_width_range = print_range

    for row in print_height_range:
        for col in print_width_range:
            char = floor_plan[tuple(map(mod, (row, col), original_shape))]
            if char == "S" and (row, col) != start:
                char = "."
            print(char, end="")
        print()


def print_reachable_inf(distance_map: heapdict, floor_plan: dict, original_shape: (int, int), start: (int, int), print_range: (range, range), max_steps):
    print_height_range, print_width_range = print_range
    even_odd = max_steps % 2

    for row in print_height_range:
        for col in print_width_range:
            if ((row, col) in distance_map and
                    distance_map[(row, col)] <= max_steps and
                    distance_map[(row, col)] % 2 == even_odd):
                print(f"O", end="")
            else:
                char = floor_plan[tuple(map(mod, (row, col), original_shape))]
                if char == "S" and (row, col) != start:
                    char = "."
                print(char, end="")
        print()


def num_reachable(distance_map, max_steps):
    even_odd = max_steps % 2
    return sum([1 for dist in distance_map.values() if dist <= max_steps and dist % 2 == even_odd])


def Dijkstra_inf(floor_plan: dict, floor_plan_size: (int, int), start: (int, int), max_steps: int, print_progress=0):
    min_height = start[0]
    max_height = min_height + 1
    min_width = start[1]
    max_width = min_width + 1

    distances = heapdict()
    previous_steps = {}

    graph_unvisited = heapdict({start: 0})
    graph_visited = []
    distances[start] = 0

    last_step = 0
    while True:
        current_node_key, current_node_dist = graph_unvisited.popitem()
        graph_visited.append(current_node_key)

        min_height = min(min_height, current_node_key[0])
        max_height = max(max_height, current_node_key[0]+1)

        min_width = min(min_width, current_node_key[1])
        max_width = max(max_width, current_node_key[1] + 1)

        current_step = current_node_dist + 1

        if print_progress:
            if current_step - last_step == 1:
                if current_step%print_progress == 0:
                    print(f"{current_step:6d}/{max_steps}")

            last_step = current_step

        if current_node_dist >= max_steps:
            break

        neighbours = [tuple(map(add, current_node_key, step)) for step in directions]

        for neighbour in neighbours:
            if neighbour in graph_visited:
                continue
            if floor_plan[tuple(map(mod, neighbour, floor_plan_size))] == "#":
                continue

            neighbour_distance = graph_unvisited.get(neighbour, inf)

            if current_step < neighbour_distance:
                distances[neighbour] = current_step
                graph_unvisited[neighbour] = current_step
                previous_steps[neighbour] = current_node_key

    return distances, previous_steps, (range(min_height, max_height), range(min_width, max_width))


def Dijkstra(graph_unvisited: heapdict, start, max_steps):
    distances = heapdict()
    previous_steps = {}

    graph_unvisited[start] = 0
    distances[start] = 0

    current_step = 1
    while graph_unvisited:
        current_node_key, current_node_dist = graph_unvisited.popitem()

        current_step = current_node_dist + 1

        if current_node_dist >= max_steps:
            break

        neighbours = [tuple(map(add, current_node_key, step)) for step in directions]

        for neighbour in neighbours:
            if neighbour not in graph_unvisited:
                continue

            if current_step < graph_unvisited[neighbour]:
                distances[neighbour] = current_step
                graph_unvisited[neighbour] = current_step
                previous_steps[neighbour] = current_node_key

    return distances, previous_steps


_map_unvisited = heapdict()
_floor_plan = dict()
_floor_plan_shape = (len(_lines), len(_lines[0]))
_start = (0, 0)
for row_idx, line in enumerate(_lines):
    for col_idx, char in enumerate(line):
        _floor_plan[(row_idx, col_idx)] = char

        if char != "#":
            _map_unvisited[(row_idx, col_idx)] = inf
        if char == "S":
            _start = (row_idx, col_idx)


steps = 200

# _dist_map, _trail, _end_map_ranges = Dijkstra_inf(_floor_plan, _floor_plan_shape, _start, steps, print_progress=50)
# print_reachable_inf(_dist_map, _floor_plan, _floor_plan_shape, _start, _end_map_ranges, steps)
# print_reachable_inf(_dist_map, _floor_plan, _floor_plan_shape, _start, (range(_floor_plan_shape[0]),range(_floor_plan_shape[1])), steps)

_dist_map, _ = Dijkstra(_map_unvisited, (_start[0],0), steps)
_dist_map_N, _ = Dijkstra(_map_unvisited, (_start[0],0), steps)
_dist_map_E, _ = Dijkstra(_map_unvisited, (_start[0],0), steps)
_dist_map_S, _ = Dijkstra(_map_unvisited, (_start[0],0), steps)
_dist_map_W, _ = Dijkstra(_map_unvisited, (_start[0],0), steps)


# print_reachable(_dist_map, _floor_plan, len(_lines), len(_lines[0]), steps)
# print_dists(_dist_map, _floor_plan, len(_lines), len(_lines[0]))

print(f"Part 1: {num_reachable(_dist_map, steps)}")

print(_dist_map[_start])
plots_per_trail_length = [num_reachable(_dist_map,max_steps) for max_steps in range(steps)]


# plt.plot(plots_per_trail_length)

plt.show()

pass
