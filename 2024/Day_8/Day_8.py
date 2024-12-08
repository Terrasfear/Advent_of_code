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

    def mark(self, row_idx, column_idx, unmark=False):
        if self.isInBounds(row_idx, column_idx):
            if not unmark:
                self.grid[(row_idx, column_idx)]["print"] = f"\033[91m"
            else:
                self.grid[(row_idx, column_idx)]["print"] = ""
        else:
            raise Exception(f"({row_idx},{column_idx}) out of bounds")

    def markBatch(self, points: list[tuple[int, int]]):
        for point in points:
            self.mark(point[0], point[1])

    def isInBounds(self, row_idx, column_idx):
        return 0 <= row_idx < self.height and 0 <= column_idx < self.width


with open("Input", "r") as _file:
    _lines = _file.readlines()

    _grid = Grid_2D(_lines)
    _grid_harmonics = Grid_2D(_lines)

_antennas = [antenna for antenna in _grid.grid.keys()
             if antenna not in _grid.find(".")]
_frequencies = {_grid.get(*antenna) for antenna in _antennas}

_antinodes = set()
_antinodes_harmonics = set(_antennas)
_grid_harmonics.markBatch(_antennas)

for frequency in _frequencies:
    antennas_with_frequency = _grid.find(frequency)
    antenna_pair_indices = [(i, j)
                            for i in range(len(antennas_with_frequency))
                            for j in range(len(antennas_with_frequency))
                            if i != j]

    for antenna_pair in antenna_pair_indices:
        antenna_a = antennas_with_frequency[antenna_pair[0]]
        antenna_b = antennas_with_frequency[antenna_pair[1]]

        antenna_distance = (antenna_b[0] - antenna_a[0],
                            antenna_b[1] - antenna_a[1])  # manhattan distance

        antinode = tuple(map(sum, zip(antenna_b, antenna_distance)))
        if _grid.isInBounds(*antinode):
            _antinodes.add(antinode)
            _grid.mark(*antinode)
            if _grid.get(*antinode) == ".":
                _grid.set(*antinode, new_value="#")


        while _grid_harmonics.isInBounds(*antinode):
            _antinodes_harmonics.add(antinode)
            _grid_harmonics.mark(*antinode)
            if _grid_harmonics.get(*antinode) == ".":
                _grid_harmonics.set(*antinode, new_value="#")
            antinode = tuple(map(sum, zip(antinode, antenna_distance)))


_grid.print()
print(f"part 1: {len(_antinodes)}")

_grid_harmonics.print()
print(f"part 2: {len(_antinodes_harmonics)}")
