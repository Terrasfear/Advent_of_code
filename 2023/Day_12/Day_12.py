from functools import cache

_file = open("Input", 'r')
_lines = [line.removesuffix("\n") for line in _file.readlines()]


@cache
def isvalid(spring_row, group_length):
    # determines if the inputted row could house a group of length len(spring_row)-1
    # therefore the last character must be a "." or "?" and no "." may be present in the preceding characters
    if len(spring_row) == group_length:
        if not any([True for spring in spring_row if spring == "."]):
            return True
    elif len(spring_row) == group_length + 1:
        if spring_row[-1] != "#" and not any([True for spring in spring_row[:-1] if spring == "."]):
            return True
    return False


@cache
def find_options(spring_row: str, record: tuple[int]) -> int:
    # invalid options
    if len(spring_row) < sum(record) + len(record) - 1:
        return 0
    # valid options (record is empty and there are no "#" left)
    if not record:
        if "#" not in spring_row:
            return 1
        else:
            return 0

    # case 1, "." as first character
    #   => strip "."
    if spring_row[0] == ".":
        return find_options(spring_row.removeprefix("."), record)

    # case 2, "?" as first character
    #   => replace with "#"; and
    #   => replace with "." (which would then be stripped, so just work with stripping "?"
    if spring_row[0] == "?":
        return find_options(spring_row.replace("?", "#", 1), record) + find_options(spring_row.removeprefix("?"),
                                                                                    record)

    # case 3, "#" as first character
    # see if the first record would fit (i.e. for length of record, no ".", and at length of record +1 no "#")
    #   => if not, this is invalid => return 0
    #   => if yes, strip first len of record + 1 chars and first record
    if spring_row[0] == "#":
        if isvalid(spring_row[:record[0] + 1], record[0]):
            return find_options(spring_row[record[0] + 1:], record[1:])
        else:
            return 0


total_options_P1 = 0
for line in _lines:
    _spring_row, _record = line.split(" ")
    _record = [int(group_length) for group_length in _record.split(",")]

    line_options = find_options(_spring_row, tuple(_record))
    total_options_P1 += line_options

print(f"Part 1: {total_options_P1}")

total_options_P2 = 0
i = 0
num_lines = len(_lines)
for line in _lines:
    _spring_row, _record = line.split(" ")
    _spring_row = "?".join([_spring_row] * 5)

    _record = [int(group_length) for group_length in _record.split(",")]
    _record = _record * 5

    line_options = find_options(_spring_row, tuple(_record))
    total_options_P2 += line_options

    i += 1
    print(f"{i}/{num_lines}")

print(f"Part 2: {total_options_P2}")
