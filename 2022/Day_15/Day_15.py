import re

import numpy as np

file = open("Input", 'r')
lines = file.readlines()


def gen_test_points(sx, sy, radius: int):
    diamond = []
    for l in range(radius+1):
        diamond.append(tuple([sx              + l,   # line 1
                              sy + (radius+1) - l]))
        diamond.append(tuple([sx + (radius+1) - l,   # line 2
                              sy              - l]))
        diamond.append(tuple([sx              - l,   # line 3
                              sy - (radius+1) + l]))
        diamond.append(tuple([sx - (radius+1) + l,   # line 4
                              sy              + l]))

    return np.array(diamond, dtype=np.int64)


sensors = np.zeros((len(lines), 5),dtype=np.int64)

for i, line in enumerate(lines):
    parse = re.search('Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)

    for j in range(4):
        sensors[i, j] = int(parse.group(j + 1))  # [sensor x, sensor y, beacon x, beacon y, distance]

    sensors[i, 4] = abs(sensors[i, 0] - sensors[i, 2]) + abs(sensors[i, 1] - sensors[i, 3])

xlim = tuple([int(np.append(sensors[:, 0] - sensors[:,4], sensors[:, 2]).min()),
              int(np.append(sensors[:, 0] + sensors[:,4], sensors[:, 2]).max())])
ylim = tuple([int(np.append(sensors[:, 1] - sensors[:,4], sensors[:, 3]).min()),
              int(np.append(sensors[:, 1] + sensors[:,4], sensors[:, 3]).max())])

# coverage_counter = 0
# test_y = 2000000
#
# test_y_sensors = sensors[~(abs(sensors[:,1] - test_y) > sensors[:,4])]

# for test_x in range(xlim[0], xlim[1] + 1):
#     test_x_sensors = test_y_sensors[~(abs(test_y_sensors[:, 0] - test_x) > test_y_sensors[:, 4])]
#
#     if (abs(sensors[:, 0] - test_x) + abs(sensors[:, 1] - test_y) <= sensors[:, 4]).any():  # location within range
#         if not np.logical_and(sensors[:, 2] == test_x, sensors[:, 3] == test_y).any():      # ... but not a beacon
#             coverage_counter += 1
#     pass
#
# print(f"{coverage_counter=}")

test_area = 4000000
found = False

# test diamond per sensor
for sensor in sensors:
    print(sensor)
    test_points = gen_test_points(sensor[0], sensor[1], sensor[4])
    test_points = test_points[(0 <= test_points[:,0]) & (test_points[:,0] <= test_area) & (0 <= test_points[:,1]) & (test_points[:,1] <= test_area)] # Remove out of bounds
    pass
    for test_point in test_points:
        if not (abs(sensors[:, 0] - test_point[0]) + abs(sensors[:, 1] - test_point[1]) <= sensors[:, 4]).any(): # not within any range:
            found = True
            break
    if found:
        break

print(f"location: ({test_point[0]},{test_point[1]})\nTuning frequency: {test_point[0]*4000000+test_point[1]}")


