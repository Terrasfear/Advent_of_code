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


class Robot:
    def __init__(self, grid: Grid_2D):
        self.grid = grid
        self.height = grid.height
        self.width = grid.width

        self.robot = self.grid.find("@")[0]
        self.walls = self.grid.find("#")
        self.boxes = self.grid.find("O")
        self.large_boxes_left = self.grid.find("[")
        self.large_boxes_right = self.grid.find("]")
        self.large_box_move_queue: set[tuple[tuple[int, int], tuple[int, int]]] = set()

    def print(self):
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) in self.walls:
                    print("#", end="")
                elif (row, col) in self.boxes:
                    print("\033[36mO", end="\033[00m")
                elif (row, col) == self.robot:
                    print("\033[31m@", end="\033[00m")
                elif (row, col) in self.large_boxes_left:
                    print("\033[36m[", end="\033[00m")
                elif (row, col) in self.large_boxes_right:
                    print("\033[36m]", end="\033[00m")
                else:
                    print(".", end="")
            print()

    def instruction(self, direction: str):
        if direction == "<":
            self.step((0, -1))
        elif direction == "^":
            self.step((-1, 0))
        elif direction == ">":
            self.step((0, 1))
        elif direction == "v":
            self.step((1, 0))
        else:
            raise Exception(f"Invalid direction: {direction}")

    def locationState(self, location: tuple[int, int]):
        if location in self.walls:
            return 5
        elif location in self.large_boxes_left:
            return 4
        elif location in self.large_boxes_right:
            return 3
        elif location in self.boxes:
            return 2
        elif location == self.robot:
            return 1
        else:
            return 0

    def step(self, direction: tuple[int, int]):
        destination = (self.robot[0] + direction[0], self.robot[1] + direction[1])

        destination_occupation = self.locationState(destination)

        if destination_occupation == 5:
            return
        elif destination_occupation == 2:
            if not self.moveBox(destination, direction):
                return
        elif destination_occupation == 3:
            if not self.moveLargeBox((destination[0], destination[1] - 1), direction):
                return
        elif destination_occupation == 4:
            if not self.moveLargeBox(destination, direction):
                return
        self.robot = destination

    def moveBox(self, box_location: tuple[int, int], direction: tuple[int, int]):
        destination = (box_location[0] + direction[0], box_location[1] + direction[1])
        destination_occupation = self.locationState(destination)

        if destination_occupation == 5:
            return False

        elif destination_occupation == 2:
            if not self.moveBox(destination, direction):
                return False

        self.boxes.remove(box_location)
        self.boxes.append(destination)
        return True

    def moveLargeBox(self, box_location_left: tuple[int, int], direction: tuple[int, int]):
        box_location_right = (box_location_left[0], box_location_left[1] + 1)
        if not box_location_right:
            raise Exception(f"box left{box_location_left} does not have a right counterpart at {box_location_right}")

        if direction[0] == 0:
            return self.moveLargeBoxLR(box_location_left, box_location_right, direction)
        else:
            self.large_box_move_queue.clear()
            if self.moveLargeBoxUD(box_location_left, box_location_right, direction):
                self.moveLargeBoxQueue(direction)
                return True
            else:
                self.large_box_move_queue.clear()
                return False

    def moveLargeBoxLR(self, box_location_left: tuple[int, int], box_location_right: tuple[int, int],
                       direction: tuple[int, int]):
        if direction[1] == 1:  # move right
            destination_occupation = self.locationState((box_location_right[0], box_location_right[1] + 1))

            if destination_occupation == 5:
                return False

            elif destination_occupation == 4:
                if not self.moveLargeBoxLR((box_location_right[0], box_location_right[1] + 1),
                                           (box_location_right[0], box_location_right[1] + 2), direction):
                    return False

        else:  # move left
            destination_occupation = self.locationState((box_location_left[0], box_location_left[1] - 1))

            if destination_occupation == 5:
                return False

            elif destination_occupation == 3:
                if not self.moveLargeBoxLR((box_location_left[0], box_location_left[1] - 2),
                                           (box_location_left[0], box_location_left[1] - 1), direction):
                    return False

        self.large_boxes_left.remove(box_location_left)
        self.large_boxes_left.append((box_location_left[0] + direction[0], box_location_left[1] + direction[1]))

        self.large_boxes_right.remove(box_location_right)
        self.large_boxes_right.append((box_location_right[0] + direction[0], box_location_right[1] + direction[1]))

        return True

    def moveLargeBoxUD(self, box_location_left: tuple[int, int], box_location_right: tuple[int, int],
                       direction: tuple[int, int]):
        destination_left = (box_location_left[0] + direction[0], box_location_left[1])
        destination_right = (box_location_right[0] + direction[0], box_location_right[1])

        destination_occupation_left = self.locationState(destination_left)
        destination_occupation_right = self.locationState(destination_right)

        if destination_occupation_left == 5 or destination_occupation_right == 5:
            return False

        elif destination_occupation_left == 0 and destination_occupation_right == 0:
            pass

        elif destination_occupation_left == 4 and destination_occupation_right == 3:
            if not self.moveLargeBoxUD(destination_left, destination_right, direction):
                return False

        elif destination_occupation_left == 3 and destination_occupation_right == 4:
            if not all(
                    [self.moveLargeBoxUD((destination_left[0], destination_left[1] - 1), destination_left, direction),
                     self.moveLargeBoxUD(destination_right, (destination_right[0], destination_right[1] + 1), direction)]):
                return False

        elif destination_occupation_left == 3 and destination_occupation_right == 0:
            if not self.moveLargeBoxUD((destination_left[0], destination_left[1] - 1), destination_left, direction):
                return False

        elif destination_occupation_left == 0 and destination_occupation_right == 4:
            if not self.moveLargeBoxUD(destination_right, (destination_right[0], destination_right[1] + 1), direction):
                return False

        self.large_box_move_queue.add((box_location_left, box_location_right))
        return True

    def moveLargeBoxQueue(self, direction):
        for large_box_left, large_box_right in self.large_box_move_queue:
            self.large_boxes_left.remove(large_box_left)
            self.large_boxes_left.append((large_box_left[0] + direction[0], large_box_left[1] + direction[1]))

            self.large_boxes_right.remove(large_box_right)
            self.large_boxes_right.append((large_box_right[0] + direction[0], large_box_right[1] + direction[1]))

    def gps(self):
        return sum([100 * box[0] + box[1] for box in self.boxes]) + \
               sum([100 * box[0] + box[1] for box in self.large_boxes_left])


with open("Input", "r") as _file:
    _lines = _file.readlines()
    _map_end = _lines.index("\n")

    _wide_lines = []
    for line in _lines[0: _map_end]:
        wide_line = ""
        for char in line.removesuffix("\n"):
            if char == "O":
                wide_line += "[]"
            elif char == "@":
                wide_line += "@."
            else:
                wide_line += char * 2
        _wide_lines.append(wide_line)

    _robot1 = Robot(Grid_2D(_lines[0: _map_end]))
    _robot2 = Robot(Grid_2D(_wide_lines))

for instruction_line in _lines[_map_end + 1:]:
    for instruction in instruction_line.removesuffix("\n"):
        _robot1.instruction(instruction)
        _robot2.instruction(instruction)


_robot1.print()
print()
print(f"Part 1: {_robot1.gps()}")

_robot2.print()
print()
print(f"Part 2: {_robot2.gps()}")
