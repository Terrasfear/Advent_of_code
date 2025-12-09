class Grid_2D:
    def __init__(self, lines):
        self.grid = {(row_idx, column_idx): {"value": char, "print": "", "misc": ""}
                     for row_idx, row in enumerate(lines) for column_idx, char in enumerate(row.removesuffix("\n"))}

        self.height = len(lines)
        self.width = len(lines[0].removesuffix("\n"))

    def print(self):
        for row_idx in range(self.height):
            for column_idx in range(self.width):
                cell = self.grid[(row_idx, column_idx)]
                print(cell["print"] + cell["value"][-1], end="\033[00m")
            print()

    def get(self, row_idx, column_idx):
        if self.isInBounds(row_idx, column_idx):
            return self.grid[(row_idx, column_idx)]["value"]
        else:
            return None

    def set(self, row_idx: int, column_idx: int, new_value, reset_mark: bool = False, field="value", append=False):
        if self.isInBounds(row_idx, column_idx):
            entry = self.grid[(row_idx, column_idx)]

            if append:
                entry[field] += new_value
            else:
                entry[field] = new_value

            if reset_mark:
                entry["print"] = ""
        else:
            raise Exception(f"({row_idx},{column_idx}) out of bounds")

    def setBatch(self, points: list[tuple[int, int]], new_value, reset_mark=False, field="value", append=False):
        for point in points:
            self.set(*point, new_value, reset_mark, field, append)

    def setLine(self, start: tuple[int, int], end: tuple[int, int], new_value, reset_mark=False, field="value",
                append=False):
        if start[0] == end[0]:
            points = [(start[0], column) for column in range(min(start[1], end[1]), max(start[1], end[1]) + 1)]
        elif start[1] == end[1]:
            points = [(row, start[1]) for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1)]
        else:
            raise Exception("points not in a cardinal direction")

        self.setBatch(points, new_value, reset_mark, field, append)

    def find(self, char, field="value"):
        return [point for point in self.grid if char in self.grid[point][field]]

    def findInLine(self, char, start, end, field="value"):
        if start[0] == end[0]:
            points = [(start[0], column) for column in range(min(start[1], end[1]), max(start[1], end[1]) + 1)]
        elif start[1] == end[1]:
            points = [(row, start[1]) for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1)]
        else:
            raise Exception("points not in a cardinal direction")

        return [point for point in points if char in self.grid[point][field]]

    def mark(self, row_idx, column_idx, mark: int = 1):
        if self.isInBounds(row_idx, column_idx):
            if 1 <= mark <= 6:  # red, green, yellow, blue, magenta, cyan
                self.grid[(row_idx, column_idx)]["print"] = f"\033[3{mark}m"
            else:
                self.grid[(row_idx, column_idx)]["print"] = ""
        else:
            raise Exception(f"({row_idx},{column_idx}) out of bounds")

    def markBatch(self, points: list[tuple[int, int]], mark: int = 1):
        for point in points:
            self.mark(point[0], point[1], mark)

    def isInBounds(self, row_idx, column_idx):
        return 0 <= row_idx < self.height and 0 <= column_idx < self.width


def argmin(l: list[int]):
    return min(range(len(l)), key=l.__getitem__)


def argmin_dict(d: dict):
    return min(d, key=d.get)


def get_neighbours(node: tuple[int, int, str]) -> dict[tuple[int, int, str], int]:
    # returns all possible neighbours regardless of walls or other obstructions, and the cost of going to said neighbour
    direction = node[2]

    if direction == "N":
        return {(node[0], node[1], "E"): 1000,
                (node[0], node[1], "W"): 1000,
                (node[0] - 1, node[1], "N"): 1}
    elif direction == "E":
        return {(node[0], node[1], "N"): 1000,
                (node[0], node[1], "S"): 1000,
                (node[0], node[1] + 1, "E"): 1}
    elif direction == "S":
        return {(node[0], node[1], "E"): 1000,
                (node[0], node[1], "W"): 1000,
                (node[0] + 1, node[1], "S"): 1}
    elif direction == "W":
        return {(node[0], node[1], "N"): 1000,
                (node[0], node[1], "S"): 1000,
                (node[0], node[1] - 1, "W"): 1}
    else:
        raise Exception(f"unknown direction: {direction}")


def dijkstra_direction_cost(vertices: list[tuple[int, int]], source: tuple[int, int, str], target: tuple[int, int]):
    distances_to_source = {}
    previous_vertex_to_source = {}
    unvisited_nodes = {}

    start_value = 1000000000

    directions = ["N", "E", "S", "W"]
    target_found = [False] * 4

    for vertex in vertices:
        distances_to_source.update({(vertex[0], vertex[1], direction): start_value for direction in directions})
        previous_vertex_to_source.update({(vertex[0], vertex[1], direction): [] for direction in directions})
        unvisited_nodes.update({(vertex[0], vertex[1], direction): start_value for direction in directions})

    distances_to_source[source] = 0
    unvisited_nodes[source] = 0

    while unvisited_nodes:
        node = argmin_dict(unvisited_nodes)
        unvisited_nodes.pop(node)

        if (node[0], node[1]) == target:
            break

        neighbours = get_neighbours(node)
        for neighbour in neighbours:
            if neighbour not in unvisited_nodes:
                continue

            distance = distances_to_source[node] + neighbours[neighbour]

            if distance > start_value:
                raise Exception("Start value exceeded")

            if distance == distances_to_source[neighbour]:
                previous_vertex_to_source[neighbour].append(node)

            if distance < distances_to_source[neighbour]:
                distances_to_source[neighbour] = distance
                unvisited_nodes[neighbour] = distance
                previous_vertex_to_source[neighbour] = [node]

    return distances_to_source, previous_vertex_to_source


def backtrack(grid: Grid_2D, steps_to_source: dict[tuple[int, int, str], list[tuple[int, int, str]]], target: tuple[int, int, str]):
    path = [target]

    while path:
        step = path.pop()

        grid.set(step[0], step[1], "O")
        grid.mark(step[0], step[1], 6)

        if next_steps := steps_to_source[step]:
            path.extend(next_steps)


with open("Input", "r") as _file:
    _lines = _file.readlines()

    _grid = Grid_2D(_lines)

_start = _grid.find("S")[0]
_end = _grid.find("E")[0]
_vertices = _grid.find(".")
_vertices.extend([_start, _end])

_distances, _path_to_source = dijkstra_direction_cost(_vertices, (_start[0], _start[1], "E"), _end)

_target_distances = {(_end[0], _end[1], direction): _distances[(_end[0], _end[1], direction)]
                     for direction in ["N", "E", "S", "W"]}

_best_target = argmin_dict(_target_distances)

backtrack(_grid, _path_to_source,_best_target)
_grid.print()

print(f"Part 1: {_distances[_best_target]}")
print(f"Part 2: {len(_grid.find('O'))}")


