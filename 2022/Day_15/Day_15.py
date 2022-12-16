import re

import numpy as np

file = open("Input", 'r')
lines = file.readlines()

# class Sensor:
#
#     def __init__(self, sx, sy, bx, by):
#         self.Sensor_location = tuple([sx, sy])
#         self.Beacon_location = tuple([bx, by])
#         self.distance = abs(sx - bx) + abs(sy - by)
#
#     def is_within_range(self, locx, locy):
#         return self.distance <= abs(self.Sensor_location[0] - locx) + abs(self.Sensor_location[1] - locy)

sensors = np.zeros((len(lines), 5))

for i, line in enumerate(lines):
    parse = re.search('Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)

    for j in range(4):
        sensors[i, j] = int(parse.group(j + 1))  # [sensor x, sensor y, beacon x, beacon y, distance]

    sensors[i, 4] = abs(sensors[i, 0] - sensors[i, 2]) + abs(sensors[i, 1] - sensors[i, 3])

xlim = tuple([int(np.append(sensors[:, 0] - sensors[:,4], sensors[:, 2]).min()),
              int(np.append(sensors[:, 0] + sensors[:,4], sensors[:, 2]).max())])
ylim = tuple([int(np.append(sensors[:, 1] - sensors[:,4], sensors[:, 3]).min()),
              int(np.append(sensors[:, 1] + sensors[:,4], sensors[:, 3]).max())])

coverage_counter = 0
test_y = 2000000

test_y_sensors = sensors[~(abs(sensors[:,1] - test_y) > sensors[:,4])]

for test_x in range(xlim[0], xlim[1] + 1):
    test_x_sensors = test_y_sensors[~(abs(test_y_sensors[:, 0] - test_x) > test_y_sensors[:, 4])]

    if (abs(sensors[:, 0] - test_x) + abs(sensors[:, 1] - test_y) <= sensors[:, 4]).any():  # location within range
        if not np.logical_and(sensors[:, 2] == test_x, sensors[:, 3] == test_y).any():      # ... but not a beacon
            coverage_counter += 1
    pass

print(f"{coverage_counter=}")

test_area = 20
found = False
for test_y in range(test_area+1):
    test_y_sensors = sensors[~(abs(sensors[:, 1] - test_y) > sensors[:, 4])]
    for test_x in range(test_area+1):
        test_x_sensors = test_y_sensors[~(abs(test_y_sensors[:, 0] - test_x) > test_y_sensors[:, 4])]
        if not (abs(sensors[:, 0] - test_x) + abs(sensors[:, 1] - test_y) <= sensors[:, 4]).any():  # not within any range
            found = True
            break
    if found:
        break

print(f"location: ({test_x},{test_y})\nTuning frequency: {test_x*4000000+test_y}")


