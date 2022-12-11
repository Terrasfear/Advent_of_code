import re
import numpy as np

def getranges(pair:str):
    vals = list(map(int, re.split(',|-',pair.strip('\n'))))
    elves = np.reshape(vals, (2, 2))

    return elves

def contains(elf1, elf2):
    if elf1[0] >= elf2[0] and elf1[1] <= elf2[1]:
        return True
    else:
        return False


def overlap(elf1, elf2):
    elf1set = set(range(elf1[0], elf1[1] + 1))
    elf2set = set(range(elf2[0], elf2[1] + 1))

    if elf1set.intersection(elf2set):
        return True
    else:
        return False

file = open("input", 'r')
pairs = file.readlines()

count_contain = 0
count_overlap = 0
for pair in pairs:
    elves = getranges(pair)

    if contains(elves[0], elves[1]) or contains(elves[1], elves[0]):
        count_contain = count_contain + 1

    if overlap(elves[0], elves[1]) or overlap(elves[1], elves[0]):
        count_overlap = count_overlap + 1

print(f'Q4.1: {count_contain}')
print(f'Q4.2: {count_overlap}')


