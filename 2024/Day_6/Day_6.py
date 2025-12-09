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
        if 0 <= row_idx < self.height and 0 <= column_idx < self.width:
            return self.grid[(row_idx, column_idx)]["value"]
        else:
            return None

    def set(self, row_idx: int, column_idx: int, new_value, reset_mark: bool = False, field="value", append=False):
        if 0 <= row_idx < self.height and 0 <= column_idx < self.width:
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
        if 0 <= row_idx < self.height and 0 <= column_idx < self.width:
            if not unmark:
                self.grid[(row_idx, column_idx)]["print"] = f"\033[91m"
            else:
                self.grid[(row_idx, column_idx)]["print"] = ""
        else:
            raise Exception(f"({row_idx},{column_idx}) out of bounds")

    def markBatch(self, points: list[tuple[int, int]]):
        for point in points:
            self.mark(point[0], point[1])


class Patrol:
    class Guard:
        def __init__(self, position: tuple[int, int], direction: str):
            self.position: tuple[int, int] = position
            self.direction = direction

        def turnRight(self):
            self.direction = self.directionToTheRight()

        def directionToTheRight(self):
            if self.direction == "^":
                return ">"
            elif self.direction == ">":
                return "v"
            elif self.direction == "v":
                return "<"
            elif self.direction == "<":
                return "^"
            else:
                raise ValueError(f"invalid direction: {self.direction}")

        def directioBehind(self):
            if self.direction == "^":
                return "v"
            elif self.direction == ">":
                return "<"
            elif self.direction == "v":
                return "^"
            elif self.direction == "<":
                return ">"
            else:
                raise ValueError(f"invalid direction: {self.direction}")

        def moveUpto(self, obstacle_to_walk_against):
            if self.direction == "^":
                self.position = (obstacle_to_walk_against[0] + 1, self.position[1])
            elif self.direction == ">":
                self.position = (self.position[0], obstacle_to_walk_against[1] - 1)
            elif self.direction == "v":
                self.position = (obstacle_to_walk_against[0] - 1, self.position[1])
            elif self.direction == "<":
                self.position = (self.position[0], obstacle_to_walk_against[1] + 1)
            else:
                raise ValueError(f"invallid direction: {self.direction}")

        def moveOut(self, height, width):
            if self.direction == "^":
                self.position = (0, self.position[1])
            elif self.direction == ">":
                self.position = (self.position[0], width - 1)
            elif self.direction == "v":
                self.position = (height - 1, self.position[1])
            elif self.direction == "<":
                self.position = (self.position[0], 0)
            else:
                raise ValueError(f"invallid direction: {self.direction}")

    def __init__(self, lines):
        self.grid = Grid_2D(lines)
        self.options_grid = Grid_2D(lines)
        self.obstacles = self.grid.find("#")

        starting_direction = "^"
        self.guard = Patrol.Guard(self.grid.find(starting_direction)[0], starting_direction)

        self.grid.set(*self.guard.position, new_value=self.guard.direction)
        self.grid.mark(*self.guard.position)

        self.patrol_finished = False
        self.loop_detected = False

    def patrol(self):
        while True:
            self.step()
            if self.patrol_finished:
                return True
            if self.loop_detected:
                return False

    def step(self):
        next_obstacle = self.findNextObstacle(self.guard.direction)
        old_position = self.guard.position
        if not next_obstacle == (-1, -1):
            self.guard.moveUpto(next_obstacle)
            self.grid.mark(*next_obstacle)
        else:
            self.guard.moveOut(self.grid.height, self.grid.width)
            self.patrol_finished = True

        if len(self.grid.findInLine(self.guard.direction, old_position, self.guard.position, field="misc")) > 1:
            self.loop_detected = True

        self.grid.setLine(old_position, self.guard.position, self.guard.direction)
        self.grid.setLine(old_position, self.guard.position, self.guard.direction, field="misc", append=True)

        self.guard.turnRight()

    def findNextObstacle(self, direction) -> tuple[int, int]:  # returns (-1,-1) if there is none
        if direction == "^":
            obstacles_in_line_row_coord = [obstacle[0] for obstacle in self.obstacles
                                           if obstacle[0] < self.guard.position[0]
                                           and obstacle[1] == self.guard.position[1]]
            if obstacles_in_line_row_coord:
                return max(obstacles_in_line_row_coord), self.guard.position[1]

        elif direction == ">":
            obstacles_in_line_row_coord = [obstacle[1] for obstacle in self.obstacles
                                           if obstacle[0] == self.guard.position[0]
                                           and obstacle[1] > self.guard.position[1]]
            if obstacles_in_line_row_coord:
                return self.guard.position[0], min(obstacles_in_line_row_coord)

        elif direction == "v":
            obstacles_in_line_row_coord = [obstacle[0] for obstacle in self.obstacles
                                           if obstacle[0] > self.guard.position[0]
                                           and obstacle[1] == self.guard.position[1]]
            if obstacles_in_line_row_coord:
                return min(obstacles_in_line_row_coord), self.guard.position[1]

        elif direction == "<":
            obstacles_in_line_row_coord = [obstacle[1] for obstacle in self.obstacles
                                           if obstacle[0] == self.guard.position[0]
                                           and obstacle[1] < self.guard.position[1]]
            if obstacles_in_line_row_coord:
                return self.guard.position[0], max(obstacles_in_line_row_coord)

        else:
            raise ValueError(f"invalid direction: {direction}")

        return -1, -1

    def length(self):
        return self.grid.height * self.grid.width \
               - len(self.grid.find(".")) - len(self.grid.find("#"))

    def addObstacle(self, position):
        self.grid.set(*position, new_value="o")
        self.obstacles.append(position)


with open("Input", "r") as _file:
    _lines = _file.readlines()

    _patrol = Patrol(_lines)

_starting_point = _patrol.guard.position
_patrol.patrol()
_patrol.grid.print()
print(f"Part 1:{_patrol.length()}")

_obstacle_options = set()
_obstacle_options.update(_patrol.grid.find("^"))
_obstacle_options.update(_patrol.grid.find(">"))
_obstacle_options.update(_patrol.grid.find("v"))
_obstacle_options.update(_patrol.grid.find("<"))
_obstacle_options.remove(_starting_point)

_successful_blocks = 0
for idx, obstacle_option in enumerate(_obstacle_options):

    if idx % 100 == 0:
        print(f"{idx}/{len(_obstacle_options)}")

    blocking_patrol = Patrol(_lines)
    blocking_patrol.addObstacle(obstacle_option)
    if not blocking_patrol.patrol():
        _successful_blocks += 1

print(f"Part 2:{_successful_blocks}")
