def decode_line(line) -> tuple[tuple[int, int], tuple[int, int]]:
    starting_position, velocity = line.removesuffix("\n").split(" ")

    starting_position = starting_position.split("=")[1].split(",")
    starting_position = (int(starting_position[0]), int(starting_position[1]))

    velocity = velocity.split("=")[1].split(",")
    velocity = (int(velocity[0]), int(velocity[1]))

    return starting_position, velocity


def quadrant_after_n_steps(chart, start, velocity, steps):
    if steps > chart[0]:
        steps %= chart[0]
    if steps > chart[1]:
        steps %= chart[1]

    quadrant_borders = (chart[0] // 2, chart[1] // 2)

    end = tuple(
        [(start[direction] + velocity[direction] * start[direction]) % chart[direction]
         for direction in range(2)])

    quadrant = ""

    if end[1] < quadrant_borders[1]:
        quadrant += "N"
    elif end[1] > quadrant_borders[1]:
        quadrant += "S"
    else:
        return ""

    if end[0] < quadrant_borders[0]:
        quadrant += "W"
    elif end[0] > quadrant_borders[0]:
        quadrant += "E"
    else:
        return ""

    return quadrant


class RobotMarch:
    def __init__(self, chart):
        self.chart = chart
        self.robot_positions: list[tuple[int, int]] = []
        self.robot_velocities: list[tuple[int, int]] = []
        self.num_robots = 0

    def add_robot(self, position: tuple[int, int], velocity: tuple[int, int]):
        self.robot_positions.append(position)
        self.robot_velocities.append(velocity)
        self.num_robots += 1

    def step(self):
        for robot_idx in range(self.num_robots):
            new_position = list(map(sum, zip(self.robot_positions[robot_idx], self.robot_velocities[robot_idx])))

            if new_position[0] >= self.chart[0]:
                new_position[0] -= self.chart[0]
            elif new_position[0] < 0:
                new_position[0] += self.chart[0]

            if new_position[1] >= self.chart[1]:
                new_position[1] -= self.chart[1]
            elif new_position[1] < 0:
                new_position[1] += self.chart[1]

            self.robot_positions[robot_idx] = tuple(new_position)

    def horizontal_line_detection(self, length=7):
        for y in range(self.chart[1]):
            row = ""
            for x in range(self.chart[0]):
                if (x, y) in self.robot_positions:
                    row += "#"
                else:
                    row += "."

            if row.find("#"*length) > -1:
                return True
        return False

    def print(self):
        for y in range(self.chart[1]):
            for x in range(self.chart[0]):
                if (x, y) in self.robot_positions:
                    print("#", end="")
                else:
                    print(" ", end="")
            print()


_file_name = "Input"
with open(f"{_file_name}", "r") as _file:
    _lines = _file.readlines()

    if _file_name == "Input":
        _chart = (101, 103)
    else:
        _chart = (11, 7)

quadrant_counts = {"NW": 0,
                   "NE": 0,
                   "SW": 0,
                   "SE": 0}

march = RobotMarch(_chart)

for _line in _lines:

    _start, _velocity = decode_line(_line)

    if quadrant := quadrant_after_n_steps(_chart, _start, _velocity, 100):
        quadrant_counts[quadrant] += 1

    march.add_robot(_start, _velocity)

safety_factor = 1
for quadrant_count in quadrant_counts.values():
    safety_factor *= quadrant_count

march.print()

current_step = 0

while True:

    march.step()
    current_step += 1

    if march.horizontal_line_detection():
        print("-" * _chart[0])
        march.print()
        if input(f"step: {current_step}\n") != "y":
            break
    else:
        print(current_step)

print(f"Part 1: {safety_factor}")
print(f"Part 2: {current_step}")
