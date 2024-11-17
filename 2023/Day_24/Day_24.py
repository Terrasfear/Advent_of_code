import numpy as np

_file = open("Input", 'r')
_lines = [line.removesuffix('\n') for line in _file.readlines()]


class Hailstone:
    def __init__(self, description: str):
        pos, vel = description.split("@")

        self.Px, self.Py, self.Pz = [int(p) for p in pos.split(",")]
        self.Vx, self.Vy, self.Vz = [int(v) for v in vel.split(",")]

        # y = xy_slope * x +xy_start
        self.xy_slope = self.Vy / self.Vx
        self.xy_start = self.Py - self.xy_slope * self.Px

    def print(self):
        print(f"{(self.Px, self.Py, self.Pz)}\t\t{(self.Vx, self.Vy, self.Vz)}")

    def getParam(self, pos_vel: str, axis: str):
        if pos_vel.lower() == "v":
            if axis.lower() == "x":
                return self.Vx
            elif axis.lower() == "y":
                return self.Vy
            elif axis.lower() == "z":
                return self.Vz
            else:
                raise TypeError(f"Invalid axis: {axis}")
        elif pos_vel.lower() == "p":
            if axis.lower() == "x":
                return self.Px
            elif axis.lower() == "y":
                return self.Py
            elif axis.lower() == "z":
                return self.Pz
            else:
                raise TypeError(f"Invalid axis: {axis}")
        else:
            raise TypeError(f"Invalid pos_vel: {pos_vel}")

    def getPaVb_PbVa(self, axis1: str, axis2: str):
        return self.getParam("p", axis1) * self.getParam("v", axis2) - self.getParam("p", axis2) * self.getParam("v",
                                                                                                                 axis1)


def intersect(A: Hailstone, B: Hailstone) -> (bool, (float, float)):
    if A.xy_slope == B.xy_slope:
        if A.xy_start != B.xy_start:
            return False
        else:
            print("Warning, trajedctories are the same in xy")
            return True

    x = (B.xy_start - A.xy_start) / (A.xy_slope - B.xy_slope)
    y = A.xy_slope * x + A.xy_start

    # test that the collision happens in the future
    if (x - A.Px) * A.Vx > 0 and (x - B.Px) * B.Vx > 0:
        return x, y
    else:
        return False


def in_search_box(cord):
    # low = 7
    # high = 27

    low = 200000000000000
    high = 400000000000000

    return low <= cord[0] <= high and low <= cord[1] <= high


_hailstones = []
for line in _lines:
    _hailstones.append(Hailstone(line))

# xy_search_box = (range(7, 27 + 1),
#                  range(7, 27 + 1))
xy_search_box = (range(200000000000000, 400000000000000 + 1),
                 range(200000000000000, 400000000000000 + 1))

num_collisions = 0
num_hailstones = len(_hailstones)
for HailA_idx, HailA in enumerate(_hailstones):
    for HailB in _hailstones[HailA_idx + 1:]:
        collision = intersect(HailA, HailB)

        # HailA.print()
        # HailB.print()
        # print(f"collision: {collision}")

        if collision:
            if len(collision) == 1:  # returned true
                num_collisions += 1
            else:
                box_check = in_search_box(collision)
                # print(box_check)
                num_collisions += box_check

        # print()

print(f"Part 1: {num_collisions}")


# Part 2
def pairDiff(hailstone1: Hailstone, hailstone2: Hailstone, pos_vel: str, axis: str):
    return hailstone1.getParam(pos_vel, axis) - hailstone2.getParam(pos_vel, axis)


def const(hailstone1: Hailstone, hailstone2: Hailstone, axis1: str, axis2: str):
    return -hailstone1.getPaVb_PbVa(axis1, axis2) + hailstone2.getPaVb_PbVa(axis1, axis2)

np.set_printoptions(suppress=True,
                    formatter={'float_kind': '{:16.4f}'.format}, linewidth=130)

quoatientsXY = []
resultsXY = []
pairs = [(0, 1), (0, 2), (0, 3), (0, 4)]

# x,y
for pair in pairs:
    hailstone1 = _hailstones[pair[0]]
    hailstone2 = _hailstones[pair[1]]

    quoatientsXY.append([(hailstone1.Py - hailstone2.Py),  # *Vxr
                       -(hailstone1.Px - hailstone2.Px),  # *Vyr
                       # 0,  # *Vzr
                       -(hailstone1.Vy - hailstone2.Vy),  # *Pxr
                       (hailstone1.Vx - hailstone2.Vx)])  # *Pyr
                       # 0])  # *Pzr
    resultsXY.append(hailstone2.getPaVb_PbVa("x", "y") - hailstone1.getPaVb_PbVa("x", "y"))

# y,z
quoatientsYZ = []
resultsYZ = []
for pair in pairs:
    hailstone1 = _hailstones[pair[0]]
    hailstone2 = _hailstones[pair[1]]

    quoatientsYZ.append([#0,  # *Vxr
                       (hailstone1.Pz - hailstone2.Pz),  # *Vyr
                       -(hailstone1.Py - hailstone2.Py),  # *Vzr
                       #0,  # *Pxr
                       -(hailstone1.Vz - hailstone2.Vz),  # *Pyr
                       (hailstone1.Vy - hailstone2.Vy)])  # *Pzr
    resultsYZ.append(hailstone2.getPaVb_PbVa("y", "z") - hailstone1.getPaVb_PbVa("y", "z"))

# z,x
quoatientsZX = []
resultsZX = []
for pair in pairs:
    hailstone1 = _hailstones[pair[0]]
    hailstone2 = _hailstones[pair[1]]

    quoatientsZX.append([-(hailstone1.Pz - hailstone2.Pz),  # *Vxr
                       # 0,  # *Vyr
                       (hailstone1.Px - hailstone2.Px),  # *Vzr
                       (hailstone1.Vz - hailstone2.Vz),  # *Pxr
                       # 0,  # *Pyr
                       -(hailstone1.Vx - hailstone2.Vx)])  # *Pzr
    resultsZX.append(hailstone2.getPaVb_PbVa("z", "x") - hailstone1.getPaVb_PbVa("z", "x"))

# q = np.array(quoatients, dtype=np.longlong)
# r = np.array(results, dtype=np.longlong)
rockXY = np.linalg.solve(quoatientsXY, resultsXY)

print("XY")
for i, row in enumerate(quoatientsXY):
    for entry in row:
        print(f"{entry:>20d}", end='\t')
    print(f"|\t{resultsXY[i]:>20d}")
print(rockXY)

print()

rockYZ = np.linalg.solve(quoatientsYZ, resultsYZ)
print("YZ")
for i, row in enumerate(quoatientsYZ):
    for entry in row:
        print(f"{entry:>20d}", end='\t')
    print(f"|\t{resultsYZ[i]:>20d}")
print(rockYZ)

print()

rockZX = np.linalg.solve(quoatientsZX, resultsZX)
print("ZX")
for i, row in enumerate(quoatientsZX):
    for entry in row:
        print(f"{entry:>20d}", end='\t')
    print(f"|\t{resultsZX[i]:>20d}")
print(rockZX)

#not the best, had to look for the largest interger options