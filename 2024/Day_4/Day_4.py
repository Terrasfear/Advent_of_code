class Grid_2D:
    def __init__(self, lines):
        self.grid = {(row_idx, column_idx): {"value": char, "print": char}
                     for row_idx, row in enumerate(lines) for column_idx, char in enumerate(row.removesuffix("\n"))}

        self.height = len(lines)
        self.width = len(lines[0].removesuffix("\n"))

    def print(self):
        for row_idx in range(self.height):
            for column_idx in range(self.width):
                print(self.grid[(row_idx, column_idx)]["print"], end="")
            print()

    def get(self, row_idx, column_idx):
        if 0 <= row_idx < self.height and 0 <= column_idx < self.width:
            return self.grid[(row_idx, column_idx)]["value"]
        else:
            return None

    def find(self, char):
        found = []
        for point in self.grid:
            if self.grid[point]["value"] == char:
                found.append(point)
        return found

    def mark(self, row_idx, column_idx, unmark=False):
        if 0 <= row_idx < self.height and 0 <= column_idx < self.width:
            char = self.get(row_idx, column_idx)
            if not unmark:
                self.grid[(row_idx, column_idx)]["print"] = f"\033[91m{char}\033[00m"
            else:
                self.grid[(row_idx, column_idx)]["print"] = f"{char}"
        else:
            raise Exception(f"({row_idx},{column_idx}) out of bounds")

    def markBatch(self, points: list[tuple[int, int]]):
        for point in points:
            self.mark(point[0], point[1])


class wordFinder:
    class searchEntry:
        def __init__(self, word: str, starting_position: tuple[int, int], direction: tuple[int, int]):
            self.word = word
            self.char_positions: list[tuple[int, int]] = [starting_position]
            self.direction: tuple[int, int] = direction

        def next_position(self) -> tuple[int, int]:
            return tuple(map(sum, zip(self.char_positions[-1], self.direction)))

        def next_char(self) -> str:
            return self.word[len(self.char_positions)] if len(self.char_positions) < len(self.word) else None

        def add_next(self):
            self.char_positions.append(self.next_position())

    def __init__(self, word: str, grid: Grid_2D):
        self.grid = grid
        self.word = word.upper()
        self.directions = [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1), (0, 1),
                           (1, -1), (1, 0), (1, 1)]

        self.found_words: list[wordFinder.searchEntry] = []
        self.find_words()

    def find_words(self):
        starting_points = self.grid.find(self.word[0])

        entry_list = [wordFinder.searchEntry(self.word, starting_point, direction)
                      for starting_point in starting_points
                      for direction in self.directions]

        for entry in entry_list:
            self.grid.mark(*entry.char_positions[0])
            while True:

                if entry.next_char() is None:
                    self.found_words.append(entry)
                    break

                char_at_next_position = self.grid.get(*entry.next_position())
                if char_at_next_position == entry.next_char():
                    entry.add_next()
                else:
                    break

        # mark entries
        for entry in self.found_words:
            self.grid.markBatch(entry.char_positions)


class crossWordFinder:
    def __init__(self, word: str, grid: Grid_2D):
        if not len(word) == 3:
            raise ValueError("can only handle 3 letter words")

        self.grid = grid
        self.word = word.upper()
        self.kernels = [{(-1, -1): 0, (-1, 1): 2,
                         (0, 0): 1,
                         (1, -1): 0, (1, 1): 2},

                        {(-1, -1): 2, (-1, 1): 2,
                         (0, 0): 1,
                         (1, -1): 0, (1, 1): 0},

                        {(-1, -1): 0, (-1, 1): 0,
                         (0, 0): 1,
                         (1, -1): 2, (1, 1): 2},

                        {(-1, -1): 2, (-1, 1): 0,
                         (0, 0): 1,
                         (1, -1): 2, (1, 1): 0}]

        for kernel in self.kernels:
            for key in kernel:
                kernel[key] = self.word[kernel[key]]

        self.num_found_words = 0
        self.find_words()

    def find_words(self):
        starting_points = self.grid.find(self.word[1])

        for starting_point in starting_points:
            for kernel in self.kernels:
                cross_word_found = True
                for position in kernel:
                    if position == (0,0):
                        continue
                    if self.grid.get(*tuple(map(sum, zip(starting_point, position)))) != kernel[position]:
                        cross_word_found = False
                        break

                if cross_word_found:
                    self.num_found_words += 1
                    for position in kernel:
                        self.grid.mark(*tuple(map(sum, zip(starting_point, position))))
                    break

with open("Input", "r") as _file:
    _lines = _file.readlines()

    _grid1 = Grid_2D(_lines)
    _grid2 = Grid_2D(_lines)

_word_finder1 = wordFinder("XMAS", _grid1)
_grid1.print()

print(f"Part 1: {len(_word_finder1.found_words)}")

_word_finder2 = crossWordFinder("MAS", _grid2)
_grid2.print()

print(f"Part 2: {_word_finder2.num_found_words}")
