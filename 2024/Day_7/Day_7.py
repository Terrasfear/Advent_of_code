def findOperator(target, remaining_operands, progress, operators) -> bool:
    if progress > target:
        return False
    if not remaining_operands:
        if target == progress:
            return True
        else:
            return False

    for operator in operators:
        if operator == "+":
            operator_result = progress + remaining_operands[0]
        elif operator == "*":
            operator_result = progress * remaining_operands[0]
        elif operator == "||":
            operator_result = int(str(progress) + str(remaining_operands[0]))

        else:
            raise Exception(f"not implemented operator {operators}")

        if findOperator(target, remaining_operands[1:], operator_result, operators):
            return True

    return False


with open("Input", "r") as _file:
    _lines = _file.readlines()

total_calibration_result = 0
total_calibration_result_with_concat = 0
for line in _lines:
    line = line.removesuffix("\n").replace(":","").split(" ")
    result = int(line[0])
    operands = [int(operand) for operand in line[1:]]

    if findOperator(result, operands[1:], operands[0], ["+", "*"]):
        total_calibration_result += result
        total_calibration_result_with_concat += result
    elif findOperator(result, operands[1:], operands[0], ["||", "+", "*"]):
        total_calibration_result_with_concat += result

print(f"part 1: {total_calibration_result}")
print(f"part 2: {total_calibration_result_with_concat}")
