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


class TrailPlanner:

    def __init__(self, height_map: Grid_2D, trail_length=10):
        self.height_map = height_map
        self.trail_length = trail_length

        starting_points = [starting_point for starting_point in self.height_map.find("0")]

        self.trails = []
        self.trail_scores_endpoints = []
        self.trail_scores_paths = []
        for starting_point in starting_points:
            if trail := self.trail(starting_point):
                self.trails.append(trail)
                self.trail_scores_endpoints.append(len(set(trail[-1])))
                self.trail_scores_paths.append(len(trail[-1]))
        i = 3

    def trail(self, trail_head: tuple[int, int]):
        return self.walkTrail([[trail_head]])

    def walkTrail(self, trail: list[list[tuple[int, int]]]):
        neighbours = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N E S W
        next_steps = []
        for current_step in trail[-1]:
            possible_steps = [tuple(map(sum, zip(neighbour, current_step))) for neighbour in neighbours]
            possible_steps = [step for step in possible_steps
                              if self.height_map.isInBounds(*step) and
                              self.height_map.get(*step) == str(len(trail))]
            next_steps.extend(possible_steps)

        if not next_steps:
            return False

        trail.append(next_steps)

        if len(trail) == self.trail_length:
            return trail

        return self.walkTrail(trail)

    def print(self):
        for trail in self.trails:
            for step in trail:
                self.height_map.markBatch(step)

        self.height_map.print()


with open("Input", 'r') as _file:
    _lines = _file.readlines()

    _height_map = Grid_2D(_lines)

_trail_planner = TrailPlanner(_height_map)
_trail_planner.print()

print(f"Part 1: {sum(_trail_planner.trail_scores_endpoints)}")
print(f"Part 2: {sum(_trail_planner.trail_scores_paths)}")
