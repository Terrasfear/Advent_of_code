import re
import math
import copy

file = open("input", 'r')
lines = file.readlines()

command_list = []
# scan input
for i, line in enumerate(lines):
    # finding stack list
    if re.search("^\s1\s",line):
        stacks_number_line = i
        stacks9000 = [[] for _ in range(int(line[-2]))]

        #build stacks
        for j in reversed(range(stacks_number_line)):
            crates = list(re.finditer('\[[A-Z]\]',lines[j]))
            if not crates:
                continue

            for crate in crates:
                stack_idx = math.floor(crate.span()[0]/4)
                stacks9000[stack_idx].append(crate.group()[1])

        stacks9001 = copy.deepcopy(stacks9000)
        continue

    # execute commands (CrateMover 9000)
    if re.search("^move",line):
        cmd = re.findall('(\d+)',line)
        cmd = list(map(int, cmd))

        # CrateMover 9000
        for _ in range(cmd[0]):
            stacks9000[cmd[2] - 1].append(stacks9000[cmd[1] - 1][-1])
            stacks9000[cmd[1] - 1].pop()
            pass

        # CrateMover 9001
        stacks9001[cmd[2] - 1].extend(stacks9001[cmd[1] - 1][(-1*cmd[0]):])
        del stacks9001[cmd[1] - 1][(-1*cmd[0]):]
        pass

# read top
msg9000 = ''
for stack in stacks9000:
    msg9000 = msg9000 + stack[-1]

msg9001 = ''
for stack in stacks9001:
    msg9001 = msg9001 + stack[-1]

print(f"Q5.1: {msg9000}")
print(f"Q5.2: {msg9001}")
