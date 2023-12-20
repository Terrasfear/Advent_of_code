from operator import gt, lt
from functools import cache

_file = open("input", 'r')
_lines = _file.readlines()


class Endflow_accept:
    def filter(self, part: dict) -> int:
        return sum(part.values())

    def filter_ranges(self, part_ranges: dict) -> int:
        combinations = 1
        for catagory in part_ranges:
            options = part_ranges[catagory][1] - part_ranges[catagory][0]
            combinations *= options
        return combinations

    def prune(self):
        return False


class Endflow_reject:
    def filter(self, part: dict) -> int:
        return 0

    def filter_ranges(self, part_ranges: dict) -> int:
        return 0

    def prune(self):
        return False


class Workflow:
    def __init__(self, description: str):
        name, rules_str = description.split("{")
        rules_str = rules_str.removesuffix("}\n").split(",")

        self.name = name
        self.rules = []
        self.exit = rules_str[-1]

        rules_str = rules_str[:-1]
        for rule_str in rules_str:
            condition, target = rule_str.split(":")

            new_rule = [condition[0], None, int(condition[2:]), target]
            # determine instruction:
            if condition[1] == ">":
                new_rule[1] = gt
            else:
                new_rule[1] = lt
            self.rules.append(new_rule)

            if target not in _backpropagation:
                _backpropagation[target] = {name}
            else:
                _backpropagation[target].add(name)

        if self.exit not in _backpropagation:
            _backpropagation[self.exit] = {name}
        else:
            _backpropagation[self.exit].add(name)

    def filter(self, part: dict):
        for rule in self.rules:
            if rule[1](part[rule[0]], rule[2]):
                return _workflows[rule[3]].filter(part)
        return _workflows[self.exit].filter(part)

    def filter_ranges(self, part_ranges: dict):
        path_options = 0
        for rule in self.rules:
            branching_ranges, part_ranges = self.split_ranges(part_ranges,rule[0], rule[1], rule[2])

            path_options += _workflows[rule[3]].filter_ranges(branching_ranges)

        path_options += _workflows[self.exit].filter_ranges(part_ranges)

        return path_options
    def split_ranges(self, part_ranges: dict, category: str, operand, border):
        match_ranges = part_ranges.copy()
        non_match_ranges = part_ranges.copy()

        if operand == gt:
            match_ranges[category] = (border + 1, part_ranges[category][1])
            non_match_ranges[category] = (part_ranges[category][0], border + 1)
        else:  # operand == lt
            match_ranges[category] = (part_ranges[category][0], border)
            non_match_ranges[category] = (border, part_ranges[category][1])
        return match_ranges, non_match_ranges

    def prune(self) -> bool:
        while self.rules:  # remove if exit matches last target
            if self.rules[-1][3] == self.exit:
                del self.rules[-1]
                continue
            else:
                break

        # merge if two rules are the same par for the value
        rule_idx = 0
        while rule_idx < len(self.rules) - 1:
            if self.rules[rule_idx][0] == self.rules[rule_idx + 1][0] and self.rules[rule_idx][1] == \
                    self.rules[rule_idx + 1][1] and self.rules[rule_idx][3] == self.rules[rule_idx + 1][3]:
                if self.rules[rule_idx][1](self.rules[rule_idx][2], self.rules[rule_idx + 1][2]):
                    del self.rules[rule_idx]
                else:
                    del self.rules[rule_idx + 1]
                continue
            else:
                rule_idx += 1

        if not self.rules:  # the workflow collapsed to only the exit -> can be removed (restart pruning)
            for upstream in _backpropagation[self.name]:
                _workflows[upstream].replace(self.name, self.exit)
                _backpropagation[self.exit].add(upstream)

            _backpropagation[self.exit].remove(self.name)

            del _backpropagation[self.name]
            return True

        return False

    def replace(self, old_target, new_target):
        for rule in self.rules:
            if rule[3] == old_target:
                rule[3] = new_target

        if self.exit == old_target:
            self.exit = new_target


accept = Endflow_accept()
reject = Endflow_reject()

_workflows = {"A": accept, "R": reject}
_backpropagation = {}

accepted_sum = 0
F_workflow_processing = True
for line in _lines:
    if line == "\n":  # blank line, going from building workflows to processing parts
        F_workflow_processing = False

        # Prune workflow parts which have the same final case as the one before.
        # if the pruning causes the entire workflow to collapse, then back propagate to skip it

        F_workflow_removed = True
        while F_workflow_removed:
            F_workflow_removed = False
            for workflow in _workflows:
                if _workflows[workflow].prune():
                    del _workflows[workflow]
                    F_workflow_removed = True
                    break

        continue

    if F_workflow_processing:
        new_workflow = Workflow(line)
        _workflows[new_workflow.name] = new_workflow
        pass


    else:
        part_categories = line.removesuffix("}\n").removeprefix("{").split(",")

        new_part = {}
        for category in part_categories:
            new_part[category[0]] = int(category[2:])

        accepted_sum += _workflows["in"].filter(new_part)

print(f"Part 1: {accepted_sum}")

min_val = 1
max_val = 4001  # exclusive

part_range = {"x": (min_val, max_val),
              "m": (min_val, max_val),
              "a": (min_val, max_val),
              "s": (min_val, max_val)}

num_accepted = _workflows["in"].filter_ranges(part_range)

print(f"Part 2: {num_accepted}")
pass
