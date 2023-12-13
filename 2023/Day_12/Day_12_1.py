
from itertools import combinations


def input_row_to_int(input_str: str):
    output = []
    for char in input_str:
        if char == ".":
            output.append(1)
        elif char == "#":
            output.append(-1)
        else:
            output.append(0)
    return output


def generate_possible_configurations(record, row_lenght):
    # based on https://towardsdatascience.com/solving-nonograms-with-120-lines-of-code-a7c6e0f627e4

    num_damaged_groups = len(record)
    num_free_operational_springs = row_lenght - sum(record) - (num_damaged_groups - 1)

    damaged_spring_blocks = [[-1] * damaged_spring_group_length for damaged_spring_group_length in record]

    options = []
    for possible_order in combinations(range(num_damaged_groups + num_free_operational_springs), num_damaged_groups):
        selected = [1] * (num_damaged_groups + num_free_operational_springs)  # opperational row where the free operational springs stay 1, and the indices of the damaged blocks are stored
        damaged_block_idx = 0

        for location in possible_order:
            selected[location] = damaged_block_idx
            damaged_block_idx += -1

        # makes list of damaged blocks (whith a manditory operational spring after) and the opreational springs
        current_option = [damaged_spring_blocks[-val] + [1] if val < 1 else [1] for val in selected]

        # makes it a single list of 1s for coverd squares and -1s for empyt squares
        current_option = [item for sublist in current_option for item in sublist][:-1]  # flattens list and removes last element (which is an overshot -1 for the last block)

        options.append(current_option)
    return options


def match_options_with_known(known_locations, options: [[int]]):

    # given .??..??...?##. changed to [ 1  0  0  1  1  0  0  1  1  1  0 -1 -1  1]
    # try   ..#.#....###.. changed to [ 1  1 -1  1 -1  1  1  1  1 -1 -1 -1  1  1]
    # then element whise product is   [ 1  0  0  1 -1  0  0  1  1 -1  0  1 -1  1]
    # if the attempt is unvalid   min([ 1  0  0  1 -1  0  0  1  1 -1  0  1 -1  1]) == -1

    num_matches = 0
    for option in options:
        match = 1
        for idx in range(len(option)):
            if known_locations[idx] * option[idx] < 0:
                match = 0
                break
        num_matches += match

    return num_matches
# rows_values = [[3, 2, 6], [8, 2]]  # etc.

# row_values = rows_values[0]
# row_lenght = 15

# n_groups = len(row_values)
# n_empty = row_lenght - sum(row_values) - (n_groups - 1)

# blocks = [[1] * x for x in row_values]

# res_opts = []
# for p in combinations(range(n_groups + n_empty), n_groups):
#     # for each filled block and empty square combination
#     selected = [-1] * (n_groups + n_empty) # empty row where an empty square stays -1, and the indices of the blocks are stored
#     ones_idx = 0
#     for val in p:
#         selected[val] = ones_idx
#         ones_idx += 1

#     #makes list of blocks (whith a manditory empyt square after) and the free empty squares
#     res_opt = [blocks[val] + [-1] if val > -1 else [-1] for val in selected]

#     # makes it a single list of 1s for coverd squares and -1s for empyt squares
#     res_opt = [item for sublist in res_opt for item in sublist][:-1] #flattens list and removes last element (which is an overshot -1 for the last block)

#     print(f"{p}\t -> {res_opt}")

# res_opts.append(res_opt)


_file = open("Input", 'r')
_lines = _file.readlines()

_possible_arrangements = 0
for line in _lines:
    known_locations, record = line.removesuffix('\n').split()

    known_locations = input_row_to_int(known_locations)
    record = [int(group) for group in record.split(",")]

    # generate possible options for the record
    options = generate_possible_configurations(record, len(known_locations))
    
    pass

    # check which options match with the known locations
    matching_options = match_options_with_known(known_locations, options)

    _possible_arrangements += matching_options


print(f"part 1: {_possible_arrangements}")
