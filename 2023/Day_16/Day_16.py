from operator import add
from copy import deepcopy
_file = open("Input", 'r')
_lines = [line.removesuffix('\n') for line in _file.readlines()]


# _flip_dir = {"N": "S",
#              "E": "W",
#              "S": "N",
#              "W": "E"}

class Glyph:
    def __init__(self, position):
        self.position = position

        self.transfer_map = {"N": "N",
                             "E": "E",
                             "S": "S",
                             "W": "W"}

        self.removal_map = {"N": "S",
                            "E": "W",
                            "S": "N",
                            "W": "E"}

        self.energised = False

    def transfer(self, incomming_direction) -> str or [str] or None:
        outgoing_direction = self.transfer_map.pop(incomming_direction, None)

        if outgoing_direction is not None:
            # remove options
            keys_to_remove = self.removal_map[incomming_direction]
            for key in keys_to_remove:
                self.transfer_map.pop(key, None)

        self.energised = True
        return outgoing_direction

    def print(self):
        if self.energised:
            print("#", end="")
        else:
            print(".", end="")


class Mirror(Glyph):
    def __init__(self, position: (int, int), type: str):
        super().__init__(position)
        self.type = type
        self.energised = False

        if type == "\\":
            self.transfer_map = {"N": "W",
                                 "E": "S",
                                 "S": "E",
                                 "W": "N"}

            self.removal_map = {"N": "E",
                                "E": "N",
                                "S": "W",
                                "W": "S"}
        elif type == "/":
            self.transfer_map = {"N": "E",
                                 "E": "N",
                                 "S": "W",
                                 "W": "S"}

            self.removal_map = {"N": "W",
                                "E": "S",
                                "S": "E",
                                "W": "N"}


class Splitter(Glyph):
    def __init__(self, position: (int, int), type: str):
        super().__init__(position)
        self.type = type
        self.energised = False

        if type == "|":
            self.transfer_map.update({"E": ["N", "S"], "W": ["N", "S"]})

        elif type == "-":
            self.transfer_map.update({"N": ["E", "W"], "S": ["E", "W"]})

        self.removal_map = {"N": ["E", "S", "W"],
                            "E": ["N", "S", "W"],
                            "S": ["N", "E", "W"],
                            "W": ["N", "E", "S"]}


class Board:
    propagate = {"N": (-1, 0),
                 "E": (0, 1),
                 "S": (1, 0),
                 "W": (0, -1)}

    def __init__(self, input):

        self.height = len(input)
        self.width = len(input[0])
        self.glyphs = {}
        self.heads = [((0, -1), "E")]

        self.populate(input)

    def populate(self, input):
        for row_idx, line in enumerate(input):
            for col_idx, char in enumerate(line):
                if char == "\\" or char == "/":
                    self.add((row_idx, col_idx), Mirror((row_idx, col_idx), char))
                elif char == "|" or char == "-":
                    self.add((row_idx, col_idx), Splitter((row_idx, col_idx), char))
                else:
                    self.add((row_idx, col_idx), Glyph((row_idx, col_idx)))

    def add(self, position: (int, int), glyph: Glyph):
        self.glyphs[position] = glyph

    def update(self):
        new_heads = []
        for head in self.heads:
            position, direction = head

            position = tuple(map(add, position, self.propagate[direction]))
            if not self.is_in_bounds(position):
                continue

            direction = self.glyphs[position].transfer(direction)
            if direction is None:
                continue
            elif isinstance(direction, list):
                for dir in direction:
                    new_heads.append((position, dir))
            else:
                new_heads.append((position, direction))

        if len(new_heads) > 0:
            self.heads = new_heads
            return True
        return False

    def print(self):
        for row_idx in range(self.height):
            for col_idx in range(self.width):
                self.glyphs[(row_idx, col_idx)].print()
            print()

    def energy_count(self):
        energy = 0
        for row_idx in range(self.height):
            for col_idx in range(self.width):
                if self.glyphs[(row_idx, col_idx)].energised:
                    energy += 1
        return energy

    def is_in_bounds(self, position):
        row_idx, col_idx = position
        if 0 <= row_idx < self.height and 0 <= col_idx < self.width:
            return True
        else:
            return False


def generate_starting_points(height: int, width: int) -> [((int, int), str)]:
    top_line = [((-1, col_idx), "S") for col_idx in range(width)]
    right_line = [((row_idx, width), "W") for row_idx in range(height)]
    bottom_line = [((height, col_idx), "N") for col_idx in range(width)]
    left_line = [((row_idx, -1), "E") for row_idx in range(width)]

    return top_line + right_line + bottom_line + left_line


max_energised = 0
board = Board(_lines)
starting_points = generate_starting_points(board.width, board.height)
for idx, starting_point in enumerate(starting_points):
    current_board = deepcopy(board)
    current_board.heads = [starting_point]
    while current_board.update():
        pass
    energy_lvl = current_board.energy_count()
    if starting_point == ((0, -1), "E"):
        P1_energy = energy_lvl

    max_energised = max(max_energised, energy_lvl)

    if (idx+1)%10 == 1:
        print(f"{idx+1:3d}/{len(starting_points)}")

print(f"Part 1: {P1_energy}")
print(f"Part 2: {max_energised}")
