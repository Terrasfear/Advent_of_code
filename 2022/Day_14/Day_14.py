import re

import numpy as np

file = open("Input", 'r')
lines = file.readlines()


class Sandfall:
    scan_map = None
    scan_limits = np.array([[500, 500], [0, 0]])  # [[xmin, xmax], [ymin, ymax]]
    xmin = 500
    xmax = 500
    ymin = 0
    ymax = 0

    sand_source = np.flip(np.array([500, 0]))

    walls = []

    time_counter = -1

    bordered = None

    def add_wall(self, wall):
        self.walls.append(wall)

        # check sizes for scan_limits
        if wall[:, 0].min() < self.xmin:  # xmin
            self.xmin = wall[:, 0].min()
        if wall[:, 0].max() > self.xmax:  # xmax
            self.xmax = wall[:, 0].max()
        if wall[:, 1].min() < self.ymin:  # ymin
            self.ymin = wall[:, 1].min()
        if wall[:, 1].max() > self.ymax:  # ymax
            self.ymax = wall[:, 1].max()

    def add_border(self):
        self.xmin -= 1
        self.xmax += 1
        self.ymax += 1
        self.bordered = "border"

    def add_floor(self):
        self.ymax += 2
        max_width = self.ymax
        self.xmax = max([self.xmax, self.sand_source[1]+max_width])
        self.xmin = min([self.xmin, self.sand_source[1]-max_width])
        self.bordered = "floor"

    def remove_border(self):
        self.xmin -= -1
        self.xmax += -1
        self.ymax += -1
        self.bordered = None

    def remove_floor(self):
        self.xmin -= -1
        self.xmax += -1
        self.ymax += -2
        self.bordered = None

    def build_scan_map(self, question_nr):
        if self.bordered == 'border':
            self.remove_border()
        elif self.bordered == "floor":
            self.remove_floor()

        if question_nr == 1:
            self.add_border()
        else:
            self.add_floor()

        self.time_counter = -1  # reset

        # self.scan_map = [['.'] * (xmax - xmin + 1) for _ in range(ymin, ymax + 1)]
        self.scan_map = np.chararray((self.ymax - self.ymin + 1, self.xmax - self.xmin + 1))
        self.scan_map[:] = '.'
        self.scan_map[-1, :] = '~' if question_nr == 1 else '#'  # void or floor
        self.scan_map = self.scan_map.astype('<U1')

        self.scan_map[tuple(self.sand_source - [self.ymin, self.xmin])] = '+'
        # self.scan_map[self.sand_source[0] - self.ymin][self.sand_source[1] - self.xmin] = '+'

        for wall in self.walls:
            for j in range(wall.shape[0] - 1):
                xcords = list(range(wall[j:j + 2, 0].min(), wall[j:j + 2, 0].max() + 1))
                ycords = list(range(wall[j:j + 2, 1].min(), wall[j:j + 2, 1].max() + 1))

                if len(xcords) == 1:  # vertical line
                    xcord = xcords[0]
                    for ycord in ycords:
                        self.scan_map[ycord - self.ymin][xcord - self.xmin] = '#'

                elif len(ycords) == 1:  # horizontal line
                    ycord = ycords[0]
                    for xcord in xcords:
                        self.scan_map[ycord - self.ymin][xcord - self.xmin] = '#'

    def print_scan_map(self):
        for i, row in enumerate(self.scan_map):
            print(f'{i}\t', end='')
            for elem in row:
                print(f"{elem}", end='')
            print('')
        print('')

    def time_step(self):
        sand_cords = self.sand_source - [self.ymin, self.xmin]

        while True:
            # fall down to unobstructed
            current_column = self.scan_map[:, sand_cords[1]]
            obstruction_idx = np.where((current_column == '#') | (current_column == 'o') | (current_column == '~'))
            obstruction_idx = obstruction_idx[0][obstruction_idx[0] > sand_cords[0]][0]

            if current_column[obstruction_idx] == '~':
                sand_cords[0] = obstruction_idx
                break

            sand_cords[0] = obstruction_idx - 1

            if self.scan_map[tuple(sand_cords + [1, -1])] == '.':  # check left
                sand_cords = sand_cords + [1, -1]
                continue
            elif self.scan_map[tuple(sand_cords + [1, 1])] == '.':  # check right
                sand_cords = sand_cords + [1, 1]
                continue
            else:
                break

        self.time_counter += 1
        self.scan_map[tuple(sand_cords)] = 'o'

    def end_reached(self):
        # returns true if there is sand on the bottom (requires void) or at the world height
        return (self.scan_map[-1, :] == 'o').any() or (self.scan_map[0, :] == 'o').any()


sandfall = Sandfall()

for line in lines:
    corners = re.findall("((\d+),(\d+))", line)

    wall = []
    for point in corners:
        wall.append([int(point[1]), int(point[2])])

    sandfall.add_wall(np.array(wall))

sandfall.build_scan_map(question_nr=1)

while not sandfall.end_reached():
    sandfall.time_step()

sandfall.print_scan_map()
print(f"Q14.1: {sandfall.time_counter} time units")

sandfall.build_scan_map(question_nr=2)
while not sandfall.end_reached():
    sandfall.time_step()
    if not sandfall.time_counter%500:
        print(f"{sandfall.time_counter+1} time units and going")

sandfall.print_scan_map()
print(f"Q14.2: {sandfall.time_counter+1} time units")