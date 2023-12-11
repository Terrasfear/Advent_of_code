class pipe_map:
    def __init__(self, input):
        self.map = [list(
            line.removesuffix('\n').replace("-", "─").replace("|", "│").replace("F", "┌").replace("7", "┐")
            .replace("L", "└").replace("J", "┘")) for line in input]
        self.map_size = (len(self.map), len(self.map[0]))
        self.step_number = 0
        self.step_number_str = "0"
        self.determine_start()

        self.replace(self.starting_position, self.step_number_str)
        self.increment_step()

        test_grid = ((-1, 0, "S"), (1, 0, "N"), (0, -1, "E"), (0, 1, "W"))
        # (change of row index, change of column index, direction you approach from)

        connected_to_start = [(self.starting_position[0] + test[0], self.starting_position[1] + test[1])
                              for test in test_grid
                              if self.is_connected(
                (self.starting_position[0] + test[0], self.starting_position[1] + test[1]), test[2])]
        self.trail_1_position, self.trail_2_position = connected_to_start
        self.trail_1_pipe = self.get(self.trail_1_position)
        self.trail_2_pipe = self.get(self.trail_2_position)

        for pos in connected_to_start:
            self.replace(pos, self.step_number_str)
        self.increment_step()

    def determine_start(self):
        for row, line in enumerate(self.map):
            if "S" in line:
                self.starting_position = (row, line.index("S"))

    def replace(self, position, char: str):
        self.map[position[0]][position[1]] = char

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

    def print(self):
        for row in self.map:
            print("".join(row))

    def print_path_only(self):
        for row in self.map:
            for char in row:
                if char.isdigit():
                    print(char, end="")
                else:
                    print(".")

    def is_connected(self, position, direction) -> bool:
        # test if the pipe at "position" is connected when approached from "direction" (N, E, S, W)
        pipe_type = self.get(position)
        if pipe_type == "." or pipe_type == "":  # not a pipe or out of bounds
            return False
        if pipe_type.isdigit():  # pipe already matched to trail
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
        # trail 1:
        self.trail_1_position = self.find_next_pipe(self.trail_1_position, self.trail_1_pipe)
        self.trail_1_pipe = self.get(self.trail_1_position)
        self.replace(self.trail_1_position, self.step_number_str)

        # trail 2:
        self.trail_2_position = self.find_next_pipe(self.trail_2_position, self.trail_2_pipe)
        if self.trail_2_position == (-1, -1):
            return False
        self.trail_2_pipe = self.get(self.trail_2_position)
        self.replace(self.trail_2_position, self.step_number_str)

        self.increment_step()
        return True

    def find_next_pipe(self, position: (int, int), pipe_type: str) -> (int, int):
        test_grid = self.pipe_type_2_test_grid(pipe_type)

        next_pipe = [(position[0] + test[0], position[1] + test[1])
                     for test in test_grid
                     if not self.get((position[0] + test[0], position[1] + test[1])).isdigit()]

        if len(next_pipe) == 0:
            return -1, -1
        else:
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


_file = open("Input", 'r')
_lines = _file.readlines()

_pipe_map = pipe_map(_lines)
_pipe_map.print()

while _pipe_map.update():
    pass
print()
_pipe_map.print()
print(f"part 1: {_pipe_map.step_number}")
