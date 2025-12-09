class Rules:
    def __init__(self, rules):
        self.rules = rules

    def __call__(self, lhs, rhs):
        if (lhs, rhs) in self.rules:
            return True
        elif (rhs, lhs) in self.rules:
            return False
        else:
            raise Exception(f"no rule with both {lhs} and {rhs}")


def testUpdate(update: list[int], rules: Rules):
    for i in range(len(update)-1):
        if not rules(update[i], update[i+1]):
            return False
    return True
    
def bubbleSort(l :list, rule):
    round = 1
    while round < len(l)+1:
        for idx in range(len(l)-round):
            if not rule(l[idx], l[idx+1]):
                l[idx], l[idx+1] = l[idx+1], l[idx]
        round += 1

def reorderUpdate(update: list[int], rules: Rules):
    bubbleSort(update, rules)


with open("Input", "r") as _file:
    _lines = iter(_file.readlines())

    _rule_list: list[tuple[int, int]] = []
    _updates: list[list[int]] = []

    while (line := next(_lines)) != "\n":
        _rule_list.append(tuple(map(int, line.removesuffix("\n").split("|"))))

    _rules = Rules(_rule_list)

    while line := next(_lines, None):
        _updates.append(list(map(int, line.removesuffix("\n").split(","))))

_middles_sum = 0
_reordered_middles_sum = 0
for update in _updates:
    if testUpdate(update, _rules):
        _middles_sum += update[len(update) // 2]
    else:
        reorderUpdate(update, _rules)
        _reordered_middles_sum += update[len(update) // 2]

print(f"Part 1: {_middles_sum}")
print(f"Part 2: {_reordered_middles_sum}")
