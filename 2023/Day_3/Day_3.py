file = open("input", 'r')
lines = file.readlines()

engine_size = (len(lines), len(lines[0]) - 1)

test_set = [[-1, -1],
            [-1, 0],
            [-1, 1],
            [0, -1],
            [0, 1],
            [1, -1],
            [1, 0],
            [1, 1]]

current_id_str = ""
collecting_numbers = False
number_is_id = False

gears = {}
is_possible_gear = False

id_sum = 0


def test_for_symbol(_line_idx, _char_idx):
    global is_possible_gear
    if _line_idx < 0 or _line_idx >= engine_size[0] or _char_idx < 0 or _char_idx >= engine_size[1]:
        return False
    else:
        try:
            char_to_test = lines[_line_idx][_char_idx]
            if not (char_to_test.isdigit() or char_to_test == "."):
                if char_to_test == "*":  # check for possible gears
                    is_possible_gear = f"{_line_idx}_{_char_idx}"
                return char_to_test
            else:
                return False
        except IndexError:
            return False


for line_idx, line in enumerate(lines):
    for char_idx, char in enumerate(line):
        if not str.isdigit(char):
            if collecting_numbers:  # end of set
                print(f"found number: {current_id_str},\t ID state: {number_is_id}")
                if number_is_id:
                    id_sum += int(current_id_str)
                    number_is_id = False

                    if is_possible_gear:
                        if is_possible_gear not in gears:  # new possible gear
                            gears[is_possible_gear] = [int(current_id_str), 0]
                        elif gears[is_possible_gear][1] == 0:  # this is the second gear part
                            gears[is_possible_gear][1] = int(current_id_str)
                        else:  # same "*" used by > 2 numbers -> not a gear, set both to 0 to have them cancel when multiplying later
                            gears[is_possible_gear] = [0, 0]

                        is_possible_gear = False

                current_id_str = ""
                collecting_numbers = False
            continue

        if str.isdigit(char):
            if not collecting_numbers:  # new set of numbers
                collecting_numbers = True

            current_id_str += char

            if not number_is_id:  # test if it could be a valid id
                id_check = [test_for_symbol(line_idx + test[0], char_idx + test[1]) for test in test_set]
                number_is_id = any(id_check)

print(f"part 1: {id_sum}")

gear_ratio_sum = 0
for gear in gears.values():
    gear_ratio_sum += gear[0] * gear[1]

print(f"part 2: {gear_ratio_sum}")