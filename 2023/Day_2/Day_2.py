
def Determine_highest_pulls(line_):
    line_ = str.removesuffix(line_, "\n")
    # strip "Game #: "
    game = str.split(str.split(line_, ": ", 1)[1], "; ")

    max_values = {"red": 0, "blue": 0, "green": 0}
    for pull in game:
        cubes = str.split(pull, ", ")
        for cube in cubes:
            collection = str.split(cube)
            max_values[collection[1]] = max(int(collection[0]), max_values[collection[1]])

        pass
    return max_values


def is_valid_game(game_, condition_):
    for colour in game_:
        if game_[colour] > condition_[colour]:
            return False
    return True


file = open("input", 'r')
lines = file.readlines()


condition = {"red": 12, "green": 13, "blue": 14}

sum_valid_indices = 0
sum_game_powers = 0
for idx, line in enumerate(lines):
    game = Determine_highest_pulls(line)
    game_power = game['red']*game['green']*game['blue']

    if is_valid_game(game, condition):
        sum_valid_indices += 1 + idx
    sum_game_powers += game_power

print(f"part 1: {sum_valid_indices}")
print(f"part 2: {sum_game_powers}")
