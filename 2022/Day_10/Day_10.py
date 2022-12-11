import math

file = open("input", 'r')
lines = file.readlines()
line_idx = 0

instruction_set = {
    'noop': 1,
    'addx': 2
}

X = 1

cycle = 0
processing = False
signal_strength_sum = 0

cycle_start = 20
cycle_period = 40

CRT_heigth = 6
CRT_width = 40
crt = [['.']*CRT_width for _ in range(CRT_heigth+1)]

while True:
    cycle = cycle + 1

    # signal strength computation
    if not (cycle-cycle_start)%cycle_period:
        signal_strength_sum += cycle*X
        print(f"cycle: {cycle}\tX: {X}\tSignal strength: {cycle*X}")

    #crt printer
    crt_line = math.floor((cycle-1)/CRT_width)
    crt_x = (cycle-1)%CRT_width
    if crt_x in range(X-1, X+2):
        crt[crt_line][crt_x] = '#'

    if not processing:
        if line_idx >= len(lines):
            break
        cmd = lines[line_idx]
        line_idx += 1

        processing_cycles = instruction_set[f"{cmd[0:4]}"]
        processing = True
        # print(f"start processing:\t\t{cmd[0:4]}")

    if processing:
        processing_cycles -= 1

        if not processing_cycles:

            if cmd[0:4] == 'addx':
                X += int(cmd[5:-1])

            processing = False
            # print(f"finished processing:\t{cmd[0:4]}")

print(f"Q10.1: {signal_strength_sum}")

print("Q10.2:")
for row in crt:
    for pixel in row:
        print(f"{pixel}", end='')
    print('')
print('')