import pickle
from operator import mod

from heapdict import heapdict

_file = open("input")
_lines = [line.removesuffix("\n") for line in _file.readlines()]


def load(filename):
    # Get global dictionary
    glob = globals()
    with open(filename, 'rb') as f:
        for k, v in pickle.load(f).items():
            # Set each global variable to the value from the file
            glob[k] = v


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


def one_block_from_start(start: (int, int), block_size: (int, int)) -> (range, range):
    return (range(start[0] * block_size[0], (start[0] + 1) * block_size[0]),
            range(start[1] * block_size[1], (start[1] + 1) * block_size[1]))


_floor_plan = dict()
_floor_plan_shape = (len(_lines), len(_lines[0]))
_start = (0, 0)
for row_idx, line in enumerate(_lines):
    for col_idx, char in enumerate(line):
        _floor_plan[(row_idx, col_idx)] = char

        if char == "S":
            _start = (row_idx, col_idx)


load("327_steps")
_dist_map: dict
_end_map_ranges: (range, range)

print_reachable_inf(_dist_map, _floor_plan, _floor_plan_shape, _start, (range(_floor_plan_shape[0]),range(_floor_plan_shape[1])), 65)


steps = 327
equivalent_steps = 327

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

print(f"64 steps: {num_reachable(_dist_map, 64)}")
print(f"65 steps: {num_reachable(_dist_map, 65)}")
print(f"66 steps: {num_reachable(_dist_map, 66)}")
print(f"196 steps: {num_reachable(_dist_map, 196)}")
print(f"327 steps: {num_reachable(_dist_map, 327)}")




# print_floor_plan_inf(_floor_plan, _floor_plan_shape, _start,
#                      (range(-_floor_plan_shape[0],2*_floor_plan_shape[0]),
#                       range(-_floor_plan_shape[1],2*_floor_plan_shape[1])))

pass
