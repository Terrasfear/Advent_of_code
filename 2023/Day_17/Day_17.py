from math import inf
from operator import add, sub, mul

import heapdict

_file = open("Input", 'r')
_lines = [line.removesuffix('\n') for line in _file.readlines()]

# _part = "Part 1"
_part = "Part 2"

def large_crucible(current_node: (int, int, str, int), height: int, width: int) -> [(int, int, str, int)]:
    neighbours = []

    for direction in ["N", "E", "S", "W"]:
        neighbour = list(current_node)
        if direction == "N":
            if current_node[0] == 0 or current_node[2] == "S":
                continue
            else:
                neighbour[0] -= 1

        elif direction == "E":
            if current_node[1] >= width - 1 or current_node[2] == "W":
                continue
            else:
                neighbour[1] += 1

        elif direction == "S":
            if current_node[0] >= height - 1 or current_node[2] == "N":
                continue
            else:
                neighbour[0] += 1

        elif direction == "W":
            if current_node[1] == 0 or current_node[2] == "E":
                continue
            else:
                neighbour[1] -= 1

        neighbour[2] = direction

        if direction == current_node[2]:
            neighbour[3] += 1
            if neighbour[3] > 3:
                continue
        else:
            neighbour[3] = 1

        neighbours.append(tuple(neighbour))
    return neighbours


def ultra_crucible(current_node: (int, int, str, int), height: int, width: int) -> [(int, int, str, int)]:
    neighbours = []

    minimal_step = 4

    for direction in ["N", "E", "S", "W"]:
        if current_node[3] < minimal_step and current_node[2] != direction:
            continue

        neighbour = list(current_node)
        if direction == "N":
            if current_node[0] == 0 or current_node[2] == "S":
                continue
            elif current_node[2] != direction and current_node[0] < minimal_step:
                continue
            else:
                neighbour[0] -= 1

        elif direction == "E":
            if current_node[1] >= width - 1 or current_node[2] == "W":
                continue
            elif current_node[2] != direction and current_node[1] > width - 1 - minimal_step:
                continue
            else:
                neighbour[1] += 1

        elif direction == "S":
            if current_node[0] >= height - 1 or current_node[2] == "N":
                continue
            elif current_node[2] != direction and current_node[0] > height - 1 -minimal_step:
                continue
            else:
                neighbour[0] += 1

        elif direction == "W":
            if current_node[1] == 0 or current_node[2] == "E":
                continue
            elif current_node[2] != direction and current_node[1] < minimal_step:
                continue
            else:
                neighbour[1] -= 1

        neighbour[2] = direction

        if direction == current_node[2]:
            neighbour[3] += 1
        else:
            neighbour[3] = 1

        if neighbour[3] > 10:
            continue

        neighbours.append(tuple(neighbour))
    return neighbours


def Dijkstra(graph_unvisited: heapdict.heapdict, start, destination, grid_height, grid_width):
    distances = heapdict.heapdict()
    previous_steps = {}

    keys = graph_unvisited.keys()
    start_keys = [key for key in keys if key[0] == start[0] and key[1] == start[1]]
    destination_keys = [key for key in keys if key[0] == destination[0] and key[1] == destination[1]]
    for key in start_keys:
        graph_unvisited[key] = 0
    pass

    while graph_unvisited:
        current_node_key, current_node_dist = graph_unvisited.popitem()

        # generate neighbours
        if _part == "Part 1":
            neighbours = large_crucible(current_node_key, height, width)
        elif _part == "Part 2":
            neighbours = ultra_crucible(current_node_key, height, width)

        for neighbour in neighbours:
            if neighbour not in graph_unvisited:
                continue

            traversed_distance = sum(map(sub, current_node_key[:2], neighbour[:2]))

            if traversed_distance == -1 or traversed_distance == 1:
                energy_lost_in_travel = heat_loss_map[neighbour[:2]]
            else:
                energy_lost_in_travel = 0
                for i in range(abs(traversed_distance)):
                    energy_lost_in_travel += heat_loss_map[tuple(map(add, current_node_key[:2],list(map(mul, [i+1]*2, transformation[neighbour[2]]))))]

            new_dist = current_node_dist + energy_lost_in_travel
            if new_dist < graph_unvisited[neighbour]:
                distances[neighbour] = new_dist
                graph_unvisited[neighbour] = new_dist
                previous_steps[neighbour] = current_node_key

    return distances, previous_steps


heat_loss_map = {}
Graph = heapdict.heapdict()

height = len(_lines)
width = len(_lines[0])

start = (0, 0)
destination = (height - 1, width - 1)

# populate graph and heatmap
for row_idx in range(height):
    for col_idx in range(width):
        heat_loss = int(_lines[row_idx][col_idx])
        heat_loss_map[(row_idx, col_idx)] = heat_loss

        # Northern approaches
        for i in range(min(10, max(0, height - 1 - row_idx))):
            Graph[(row_idx, col_idx, "N", i + 1)] = inf

        # Eastern approaches
        for i in range(min(10, max(0, col_idx))):
            Graph[(row_idx, col_idx, "E", i + 1)] = inf

        # Southern approaches
        for i in range(min(10, max(0, row_idx))):
            Graph[(row_idx, col_idx, "S", i + 1)] = inf

        # Western approaches
        for i in range(min(10, max(0, width - 1 - col_idx))):
            Graph[(row_idx, col_idx, "W", i + 1)] = inf

dists, steps = Dijkstra(Graph, start, destination, height, width)

target_keys = [key for key in dists if key[:2] == destination]

print(f"{_part}: {dists[target_keys[0]]}")

path = [target_keys[0]]
directions = {}
while True:
    directions[path[-1][:2]] = path[-1][2]
    path.append(steps[path[-1]])
    if path[-1][:2] == start:
        directions[start] = path[-2][2]
        break

# print(path)
print(path[::-1])
for row_idx in range(height):
    for col_idx in range(width):
        if (row_idx, col_idx) in directions:
            step = directions[(row_idx, col_idx)]
            if step == "N":
                print("^", end="")
            elif step == "E":
                print(">", end="")
            elif step == "S":
                print("v", end="")
            else:
                print("<", end="")
        else:
            print(".", end="")
    print()
