import numpy as np

_file = open("Input", 'r')
_lines = _file.readlines()

_future_values = []
_past_values = []

for line in _lines:
    history = np.array([int(value) for value in line.removesuffix('\n').split(" ")])

    last_values = [history[-1]]
    first_values = [history[0]]

    current_diff_layer = history
    while True:
        next_diff_layer = np.diff(current_diff_layer)
        current_diff_layer = next_diff_layer
        last_values.append(current_diff_layer[-1])
        first_values.append(current_diff_layer[0])
        if not next_diff_layer.any():
            _future_values.append(sum(last_values))
            _past_values.append(sum(first_values[0::2])-sum(first_values[1::2]))
            break

print(f"Part 1: {sum(_future_values)}")
print(f"Part 2: {sum(_past_values)}")