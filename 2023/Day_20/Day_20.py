import matplotlib.pyplot as plt
from math import lcm

_file = open("Input")
_lines = _file.readlines()


def print_propagation(propagation):
    for prop in propagation:
        print(f"{prop[1][0]} ---{prop[1][1]}---> {prop[0]}")


class Node:
    def __init__(self, name: str, targets: [str] or None):
        self.name = name
        self.outgoing = targets
        self.incoming = []

    def pulse_input(self, source: str, pulse: str) -> [(str, str)]:
        return []

    def update_incoming(self):
        for target in self.outgoing:
            if target in _nodelist:
                _nodelist[target].incoming.append(self.name)

    def find_target(self, target):
        if target in self.outgoing:
            return True
        return False


class Button(Node):
    def push(self):
        return [(target, (self.name, "L")) for target in self.outgoing]


class Broadcast(Node):
    def pulse_input(self, source: str, pulse: str) -> [(str, str)]:
        return [(target, (self.name, pulse)) for target in self.outgoing]


class Flip_flop(Node):
    def __init__(self, name: str, targets: [str]):
        super().__init__(name, targets)
        self.state = False

    def pulse_input(self, source: str, pulse: str) -> [(str, str)]:
        if pulse == "H":
            return []
        else:
            if self.state:
                self.state = False
                return [(target, (self.name, "L")) for target in self.outgoing]
            else:
                self.state = True
                return [(target, (self.name, "H")) for target in self.outgoing]


class Conjunction(Node):
    def __init__(self, name: str, targets: [str]):
        super().__init__(name, targets)
        self.memory = {}
        self.state = False

    def pulse_input(self, source: str, pulse: str) -> [(str, str)]:
        # update memory
        self.memory[source] = pulse

        if all([source_mem == "H" for source_mem in self.memory.values()]):
            return [(target, (self.name, "L")) for target in self.outgoing]
        else:
            return [(target, (self.name, "H")) for target in self.outgoing]

    def init_memory(self):
        self.memory = {source: "L" for source in self.incoming}


_nodelist = {"button": Button("button", ["broadcaster"])}
_conjunctions = []

# build node list
for line in _lines:
    name, targets = line.removesuffix('\n').split(" -> ")
    targets = targets.split(", ")

    if name[0] == '%':  # flip flop
        _nodelist[name[1:]] = Flip_flop(name[1:], targets)
    elif name[0] == "&":  # conjunction
        _nodelist[name[1:]] = Conjunction(name[1:], targets)
        _conjunctions.append(name[1:])
    elif name == "broadcaster":
        _nodelist[name] = Broadcast(name, targets)
    else:
        print(f"error, unknown name {name}")
        quit(1)

# update incoming references
for node in _nodelist:
    _nodelist[node].update_incoming()
    pass

# initialize conjunction node memories
for conjunction_node in _conjunctions:
    _nodelist[conjunction_node].init_memory()

rx_source = [node for node in _nodelist if _nodelist[node].find_target("rx")][0]
rx_leading = _nodelist[rx_source].incoming

rx_leading_traces = {source: [] for source in rx_leading}

num_high_pulses = [0]
num_low_pulses = [0]
pulse_propagation = []
for press in range(10000):
    pulse_propagation = _nodelist["button"].push()
    num_low_pulses[-1] += 1

    for trace in rx_leading_traces:
        rx_leading_traces[trace].append(0)

    while pulse_propagation:
        next_pulse_propagation = []

        for target, pulse_info in pulse_propagation:
            if target not in _nodelist:
                continue

            future_pulses = _nodelist[target].pulse_input(pulse_info[0], pulse_info[1])
            next_pulse_propagation.extend(future_pulses)

            num_low_pulses[-1] += sum(1 for future_pulse in future_pulses if future_pulse[1][1] == "L")
            num_high_pulses[-1] += sum(1 for future_pulse in future_pulses if future_pulse[1][1] == "H")

            if target in rx_leading:
                if (rx_source, (target, "H")) in future_pulses:
                    rx_leading_traces[target][-1] += 1

        pulse_propagation = next_pulse_propagation.copy()

    num_high_pulses.append(0)
    num_low_pulses.append(0)

P1_value = sum(num_low_pulses[:1000]) * sum(num_high_pulses[:1000])
print(f"Part 1:{P1_value}")

common_period = 1
for trace in rx_leading_traces:
    plt.plot(rx_leading_traces[trace])
    high_indices = [i for i,val in enumerate(rx_leading_traces[trace]) if val == 1]
    period = high_indices[1] - high_indices[0]
    common_period = lcm(common_period, period)

print(f"Part 2: {common_period}")


plt.show()
