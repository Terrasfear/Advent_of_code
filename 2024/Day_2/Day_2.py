def is_safe(levels: list[int], damped:bool=False) -> tuple[bool,bool]:
    levelDiffs = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]

    isCorrectIncreasing = [0 < difference <= 3 for difference in levelDiffs]
    isCorrectDecreasing = [-3 <= difference < 0 for difference in levelDiffs]

    if all(isCorrectIncreasing) or all(isCorrectDecreasing):
        return True, True
    elif damped:
        for idx in range(len(levels)):
            secondChance = levels.copy()
            secondChance.pop(idx)
            if is_safe(secondChance)[0]:
                return False, True

        return False, False
    else:
        return False, False


with open("Input", "r") as _file:
    _lines = _file.readlines()

    _countValid = 0
    _countValidDamped = 0

    for line in _lines:
        line = line.removesuffix("\n").split(" ")

        levels = [int(level) for level in line]

        isSafe, isSafeDamped = is_safe(levels, True)
        _countValid += isSafe
        _countValidDamped += isSafeDamped

        if not isSafeDamped:
            print(f"{isSafe}\t{isSafeDamped}\t{levels}")

print(f"Part 1: {_countValid}")
print(f"Part 2: {_countValidDamped}")
