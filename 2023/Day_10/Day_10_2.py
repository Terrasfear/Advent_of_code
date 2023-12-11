class pipe_map:
    def __init__(self, input):
        self.map = [list(
            line.removesuffix('\n').replace("-", "─", ).replace("|", "│", ).replace("F", "┌", ).replace("7", "┐", ).replace("L", "└", ).replace("J", "┘", )) for line in input]
        self.map_size = (len(self.map), len(self.map[0]))
        self.path_map = [["." for _ in range(self.map_size[1])] for _ in range(self.map_size[0])]
        self.direction_map = [["." for _ in range(self.map_size[1])] for _ in range(self.map_size[0])]
        self.volume_map = [["." for _ in range(self.map_size[1])] for _ in range(self.map_size[0])]
        self.step_number = 0
        self.step_number_str = "0"
        self.determine_start()

        self.trail_head_position = self.find_next_pipe(self.starting_position, "S")
        self.trail_head_type = self.get(self.trail_head_position)
        self.starting_direction = self.determine_direction(self.starting_position, self.trail_head_position)
        self.trail_head_direction = self.determine_exit_direction(self.trail_head_type, self.starting_direction)

        self.add_to_path(self.starting_position, self.step_number_str, self.starting_direction)
        self.increment_step()

        self.add_to_path(self.trail_head_position, self.step_number_str, self.trail_head_direction)
        self.increment_step()

    def determine_start(self):
        for row, line in enumerate(self.map):
            if "S" in line:
                self.starting_position = (row, line.index("S"))

    def add_to_path(self, position, step_nr: str, out_direction: str):
        if out_direction == None:
            print(f"None at stepnr: {step_nr}")

        self.path_map[position[0]][position[1]] = step_nr
        self.direction_map[position[0]][position[1]] = out_direction

    def increment_step(self):
        self.step_number += 1
        self.step_number_str = str(self.step_number)

    def get(self, position) -> str:
        # check out of bounds
        if position[0] < 0 or position[0] >= self.map_size[0]:
            return ""
        if position[1] < 0 or position[1] >= self.map_size[1]:
            return ""

        return str(self.map[position[0]][position[1]])

    def get_direction(self, position) -> str:
        # check out of bounds
        if position[0] < 0 or position[0] >= self.map_size[0]:
            return ""
        if position[1] < 0 or position[1] >= self.map_size[1]:
            return ""

        return str(self.direction_map[position[0]][position[1]])

    def print_map(self):
        for row in self.map:
            print("".join(row))

    def print_path_only(self):
        for row_idx in range(self.map_size[0]):
            for col_idx in range(self.map_size[1]):
                if self.path_map[row_idx][col_idx].isdigit():
                    print(self.map[row_idx][col_idx], end="")
                else:
                    print(".", end="")
            print()

    def print_directions_only(self):
        for row in self.direction_map:
            print("".join(row))

    def print_path_with_infill(self):
        for row_idx in range(self.map_size[0]):
            for col_idx in range(self.map_size[1]):
                if self.path_map[row_idx][col_idx].isdigit():
                    print(self.map[row_idx][col_idx], end="")
                else:
                    print(self.volume_map[row_idx][col_idx], end="")
            print()

    def is_connected(self, position, direction) -> bool:
        if self.is_trail_part(position):
            return False
        # test if the pipe at "position" is connected when approached from "direction" (N, E, S, W)
        pipe_type = self.get(position)
        if pipe_type == "." or pipe_type == "":  # not a pipe or out of bounds
            return False

        if pipe_type == "│" and (direction == "N" or direction == "S"):
            return True
        if pipe_type == "─" and (direction == "E" or direction == "W"):
            return True

        if pipe_type == "┌" and (direction == "S" or direction == "E"):
            return True
        if pipe_type == "┐" and (direction == "S" or direction == "W"):
            return True

        if pipe_type == "└" and (direction == "N" or direction == "E"):
            return True
        if pipe_type == "┘" and (direction == "N" or direction == "W"):
            return True

        return False

    def update(self) -> bool:
        self.trail_head_position = self.find_next_pipe(self.trail_head_position, self.trail_head_type)
        if self.trail_head_position == (-1, -1):
            return False
        self.trail_head_type = self.get(self.trail_head_position)
        self.trail_head_direction = self.determine_exit_direction(self.trail_head_type, self.trail_head_direction)

        self.add_to_path(self.trail_head_position, self.step_number_str, self.trail_head_direction)
        self.increment_step()
        return True

    def find_next_pipe(self, position: (int, int), pipe_type: str) -> (int, int):
        test_grid = self.pipe_type_2_test_grid(pipe_type)

        next_pipe = [(position[0] + test[0], position[1] + test[1])
                     for test in test_grid
                     if not self.is_trail_part((position[0] + test[0], position[1] + test[1]))]

        if len(next_pipe) == 0:
            return -1, -1
        elif pipe_type == "S":
            next_pipe = [pipe for pipe in next_pipe if self.determine_exit_direction(self.get(pipe), self.determine_direction(self.starting_position, pipe)) is not None]

        return next_pipe[0]

    def pipe_type_2_test_grid(self, pipe_type):

        if pipe_type == "S":
            return (1, 0, "S"), (-1, 0, "N"), (0, 1, "E"), (0, -1, "W")

        if pipe_type == "│":
            return (1, 0, "S"), (-1, 0, "N")
        if pipe_type == "─":
            return (0, 1, "E"), (0, -1, "W")

        if pipe_type == "┌":
            return (1, 0, "S"), (0, 1, "E")
        if pipe_type == "┐":
            return (1, 0, "S"), (0, -1, "W")

        if pipe_type == "└":
            return (-1, 0, "N"), (0, 1, "E")
        if pipe_type == "┘":
            return (-1, 0, "N"), (0, -1, "W")

    def determine_direction(self, start_position: (int, int), end_position: (int, int)) -> str:
        if start_position[0] == end_position[0]:  # row doesn't change => E or W
            if start_position[1] > end_position[1]:
                return "W"
            else:
                return "E"
        else:
            if start_position[1] > end_position[1]:
                return "N"
            else:
                return "S"

    def determine_exit_direction(self, pipe_type, starting_direction):
        if pipe_type == "│":
            if starting_direction == "N":
                return "N"
            if starting_direction == "S":
                return "S"

        if pipe_type == "─":
            if starting_direction == "E":
                return "E"
            if starting_direction == "W":
                return "W"

        if pipe_type == "┌":
            if starting_direction == "N":
                return "E"
            if starting_direction == "W":
                return "S"

        if pipe_type == "┐":
            if starting_direction == "N":
                return "W"
            if starting_direction == "E":
                return "S"

        if pipe_type == "└":
            if starting_direction == "S":
                return "E"
            if starting_direction == "W":
                return "N"

        if pipe_type == "┘":
            if starting_direction == "S":
                return "W"
            if starting_direction == "E":
                return "N"

    def is_trail_part(self, position):
        return self.path_map[position[0]][position[1]].isdigit()

    def fill_volume(self, position):
        self.volume_map[position[0]][position[1]] = "█"

    def find_start_pipe(self, trail_head_direction):
        if trail_head_direction == "N":
            if self.starting_direction == "N":
                self.map[self.starting_position[0]][self.starting_position[1]] = "│"
                return
            if self.starting_direction == "E":
                self.map[self.starting_position[0]][self.starting_position[1]] = "┌"
                return
            if self.starting_direction == "W":
                self.map[self.starting_position[0]][self.starting_position[1]] = "┐"
                return

        if trail_head_direction == "E":
            if self.starting_direction == "N":
                self.map[self.starting_position[0]][self.starting_position[1]] = "┘"
                return
            if self.starting_direction == "E":
                self.map[self.starting_position[0]][self.starting_position[1]] = "─"
                return
            if self.starting_direction == "S":
                self.map[self.starting_position[0]][self.starting_position[1]] = "┐"
                return

        if trail_head_direction == "S":
            if self.starting_direction == "E":
                self.map[self.starting_position[0]][self.starting_position[1]] = "└"
                return
            if self.starting_direction == "S":
                self.map[self.starting_position[0]][self.starting_position[1]] = "│"
                return
            if self.starting_direction == "W":
                self.map[self.starting_position[0]][self.starting_position[1]] = "┘"
                return

        if trail_head_direction == "W":
            if self.starting_direction == "N":
                self.map[self.starting_position[0]][self.starting_position[1]] = "└"
                return
            if self.starting_direction == "S":
                self.map[self.starting_position[0]][self.starting_position[1]] = "┌"
                return
            if self.starting_direction == "W":
                self.map[self.starting_position[0]][self.starting_position[1]] = "─"
                return

    def nonzero_rule_value(self, position):
        exit_direction = self.get_direction(position)
        pipe = self.get(position)

        if (pipe == "│" and exit_direction == "S"):
            return -1

        if (pipe == "┌" and exit_direction == "S") or (pipe == "┐" and exit_direction == "S") or (pipe == "└" and exit_direction == "E") or (pipe == "┘" and exit_direction == "W"):
            return -0.5

        if pipe == "─":
            return 0

        if (pipe == "┌" and exit_direction == "E") or (pipe == "┐" and exit_direction == "W") or (pipe == "└" and exit_direction == "N") or (pipe == "┘" and exit_direction == "N"):
            return 0.5

        if (pipe == "│" and exit_direction == "N"):
            return 1


_file = open("Input", 'r')
_lines = _file.readlines()

_pipe_map = pipe_map(_lines)
_pipe_map.print_map()

while _pipe_map.update():
    pass

_pipe_map.find_start_pipe(_pipe_map.trail_head_direction)

_enclosed_tiles = 0
for row_idx, row in enumerate(_pipe_map.direction_map):
    _in_loop = 0
    for col_idx, direction in enumerate(row):
        if direction == ".":
            if _in_loop != 0:
                _enclosed_tiles += 1
                _pipe_map.fill_volume((row_idx, col_idx))
        else:
            _in_loop += _pipe_map.nonzero_rule_value((row_idx, col_idx))


print()
_pipe_map.print_path_only()
print()
_pipe_map.print_directions_only()
print()
_pipe_map.print_path_with_infill()

print(f"Part 2: {_enclosed_tiles}")
