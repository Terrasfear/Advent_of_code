file = open("input", 'r')
lines = file.readlines()


# part 1
total = 0
for _line in lines:
    digits = "".join(filter(str.isdigit, _line))
    if digits == '':
        continue
    value = int(digits[0] + digits[-1])
    total += value

print(f"part 1: {total}")

# part 2

def replace_to_digit(line):
    line = str.replace(line, "one",     "o1e")
    line = str.replace(line, "two",     "t2o")
    line = str.replace(line, "three",   "t3e")
    line = str.replace(line, "four",     "4")
    line = str.replace(line, "five",     "5e")
    line = str.replace(line, "six",      "6")
    line = str.replace(line, "seven",    "7")
    line = str.replace(line, "eight",   "e8t")
    line = str.replace(line, "nine",     "9e")
    return line


total = 0

for _line in lines:
    _line = replace_to_digit(_line)

    digits = "".join(filter(str.isdigit, _line))
    if digits == '':
        continue
    value = int(digits[0] + digits[-1])
    total += value

print(f"part 2: {total}")
