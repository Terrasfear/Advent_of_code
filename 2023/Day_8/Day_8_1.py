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

_instruction = instructions(_lines[0].removesuffix("\n"))

for node in _lines[2:]:
    _network.update({node[0:3]: {"L": node[7:10], "R": node[12:15]}})

_current_node = "AAA"
_steps = 1
while True:
    _next_node = _network[_current_node][_instruction.next()]
    if _next_node == "ZZZ":
        break
    _steps += 1
    _current_node = _next_node

print(f"Part 1: {_steps}")
