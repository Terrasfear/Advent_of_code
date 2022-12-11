import re
import math

class Monkey:
    held_items = None

    operation_type = None
    operands = None

    worry_division_factor = 1
    worry_lvl_manager = math.inf

    test_value = None
    true_target = None
    false_target = None

    Monkey_list = None

    inspection_counter = 0

    def __init__(self, monkey_description):
        starting_items = re.findall('\s(\d+)',monkey_description[0])
        self.held_items = (list(map(int, starting_items)))

        operation = re.search('new = old (.) (.+)', monkey_description[1])
        self.operation_type = operation.group((1))
        if not re.search('^[+*]|$[+*]', self.operation_type):
            raise Exception(f"{self.operation_type} not supported")
        self.operands = ['old']
        if operation.group(2) == 'old':
            self.operands.append('old')
        else:
            self.operands.append(int(operation.group(2)))

        test = re.search('(\d+)',monkey_description[2])
        self.test_value = int(test.group())
        true_target_str = re.search('(\d+)',monkey_description[3])
        self.true_target = int(true_target_str.group())
        false_target_str = re.search('(\d+)', monkey_description[4])
        self.false_target = int(false_target_str.group())

    def operation(self, item_value) -> int:

        self.inspection_counter += 1

        ops = [None, None]
        for i in range(2):
            if self.operands[i] == 'old':
                ops[i] = item_value
            else:
                ops[i] = self.operands[i]

        if self.operation_type == "*":
            return ops[0] * ops[1]
        elif self.operation_type == "+":
            return ops[0] + ops[1]
        else:
            raise Exception(f"{self.operation_type} not supported")

    def reduce_worry(self, item_value) -> int:
        return int(math.floor(item_value/self.worry_division_factor))

    def test(self,item_value):
        if not item_value%self.test_value:
            return [self.true_target, item_value]
        else:
            return [self.false_target, item_value]

    def turn(self):
        for item in self.held_items:
            worry_value = item%self.worry_lvl_manager
            worry_value = self.operation(worry_value)
            worry_value = self.reduce_worry(worry_value)
            [target, worry_value] = self.test(worry_value)

            self.Monkey_list[target].held_items.append(worry_value)

        self.held_items.clear()


file = open("Input", 'r')
lines = file.readlines()
line_idx = 0

# build monkey list
worry_division_factor = 1
monkeys = []
test_values = []
while True:
    line = lines[line_idx]
    if re.search("^Monkey", line):
        monkey_description = lines[line_idx+1:line_idx+6]
        print(len(monkeys))
        monkeys.append(Monkey(monkey_description))
        monkeys[-1].worry_division_factor = worry_division_factor
        test_values.append(monkeys[-1].test_value)

        line_idx += 6
    else:
        line_idx += 1

    if line_idx >= len(lines):
        break

lcm = math.lcm(*test_values)
for monkey in monkeys:
    monkey.Monkey_list = monkeys
    monkey.worry_lvl_manager = lcm


print(f"start")
for i, monkey in enumerate(monkeys):
    print(f"\tmonkey {i}: {monkey.held_items}")


for rounds in range(10000):
    for i, monkey in enumerate(monkeys):
        monkey.turn()

    if not rounds%100:
        print(f"turn: {rounds + 1}")

    if not rounds%1000:
        print(f"turn: {rounds + 1}")
        for i, monkey in enumerate(monkeys):
            print(f"\tmonkey {i}: {monkey.held_items}")

print("activity")
activity_list = []
for i, monkey in enumerate(monkeys):
    print(f"\tmonkey {i}: {monkey.inspection_counter}")
    activity_list.append(monkey.inspection_counter)

activity_list.sort()
print(f"Q11: {activity_list[-1]*activity_list[-2]}")