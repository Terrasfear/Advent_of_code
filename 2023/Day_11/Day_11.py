def manhattan_dist(pos1: (int, int), pos2: (int, int)) -> int:
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def galaxy_distances(galaxies: [(int, int)]) -> int:
    distance_sum = 0
    for galaxy1_idx, galaxy1 in enumerate(galaxies):
        for galaxy2 in galaxies[galaxy1_idx+1:]:
            distance_sum += manhattan_dist(galaxy1, galaxy2)
    return distance_sum


_file = open("Input", 'r')
_lines = [line.removesuffix('\n') for line in _file.readlines()]

_empty_rows = list(range(len(_lines[0])))
_empty_columns = list(range(len(_lines[0])))

_galaxies = []

for row_idx, row in enumerate(_lines):
    for column_idx, char in enumerate(row):
        if char == "#":
            _galaxies.append((row_idx, column_idx))

            try:
                _empty_columns.remove(column_idx)
            except ValueError:
                pass

            try:
                _empty_rows.remove(row_idx)
            except ValueError:
                pass


_galaxies_extended_p1 = []
_galaxies_extended_p2 = []
for galaxy in _galaxies:
    galaxy_row, galaxy_column = galaxy

    empty_rows = sum([1 for row in _empty_rows if row < galaxy_row])
    empty_columns = sum([1 for column in _empty_columns if column < galaxy_column])

    _galaxies_extended_p1.append((galaxy_row + empty_rows, galaxy_column + empty_columns))
    _galaxies_extended_p2.append((galaxy_row + empty_rows*(1e6 - 1), galaxy_column + empty_columns*(1e6 - 1)))
    pass

print(f"part 1: {galaxy_distances(_galaxies_extended_p1)}")
print(f"part 2: {galaxy_distances(_galaxies_extended_p2)}")
