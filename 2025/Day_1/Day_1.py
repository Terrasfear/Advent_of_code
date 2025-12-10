0
file = open("input_test",'r')


position = 50
ring_size = 100

zeros_encountered = 0
zeros_clicked = 0

with open(f"input", 'r') as _file:
    _lines = _file.readlines()

    for line in _lines:
        line = line.removesuffix("\n")

        direction = line[0]
        steps_str = line[1:]
        if len(steps_str) > 2:
            # print(f"full rotation, {steps_str[0:-2]}")
            zeros_clicked += int(steps_str[0:-2])

        # print(f"steps remaining: {steps_str[-2:]}")
        steps = int(steps_str[-2:])
        
        if direction == "R":
            if steps + position > ring_size:
                zeros_clicked += 1
                position += steps -ring_size
            elif steps + position == ring_size:
                zeros_clicked += 1
                zeros_encountered += 1
                position = 0
            else: # steps + position < ringsize
                position += steps
        else: # direction == "L"
            if steps > position:
                if position != 0:
                  zeros_clicked += 1
                position -= steps
                position += ring_size
            elif steps == position:
                zeros_clicked += 1
                zeros_encountered += 1
                position = 0
            else: # steps < position:
                position -= steps

        # print(f"Position {position}\t ticks {zeros_clicked}")
        # print()

print(f"Part 1: {zeros_encountered}")
print(f"Part 2: {zeros_clicked}")
# 5829 too high

