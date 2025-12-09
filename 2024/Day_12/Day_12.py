class Grid_2D:
    def __init__(self, lines):
        self.grid = {(row_idx, column_idx): {"value": char, "print": "", "misc": ""}
                     for row_idx, row in enumerate(lines) for column_idx, char in enumerate(row.removesuffix("\n"))}

        self.height = len(lines)
        self.width = len(lines[0].removesuffix("\n"))

    def print(self):
        for row_idx in range(self.height):
            for column_idx in range(self.width):
                cell = self.grid[(row_idx, column_idx)]
                print(cell["print"] + cell["value"][-1], end="\033[00m")
            print()

    def get(self, row_idx, column_idx):
        if self.isInBounds(row_idx, column_idx):
            return self.grid[(row_idx, column_idx)]["value"]
        else:
            return None

    def set(self, row_idx: int, column_idx: int, new_value, reset_mark: bool = False, field="value", append=False):
        if self.isInBounds(row_idx, column_idx):
            entry = self.grid[(row_idx, column_idx)]

            if append:
                entry[field] += new_value
            else:
                entry[field] = new_value

            if reset_mark:
                entry["print"] = ""
        else:
            raise Exception(f"({row_idx},{column_idx}) out of bounds")

    def setBatch(self, points: list[tuple[int, int]], new_value, reset_mark=False, field="value", append=False):
        for point in points:
            self.set(*point, new_value, reset_mark, field, append)

    def setLine(self, start: tuple[int, int], end: tuple[int, int], new_value, reset_mark=False, field="value",
                append=False):
        if start[0] == end[0]:
            points = [(start[0], column) for column in range(min(start[1], end[1]), max(start[1], end[1]) + 1)]
        elif start[1] == end[1]:
            points = [(row, start[1]) for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1)]
        else:
            raise Exception("points not in a cardinal direction")

        self.setBatch(points, new_value, reset_mark, field, append)

    def find(self, char, field="value"):
        return [point for point in self.grid if char in self.grid[point][field]]

    def findInLine(self, char, start, end, field="value"):
        if start[0] == end[0]:
            points = [(start[0], column) for column in range(min(start[1], end[1]), max(start[1], end[1]) + 1)]
        elif start[1] == end[1]:
            points = [(row, start[1]) for row in range(min(start[0], end[0]), max(start[0], end[0]) + 1)]
        else:
            raise Exception("points not in a cardinal direction")

        return [point for point in points if char in self.grid[point][field]]

    def mark(self, row_idx, column_idx, mark: int = 1):
        if self.isInBounds(row_idx, column_idx):
            if 1 <= mark <= 6:  # red, green, yellow, blue, magenta, cyan
                self.grid[(row_idx, column_idx)]["print"] = f"\033[3{mark}m"
            else:
                self.grid[(row_idx, column_idx)]["print"] = ""
        else:
            raise Exception(f"({row_idx},{column_idx}) out of bounds")

    def markBatch(self, points: list[tuple[int, int]], mark: int = 1):
        for point in points:
            self.mark(point[0], point[1], mark)

    def isInBounds(self, row_idx, column_idx):
        return 0 <= row_idx < self.height and 0 <= column_idx < self.width


class Region:
    def __init__(self, plant_type: str):
        self.plant_type = _plant_type
        self.plants = list()
        self.sides_per_plant = dict()
        self.unexplored_plants = list()
        self.perimeter = 0
        self.area = 0
        self.sides = 0

    def __str__(self):
        return f"Plant type: {self.plant_type},\n" \
               f"\tarea: {self.area}, \n" \
               f"\tperimeter: {self.perimeter}, perimeter price: {self.perimeter_price()}\n" \
               f"\tsides: {self.sides}, side price: {self.side_price()}"

    def add_plant(self, plant: tuple[int, int]):
        if plant not in self.plants:
            self.plants.append(plant)
            self.unexplored_plants.append(plant)
            self.area += 1
            self.sides_per_plant[plant] = []

    def perimeter_price(self):
        return self.perimeter * self.area

    def side_price(self):
        return self.sides * self.area


with open("Input", "r") as _file:
    _lines = _file.readlines()

    _plant_types = sorted({plant for line in _lines for plant in line.removesuffix("\n")})
    _garden = Grid_2D(_lines)

NEIGHBOURS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N E S W
NEIGHBOUR_ORDER = ["N", "E", "S", "W"]

_regions = []
for _plant_type in _plant_types:

    _plants_of_type = _garden.find(_plant_type)
    _ungrouped_plants_of_type = _plants_of_type.copy()

    while _ungrouped_plants_of_type:
        _current_plant = _ungrouped_plants_of_type.pop()

        _new_region = Region(_plant_type)

        _new_region.add_plant(_current_plant)

        while _new_region.unexplored_plants:
            _current_plant = _new_region.unexplored_plants.pop()

            _neighbours = [tuple(map(sum, zip(_current_plant, neighbour))) for neighbour in NEIGHBOURS]
            _region_mates = []
            for i, neighbour in enumerate(_neighbours):
                if neighbour in _plants_of_type:
                    _region_mates.append(neighbour)
                else:
                    _new_region.perimeter += 1
                    _new_region.sides_per_plant[_current_plant].append(NEIGHBOUR_ORDER[i])

            _current_plant_sides = _new_region.sides_per_plant[_current_plant].copy()

            _sides_seen = set()
            for region_mate in _region_mates:
                if region_mate not in _new_region.plants:
                    _new_region.add_plant(region_mate)
                    _ungrouped_plants_of_type.remove(region_mate)
                else:
                    _mates_sides = _new_region.sides_per_plant[region_mate]
                    for side in _mates_sides:
                        if side in _sides_seen:  # edge case where we close a loop on a side
                            _new_region.sides -= 1
                        if side in _current_plant_sides:
                            _sides_seen.update(side)
                            _current_plant_sides.remove(side)

            _new_region.sides += len(_current_plant_sides)

        _regions.append(_new_region)

_perimeter_price = 0
_side_price = 0
for i, region in enumerate(_regions):
    _garden.markBatch(region.plants, i % 6 + 1)
    # print(region)
    _perimeter_price += region.perimeter_price()
    _side_price += region.side_price()

_garden.print()

print(f"Part 1: {_perimeter_price}")
print(f"Part 2: {_side_price}")
