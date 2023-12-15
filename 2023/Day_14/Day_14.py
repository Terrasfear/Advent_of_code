import copy
from timeit import default_timer as timer
from datetime import timedelta

import matplotlib.pyplot as plt

_file = open("Input", 'r')
_lines = _file.readlines()

class print_loading_bar:
    def __init__(self, bar_max, num_blocks:int):
        self.resolution = num_blocks/bar_max
        self.num_blocks = num_blocks
        self.start_time = timer()

    def print(self, level):
        lvl_blocks = int(self.resolution * level)

        print("|" + "#"*lvl_blocks + " "*(self.num_blocks-lvl_blocks) + f"|\t{timedelta(seconds=int(timer()-self.start_time))}")


class Rock_line:

    def __init__(self, height, width):
        self.rows = [[] for _ in range(height)]
        self.cols = [[] for _ in range(width)]

    def add(self, row: int, col: int):
        self.rows[row].append(col)
        self.cols[col].append(row)

    def remove(self, row: int, col: int):
        self.rows[row].remove(col)
        self.cols[col].remove(row)

    def remove_from_col(self, rows: [int], col: int):
        for row in rows:
            self.remove(row, col)

    def remove_from_row(self, row: int, cols: [int]):
        for col in cols:
            self.remove(row, col)


class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.cubes = Rock_line(height, width)
        self.rounds = Rock_line(height, width)

    def add_cube(self, row, col):
        self.cubes.add(row,col)

    def remove_cube(self, row, col):
        self.cubes.remove(row, col)

    def add_round(self,row,col):
        self.rounds.add(row, col)

    def remove_round(self, row, col):
        self.rounds.remove(row, col)

    def compute_load(self):
        arm = self.height
        load = 0
        for row in self.rounds.rows:
            load += arm * len(row)
            arm -= 1

        return load

    def cycle(self):
        self.north()
        self.west()
        self.south()
        self.east()

    def north(self):
        for col_idx in range(self.width):
            cubes = [-1] + sorted(self.cubes.cols[col_idx]) + [self.height]
            rounds = sorted(self.rounds.cols[col_idx])

            for idx in range(len(cubes)-1):
                if cubes[idx]+1 == cubes[idx+1]:
                    continue

                rounds_to_move = [round_ for round_ in rounds if cubes[idx] < round_ < cubes[idx + 1]]
                self.rounds.remove_from_col(rounds_to_move, col_idx)

                for round_ in range(len(rounds_to_move)):
                    self.add_round(cubes[idx]+1+round_, col_idx)

    def east(self):
        for row_idx in range(self.height):
            cubes = [self.width] + sorted(self.cubes.rows[row_idx], reverse=True) + [-1]
            rounds = sorted(self.rounds.rows[row_idx])

            for idx in range(len(cubes)-1):
                if cubes[idx]-1 == cubes[idx+1]:
                    continue

                rounds_to_move = [round_ for round_ in rounds if cubes[idx] > round_ > cubes[idx + 1]]
                self.rounds.remove_from_row(row_idx, rounds_to_move)

                for round_ in range(len(rounds_to_move)):
                    self.add_round(row_idx, cubes[idx]-1-round_)

    def south(self):
        for col_idx in range(self.width):
            cubes = [self.height] + sorted(self.cubes.cols[col_idx], reverse=True) + [-1]
            rounds = sorted(self.rounds.cols[col_idx])

            for idx in range(len(cubes)-1):
                if cubes[idx]-1 == cubes[idx+1]:
                    continue

                rounds_to_move = [round_ for round_ in rounds if cubes[idx] > round_ > cubes[idx + 1]]
                self.rounds.remove_from_col(rounds_to_move, col_idx)

                for round_ in range(len(rounds_to_move)):
                    self.add_round(cubes[idx]-1-round_, col_idx)

    def west(self):
        for row_idx in range(self.height):
            cubes = [-1] + sorted(self.cubes.rows[row_idx]) + [self.width]
            rounds = sorted(self.rounds.rows[row_idx])

            for idx in range(len(cubes)-1):
                if cubes[idx]+1 == cubes[idx+1]:
                    continue

                rounds_to_move = [round_ for round_ in rounds if cubes[idx] < round_ < cubes[idx + 1]]
                self.rounds.remove_from_row(row_idx, rounds_to_move)

                for round_ in range(len(rounds_to_move)):
                    self.add_round(row_idx, cubes[idx]+1+round_)
    def print(self):
        for row_idx in range(self.height):
            row = ["." for _ in range(self.width)]
            for cube in self.cubes.rows[row_idx]:
                row[cube] = "#"
            for round in self.rounds.rows[row_idx]:
                row[round] = "O"
            print("".join(row))


_board_P1 = Board(len(_lines), len(_lines[0])-1)

for line_idx, line in enumerate(_lines):
    for char_idx, char in enumerate(line.removesuffix('\n')):
        if char == "#":
            _board_P1.add_cube(line_idx, char_idx)
        elif char == "O":
            _board_P1.add_round(line_idx, char_idx)

_board_P2 = copy.deepcopy(_board_P1)

_board_P1.north()

_target_cycles = 1e9
_cycles = 150
_P2_loads = []

_bar = print_loading_bar(_cycles,100)
for i in range(_cycles):
    _board_P2.cycle()
    _P2_loads.append(_board_P2.compute_load())
    _bar.print(i+1)


plt.plot(_P2_loads)
plt.title("now human, time to do your part! find two points which are 1 cycle apart, note them down, close the figure and fill them in in the terminal", wrap=True)

plt.show()


_cyclic_1 = int(input("first index of period:"))
_cyclic_2 = int(input("index whole number of periods away:"))
_period = (_cyclic_2 - _cyclic_1)
_highest_idx_below_target_with_value_of_cyclic_1 = _cyclic_1 + _period * ((_target_cycles-_cyclic_1)//_period)
_idx_offset = _target_cycles - _highest_idx_below_target_with_value_of_cyclic_1
_equal_value_as_target = _P2_loads[int(_cyclic_1 + _idx_offset - 1)]  # -1 for zero indexing

print(f"Part 1: {_board_P1.compute_load()}")
print(f"Part 2: {_equal_value_as_target}")


plt.show()