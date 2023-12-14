import numpy as np

_file = open("Input", 'r')
_lines = _file.readlines()
_lines.append("\n")  # for final block detection


class Block:
    block = None

    def add_line(self, line: str):
        # "#" => 1
        # "." => -1
        line_bool = [1 if char == "#" else -1 for char in line.removesuffix("\n")]

        if self.block is None:
            self.block = np.array(line_bool, dtype=np.int8, ndmin=2)
        else:
            self.block = np.append(self.block, np.array(line_bool, dtype=np.int8, ndmin=2), axis=0)

    def summarize(self):

        height, width = self.block.shape

        possible_vertical_mirrors = [set(self.find_possible_mirrors(self.block[row_idx, :])) for row_idx in range(height)]
        possible_horizontal_mirrors = [set(self.find_possible_mirrors(self.block[:, col_idx])) for col_idx in range(width)]

        possible_vertical_mirror_counts = self.count_mirror_locations(possible_vertical_mirrors)
        possible_horizontal_mirror_counts = self.count_mirror_locations(possible_horizontal_mirrors)

        # Part 1

        try:
            P1_value = list(possible_vertical_mirror_counts.keys())[list(possible_vertical_mirror_counts.values()).index(height)] + 1
        except ValueError:
            P1_value = list(possible_horizontal_mirror_counts.keys())[list(possible_horizontal_mirror_counts.values()).index(width)] + 1
            P1_value *= 100

        # Part 2
        if list(possible_vertical_mirror_counts.values()).count(height - 1) == 2:
            raise ("multiple smudges for vertical")

        if list(possible_horizontal_mirror_counts.values()).count(width - 1) == 2:
            raise ("multiple smudges for horizontal")

        P2_value = 0
        try:
            P2_value = list(possible_vertical_mirror_counts.keys())[list(possible_vertical_mirror_counts.values()).index(height - 1)] + 1
        except ValueError:
            P2_value = list(possible_horizontal_mirror_counts.keys())[list(possible_horizontal_mirror_counts.values()).index(width - 1)] + 1
            P2_value *= 100
        return P1_value, P2_value

    def find_possible_mirrors(self, line):
        even_auto_correlations = np.correlate(line, np.flip(line), mode="full")[1::2]
        length_populated_parts = self.non_zero_per_even_correlation_step(len(line))
        mirrors = [idx for idx in range(len(even_auto_correlations)) if even_auto_correlations[idx] == length_populated_parts[idx]]
        return mirrors

    def count_mirror_locations(self, possible_mirrors):
        count_list = {}
        for line in possible_mirrors:
            for mirror in line:
                if mirror in count_list:
                    count_list[mirror] += 1
                else:
                    count_list[mirror] = 1
        return count_list
        # for line in poss

    def non_zero_per_even_correlation_step(self, input_length):
        return [-2 * abs(x - (input_length - 2) / 2) + input_length for x in range(0, input_length - 1)]

    def print(self):
        if self.block is not None:
            print(self.block.astype(int))


current_block = Block()
summary_sum_p1 = 0
summary_sum_p2 = 0
for line in _lines:
    if line == "\n":  # end of block
        mirror_value, clean_mirror_value = current_block.summarize()
        summary_sum_p1 += mirror_value
        summary_sum_p2 += clean_mirror_value
        current_block = Block()
    else:
        current_block.add_line(line)

print(f"Part 1: {summary_sum_p1}")  # 27742
print(f"Part 2: {summary_sum_p2}")
