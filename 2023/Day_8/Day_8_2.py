import math

_file = open("Input", 'r')
_lines = _file.readlines()


class instructions:
    def __init__(self, instruction_string):
        self.instruction_string = instruction_string
        self.instruction_length = len(self.instruction_string)
        self.current_instruction = 0

    def next(self):
        next_instruction = self.instruction_string[self.current_instruction]
        self.current_instruction += 1
        if self.current_instruction >= self.instruction_length:
            self.current_instruction = 0
        return next_instruction


_network = dict()
_current_superposition = []

_instruction = instructions(_lines[0].removesuffix("\n"))

for node in _lines[2:]:
    _network.update({node[0:3]: {"L": node[7:10], "R": node[12:15]}})
    if node[2] == "A":
        _current_superposition.append(node[0:3])

_trail_log = [{0: start} for start in _current_superposition]

_f_early_break = False
_steps = 1
while True:
    _future_superposition = []
    _finish_check = []
    instruction = _instruction.next()
    for idx, trail in enumerate(_current_superposition):
        next_node = _network[trail][instruction]
        _future_superposition.append(next_node)

        if next_node[2] == "Z":
            _trail_log[idx].update({_steps: next_node})
            _finish_check.append(True)
        else:
            _finish_check.append(False)

    if all(_finish_check):
        print("al Zs reached")
        # break

    if min([len(trail) for trail in _trail_log]) > 5:
        print("each trail reached a Z at least 5 times")
        _f_early_break = True
        break

    _steps += 1
    _current_superposition = _future_superposition.copy()


if not _f_early_break:
    print(f"Part 2: {_steps}")
else:
    print("trail_log")
    lcm_period = 1
    for trail in _trail_log:
        marked_steps = list(trail.keys())
        periods = [marked_steps[idx + 1] - marked_steps[idx] for idx in range(1, len(marked_steps) - 1)]
        print(f"trail {trail[0]} ends at {trail[marked_steps[1]]}")
        print(f"first arrival after {marked_steps[1]} steps")
        print(f"\tarrived there {len(marked_steps) - 1} times with the periods:")
        print(f"\t{periods}")
        print()

        lcm_period = math.lcm(lcm_period, marked_steps[1])
        # from personal inspection, all periods and initial tracks are the same so the common period for all
        # superpositions (and thus the time to reach all Z locations) is the LCM of the individual periods

    print(f"Part 2: {lcm_period}")