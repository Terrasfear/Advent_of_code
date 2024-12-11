def stone_change(number: str) -> list[str]:
    if number == "0":
        return ["1"]
    if not ((num_digits := len(number)) & 1):
        return [number[:num_digits // 2], str(int(number[num_digits // 2:]))]
    else:
        return [str(2024 * int(number))]


def blink(stone_line: dict[str, int]) -> dict[str, int]:
    new_stone_line = {}
    for stone in stone_line:
        for new_stone in stone_change(stone):
            new_stone_line.update({new_stone: stone_line[stone] + new_stone_line.get(new_stone, 0)})
    return new_stone_line


with open("Input", "r") as _file:
    _line = _file.readlines()[0].removesuffix("\n").split(" ")
    _stone_line = {stone_number: 1 for stone_number in _line}


_num_blinks = 75
_num_blinks_part_1 = 25

_num_blinks_part_1 = min(_num_blinks_part_1, _num_blinks)

for i in range(_num_blinks):
    print(f"{i}/{_num_blinks}")
    _stone_line = blink(_stone_line)
    if i == _num_blinks_part_1 - 1:
        _part_1_answer = sum(_stone_line.values())

print(f"Part 1: {_part_1_answer}")
print(f"Part 2: {sum(_stone_line.values())}")
