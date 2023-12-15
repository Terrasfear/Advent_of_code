import numpy as np

_file = open("Input", 'r')
_line = _file.readline().removesuffix("\n")


def holiday_hash(instruction):
    hash_value = 0
    for char in instruction:
        char_ascii = ord(char)

        hash_value = np.add(hash_value, char_ascii)
        hash_value = np.multiply(hash_value, np.ubyte(17), dtype=np.uint8)
    return hash_value


hash_sum = 0
for instruction in _line.split(","):
    current_hash_value = holiday_hash(instruction)

    hash_sum += current_hash_value

print(f"Part 1: {hash_sum}")

# Part 2

hash_map = dict()
boxes = {box_nr: {} for box_nr in range((256))}

for instruction in _line.split(","):
    if instruction[-2] == "=":  # placement instruction
        label = instruction[:-2]
        box_nr = hash_map.setdefault(label, holiday_hash(label))
        focal_length = int(instruction[-1])

        boxes[box_nr][label] = focal_length


    else:  # remove instruction
        label = instruction[:-1]
        box_nr = hash_map.setdefault(label, holiday_hash(label))

        boxes[box_nr].pop(label, None)

focus_power_sum = 0
for box_nr in range(256):
    box = boxes[box_nr]
    if len(box) == 0:
        continue

    for slot_nr, lens in enumerate(box.values()):
        focus_power_sum += (box_nr + 1) * (slot_nr + 1) * lens

print(f"Part 2: {focus_power_sum}")
