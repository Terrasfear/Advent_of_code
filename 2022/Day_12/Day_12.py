import numpy as np
import re

file = open("Input", 'r')
lines = file.readlines()

height_map = np.zeros([len(lines), len(lines[1]) - 1], dtype=np.uint8)


class Map_walker:

    def __init__(self, height_map, starting_point, end_point, goal):
        self.height_map = height_map
        self.starting_point = tuple(starting_point)
        self.end_point = tuple(end_point)

        self.map_shape = self.height_map.shape

        self.current_step = 1
        self.walking_map = np.zeros_like(self.height_map, dtype=np.uint32)
        self.walking_map[self.end_point] = 1

        if isinstance(goal, int) or goal == "start":
            self.goal = goal
        else:
            raise Exception(f"invalid goal: {goal}")

    def print_height_map(self):
        print(self.height_map)

    def print_walking_map(self):
        print(self.walking_map)

    def check_size_limit(self):
        if self.current_step >= np.iinfo(self.walking_map.dtype).max:
            raise Exception("overflow")

    def find_valid_steps(self):
        valid_map = np.zeros_like(self.walking_map)
        current_locs = np.argwhere(self.walking_map == self.current_step)
        current_locs = np.hstack(
            (current_locs, np.reshape(self.height_map[current_locs[:, 0], current_locs[:, 1]], (-1, 1))))

        north_steps = current_locs + [-1, 0, 0]
        south_steps = current_locs + [1, 0, 0]
        west_steps = current_locs + [0, -1, 0]
        east_steps = current_locs + [0, 1, 0]

        # all possible previous locations
        steps = np.concatenate((north_steps, south_steps, east_steps, west_steps))

        # remove out of bounds steps
        steps = steps[steps[:, 0] >= 0]  # too far north
        steps = steps[steps[:, 0] < self.map_shape[0]]  # too far south
        steps = steps[steps[:, 1] >= 0]  # too far west
        steps = steps[steps[:, 1] < self.map_shape[1]]  # too far east

        # remove steps that have already been visited
        steps = steps[self.walking_map[steps[:, 0], steps[:, 1]] == 0]

        # remove steps that originate from places more that 1 elevation lower
        steps = steps[self.height_map[steps[:, 0], steps[:, 1]] >= steps[:, 2] - 1]

        valid_map[steps[:, 0], steps[:, 1]] = 1

        return valid_map

    def step(self):
        self.check_size_limit()

        # find valid steps
        valid_map = self.find_valid_steps()

        self.current_step += 1
        self.walking_map += valid_map * self.current_step

        if self.goal == "start":
            if not self.walking_map[self.starting_point]:
                return False
        else:
            if not np.logical_and(self.walking_map, self.height_map == self.goal).any():
                return False

        return True


# build height map as values
for i, line in enumerate(lines):
    start = re.search('S', line)
    if start:
        starting_point = np.array([i, start.span()[0]], dtype=np.uint8)
        line = re.sub('S', 'a', line)

    end = re.search('E', line)
    if end:
        end_point = np.array([i, end.span()[0]], dtype=np.uint8)
        line = re.sub('E', 'z', line)

    height_map[i, :] = list(map(ord, line[0:-1]))

height_map -= ord('a')

walker = Map_walker(height_map, starting_point, end_point, goal=0)

walker.print_height_map()

steps = 1
while not walker.step():
    pass

walker.print_walking_map()
print(walker.current_step - 1)

pass
