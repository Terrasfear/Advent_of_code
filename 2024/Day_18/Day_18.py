def argmin_dict(d: dict):
    return min(d, key=d.get)


def get_neighbours(node: tuple[int, int], border: tuple[int, int]) -> dict[tuple[int, int], int]:
    # returns all possible neighbours in the range( [0,border[0]), [0,border[1])) , and the cost of going to said neighbour

    steps = [(1, 0),
             (-1, 0),
             (0, 1),
             (0, -1)]

    neighbours = {}

    for step in steps:
        neighbour = (node[0] + step[0], node[1] + step[1])
        if neighbour[0] in range(border[0]) and neighbour[1] in range(border[1]):
            neighbours[neighbour] = 1

    return neighbours


def dijkstra(vertices: dict[tuple[int, int], str], source: tuple[int, int], target: tuple[int, int], border: tuple[int, int]):
    target_reached = False

    distances_to_source = {}
    previous_vertex_to_source = {}
    unvisited_nodes = {}
    visited = {}

    start_value = 1000000000

    for vertex in vertices:
        if vertices[vertex] == "#":
            continue
        distances_to_source.update({vertex: start_value})
        previous_vertex_to_source.update({vertex: None})
        unvisited_nodes.update({vertex: start_value})
        visited.update({vertex: False})

    distances_to_source[source] = 0
    unvisited_nodes[source] = 0

    while unvisited_nodes:
        node = argmin_dict(unvisited_nodes)
        unvisited_nodes.pop(node)
        visited[node] = True

        if node == target:
            target_reached = True
            break

        if distances_to_source[node] == start_value:
            break  # in case of unreachable places

        neighbours = get_neighbours(node, border)
        for neighbour in neighbours:
            if vertices[neighbour] == "#":
                continue

            distance = distances_to_source[node] + neighbours[neighbour]

            if distance > start_value:
                raise Exception("Start value exceeded")

            if distance < distances_to_source[neighbour]:
                distances_to_source[neighbour] = distance
                unvisited_nodes[neighbour] = distance
                previous_vertex_to_source[neighbour] = node

    return distances_to_source, previous_vertex_to_source, target_reached


def backtrack(vertices: dict[tuple[int, int], str], steps_to_source: dict[tuple[int, int], tuple[int, int]], target: tuple[int, int]):
    path = [target]

    while path:
        step = path.pop()

        vertices[step] = "O"

        if next_steps := steps_to_source[step]:
            path.append(next_steps)


def print_grid(grid_size, map_dict: dict[tuple[int, int], str]):
    for y in range(grid_size):
        for x in range(grid_size):
            print(map_dict[(x, y)], end="")
        print()


_file_name = "Input"

if _file_name == "Input":
    _grid_size = 71
    _steps_P1 = 1024
else:
    _grid_size = 7
    _steps_P1 = 12

with open(_file_name, "r") as _file:
    _lines = _file.readlines()

_start = (0, 0)
_target = (_grid_size - 1, _grid_size - 1)

_target_reached = True

_highest_reached = 0
_lowest_not_reached = len(_lines)

_steps = _steps_P1

while True:

    _map = {(x, y): "." for y in range(_grid_size) for x in range(_grid_size)}
    for step in range(_steps):
        corruption = _lines[step].removesuffix("\n").split(",")
        corruption = (int(corruption[0]), int(corruption[1]))

        _map[corruption] = "#"

    _distances, _path, _target_reached = dijkstra(_map, _start, _target, (_grid_size, _grid_size))

    print(f"{_steps}: {_target_reached}")

    if _target_reached:
        _highest_reached = _steps
    else:
        _lowest_not_reached = _steps

    _new_steps = (_highest_reached + _lowest_not_reached) // 2

    if _new_steps == _steps:
        break

    if _steps == _steps_P1:
        P1 = _distances[_target]

    _steps = _new_steps

print(f"Part 1: {P1}")
print(f"Part 2: {_lines[_lowest_not_reached - 1]}")
