class Machine:
    def __init__(self, program: list[int], starting_registers: tuple[int, int, int]):
        self.instructions = program[0::2]
        self.operands = program[1::2]

        self.program_counter = 0
        self.program_length = len(self.instructions)

        self.A, self.B, self.C = starting_registers

        self.output = []

        self.opcode_dict = {0: self.adv,
                            1: self.bxl,
                            2: self.bst,
                            3: self.jnz,
                            4: self.bxc,
                            5: self.out,
                            6: self.bdv,
                            7: self.cdv}

    def reset(self, starting_A: int):
        self.program_counter = 0
        self.A = starting_A
        self.B = 0
        self.C = 0
        self.output = []

    def run_program(self):
        while 0 <= self.program_counter < self.program_length:
            self.opcode_dict[self.instructions[self.program_counter]](self.operands[self.program_counter])
            self.program_counter += 1

    def combo_operand(self, operand: int):
        if operand <= 3:
            return operand
        if operand == 4:
            return self.A
        if operand == 5:
            return self.B
        if operand == 6:
            return self.C

        raise ValueError(f"operand {operand} not in range [0,7)")

    def adv(self, operand: int):
        self.A = self.A >> self.combo_operand(operand)

    def bxl(self, operand: int):
        self.B = self.B ^ operand

    def bst(self, operand: int):
        self.B = self.combo_operand(operand) & 0b111

    def jnz(self, operand: int):
        if self.A != 0:
            self.program_counter = operand - 1

    def bxc(self, operand: int):
        self.B = self.B ^ self.C

    def out(self, operand: int):
        self.output.append(self.combo_operand(operand) & 0b111)

    def bdv(self, operand: int):
        self.B = self.A >> self.combo_operand(operand)

    def cdv(self, operand: int):
        self.C = self.A >> self.combo_operand(operand)

def octets_to_value(octets:list[int]):
    value = 0
    for octet in octets:
        value = value << 3
        value += octet
    return value

with open("Input", "r") as _file:
    _lines = _file.readlines()

    _registers_start = tuple([int(_lines[i].removesuffix("\n").split(":")[-1]) for i in range(3)])
    _program = [int(value) for value in
                _lines[4].removesuffix("\n").split(":")[-1].split(",")]

machine = Machine(_program, _registers_start)

machine.run_program()

print(f"Part 1: {machine.output}")

# finding the correct register A:

_found_octets = [0]
_current_octet = 0
while True:

    _found_octets[-1] = _current_octet
    _register_A_value = octets_to_value(_found_octets)

    machine.reset(_register_A_value)
    machine.run_program()
    if machine.output == _program[-len(_found_octets):]:
        print(f"octets: {_found_octets},\tresult: {machine.output}")
        if machine.output == _program:
            break

        _found_octets.append(0)
        _current_octet = 0
        continue
    elif _current_octet == 7:
        _found_octets.pop()
        _current_octet = _found_octets[-1]

    _current_octet += 1

print(f"Part 2: {octets_to_value(_found_octets)}")
