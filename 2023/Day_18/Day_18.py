import matplotlib.pyplot as plt
import numpy as np

_file = open("input", 'r')
_lines = [line.removesuffix('\n') for line in _file.readlines()]

movement = {"L": (-1, 0),
            "R": (1, 0),
            "U": (0, 1),
            "D": (0, -1)}

col2dir = {0: "R", 1: "D", 2: "L", 3: "U"}


def PolyArea(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def translate(colour: str) -> (int, str):
    direction = col2dir[int(colour[-2])]
    distance = int(colour[2:-2], 16)
    return direction, float(distance)


# x+ = rightwards,
# y+ = upwards
x_p1 = [0]
y_p1 = [0]
boarder_points_p1 = 0
x_p2 = [0]
y_p2 = [0]
boarder_points_p2 = 0
for line in _lines:
    direction_p1, distance_p1, colour = line.split(" ")
    distance_p1 = int(distance_p1)

    direction_p2, distance_p2 = translate(colour)

    boarder_points_p1 += distance_p1
    x_p1.append(x_p1[-1] + movement[direction_p1][0] * distance_p1)
    y_p1.append(y_p1[-1] + movement[direction_p1][1] * distance_p1)

    boarder_points_p2 += distance_p2
    x_p2.append(x_p2[-1] + movement[direction_p2][0] * distance_p2)
    y_p2.append(y_p2[-1] + movement[direction_p2][1] * distance_p2)

inner_points_p1 = PolyArea(x_p1, y_p1) - boarder_points_p1 / 2 + 1
print(f"Part 1: {inner_points_p1 + boarder_points_p1}")

inner_points_p2 = PolyArea(x_p2, y_p2) - boarder_points_p2 / 2 + 1
print(f"Part 2: {inner_points_p2 + boarder_points_p2}")

f1 = plt.figure(1)
plt.plot(x_p1, y_p1)

f2 = plt.figure(2)
plt.plot(x_p2, y_p2)

plt.show()
