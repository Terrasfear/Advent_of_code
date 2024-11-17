from math import inf
from heapdict import heapdict
from operator import add, mod
import pickle

_file = open("input")
_lines = [line.removesuffix("\n") for line in _file.readlines()]

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

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


def included_in(a: int, b: range) -> bool:
    return a in b


def coordinate_in_area(coordinate: (int, int), area: (range, range)):
    return all(map(included_in, coordinate, area))


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


def one_block_from_start(start: (int, int), block_size: (int, int)) -> (range, range):
    return (range(start[0] * block_size[0], (start[0] + 1) * block_size[0]),
            range(start[1] * block_size[1], (start[1] + 1) * block_size[1]))


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


def print_reachable_inf(distance_map: heapdict, floor_plan: dict, original_shape: (int, int), start: (int, int),
                        print_range: (range, range), max_steps):
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


def num_reachable_in_range(distance_map, max_steps, search_range: (range, range)):
    even_odd = max_steps % 2

    reachable = 0
    for row in search_range[0]:
        for col in search_range[1]:
            if (row, col) in distance_map:
                dist = distance_map[(row, col)]
                if dist <= max_steps and dist % 2 == even_odd:
                    reachable += 1

    return reachable


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
        max_height = max(max_height, current_node_key[0] + 1)

        min_width = min(min_width, current_node_key[1])
        max_width = max(max_width, current_node_key[1] + 1)

        current_step = current_node_dist + 1

        if print_progress:
            if current_step - last_step == 1:
                if current_step % print_progress == 0:
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

# steps = 26501365
steps = 327
equivalent_steps = 327


_dist_map, _trail, _end_map_ranges = Dijkstra_inf(_floor_plan, _floor_plan_shape, _start, equivalent_steps,
                                                  print_progress=50)

save("327_steps", "_dist_map", "_end_map_ranges")

quit()

full_blocks = steps // _floor_plan_shape[0]
remainder = steps % _floor_plan_shape[0]

# full blocks
num_full_odd_blocks = (full_blocks - 1) ** 2
num_full_even_blocks = full_blocks ** 2
reachable_in_full_odd_block = num_reachable_in_range(_dist_map, equivalent_steps,
                                                     one_block_from_start((0, 0), _floor_plan_shape))
reachable_in_full_even_block = num_reachable_in_range(_dist_map, equivalent_steps,
                                                      one_block_from_start((0, 1), _floor_plan_shape))

reachable_in_full_blocks = (num_full_odd_blocks * reachable_in_full_odd_block +
                            num_full_even_blocks * reachable_in_full_even_block)

# corner pieces
reachable_N_corner = num_reachable_in_range(_dist_map, equivalent_steps,
                                            one_block_from_start((-2, 0), _floor_plan_shape))
reachable_E_corner = num_reachable_in_range(_dist_map, equivalent_steps,
                                            one_block_from_start((0, 2), _floor_plan_shape))
reachable_S_corner = num_reachable_in_range(_dist_map, equivalent_steps,
                                            one_block_from_start((2, 0), _floor_plan_shape))
reachable_W_corner = num_reachable_in_range(_dist_map, equivalent_steps,
                                            one_block_from_start((0, -2), _floor_plan_shape))

reachable_in_corners = reachable_N_corner + reachable_E_corner + reachable_S_corner + reachable_W_corner

# edge pieces
num_even_edge_pieces = full_blocks
num_odd_edge_pieces = full_blocks - 1
# NE
NE_even_edge = num_reachable_in_range(_dist_map, equivalent_steps,
                                      one_block_from_start((-1, 1), _floor_plan_shape))
NE_odd_edge = num_reachable_in_range(_dist_map, equivalent_steps,
                                     one_block_from_start((-1, 2), _floor_plan_shape))
# NW
NW_even_edge = num_reachable_in_range(_dist_map, equivalent_steps,
                                      one_block_from_start((-1, -1), _floor_plan_shape))
NW_odd_edge = num_reachable_in_range(_dist_map, equivalent_steps,
                                     one_block_from_start((-1, -2), _floor_plan_shape))
# SE
SE_even_edge = num_reachable_in_range(_dist_map, equivalent_steps,
                                      one_block_from_start((1, 1), _floor_plan_shape))
SE_odd_edge = num_reachable_in_range(_dist_map, equivalent_steps,
                                     one_block_from_start((1, 2), _floor_plan_shape))
# SW
SW_even_edge = num_reachable_in_range(_dist_map, equivalent_steps,
                                      one_block_from_start((1, -1), _floor_plan_shape))
SW_odd_edge = num_reachable_in_range(_dist_map, equivalent_steps,
                                     one_block_from_start((1, -2), _floor_plan_shape))

reachable_in_even_edges = num_even_edge_pieces * (NE_even_edge + NW_even_edge + SE_even_edge + SW_even_edge)
reachable_in_odd_edges = num_odd_edge_pieces * (NE_odd_edge + NW_odd_edge + SE_odd_edge + SW_odd_edge)
reachable_in_edges = reachable_in_odd_edges + reachable_in_even_edges

total_reachable = reachable_in_full_blocks + reachable_in_corners + reachable_in_edges

# print_reachable_inf(_dist_map, _floor_plan, _floor_plan_shape, _start, _end_map_ranges, steps)
# print_reachable_inf(_dist_map, _floor_plan, _floor_plan_shape, _start, (range(_floor_plan_shape[0]),range(_floor_plan_shape[1])), steps)

# _dist_map, _trails = Dijkstra(_map_unvisited, _start, steps)
# print_reachable_(_dist_map, _floor_plan, len(_lines), len(_lines[0]), steps)
# print_dists(_dist_map, _floor_plan, len(_lines), len(_lines[0]))

print(f"Part 1: {num_reachable(_dist_map, 64)}")
print(f"Part 2: {total_reachable}")
print(num_reachable(_dist_map, 327))

# print_floor_plan_inf(_floor_plan, _floor_plan_shape, _start,
#                      (range(-_floor_plan_shape[0],2*_floor_plan_shape[0]),
#                       range(-_floor_plan_shape[1],2*_floor_plan_shape[1])))

pass
