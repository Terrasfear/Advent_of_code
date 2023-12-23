from heapdict import heapdict

_file = open("Input", 'r')
_lines = [line.removesuffix('\n') for line in _file.readlines()]


class Block:
    def __init__(self, start: (int, int, int), end: (int, int, int)):
        self.supported_by = set()
        self.supporting = dict()

        sx, sy, sz = start
        ex, ey, ez = end

        low_x = min(sx, ex)
        high_x = max(sx, ex)

        low_y = min(sy, ey)
        high_y = max(sy, ey)

        self.bottom = min(sz, ez)
        self.top = max(sz, ez)

        self.xy = set()
        self.cords = set()
        for x in range(low_x, high_x + 1):
            for y in range(low_y, high_y + 1):
                self.xy.add((x, y))
                for z in range(self.bottom, self.top + 1):
                    self.cords.add((x, y, z))

    def get_x_y(self):
        return self.xy

    def get_cords(self):
        return self.cords

    def update_deep_supporting(self, deep_supported, fraction):
        if deep_supported not in self.supporting:
            self.supporting[deep_supported] = 0

        self.supporting[deep_supported] += fraction
        for support in self.supported_by:
            support.update_deep_supporting(deep_supported, fraction / len(self.supported_by))

    def drop_down(self, height_map):
        new_height = 1 + max([height_map[xy][0] for xy in self.xy])

        for support in [height_map[xy][1] for xy in self.xy if height_map[xy][0] == new_height - 1]:
            if support is not None:
                self.supported_by.add(support)

        for support in self.supported_by:
            # if support is not None:
            support.update_deep_supporting(self, 1 / len(self.supported_by))

        drop = new_height - self.bottom

        self.bottom += drop
        self.top += drop

        self.cords = set([(cord[0], cord[1], cord[2] + drop) for cord in self.cords])

        for xy in self.xy:
            height_map[xy] = (self.top, self)


_height_map = {(x, y): [0, None] for x in range(10) for y in range(10)}
_airborne_blocks = heapdict()
_dropped_blocks = []
for line in _lines:
    values = list(map(int, line.replace(",", "~").split("~")))
    _airborne_blocks[Block(tuple(values[:3]), tuple(values[3:]))] = min(values[2], values[5])

while _airborne_blocks:
    falling_block = _airborne_blocks.popitem()[0]
    falling_block.drop_down(_height_map)
    _dropped_blocks.append(falling_block)

num_disintegratable = 0
sum_disintegrate_chains = 0
for block in _dropped_blocks:
    num_disintegratable += all(map(lambda x: x < 1, block.supporting.values()))
    sum_disintegrate_chains += sum(map(lambda x: x == 1, block.supporting.values()))

print(f"Part 1: {num_disintegratable}")
print(f"Part 2: {sum_disintegrate_chains}")
