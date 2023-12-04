import numpy as np

file = open("input", 'r')
lines = file.readlines()

score_sum = 0

card_count = np.ones(len(lines),dtype=np.int32)

for idx, line in enumerate(lines):
    line = line.removesuffix('\n')
    winning_numbers, numbers_you_have = line.split(":")[1].split("|")

    winning_numbers = winning_numbers.split()
    numbers_you_have = numbers_you_have.split()

    matching_numbers = [number for number in numbers_you_have if number in winning_numbers]
    number_of_matching_numbers = len(matching_numbers)

    if number_of_matching_numbers> 0:
        card_score = 2 ** (number_of_matching_numbers - 1)
        score_sum += card_score

    for i in range(number_of_matching_numbers):
        card_count[idx+i+1] += card_count[idx]


print(f"part 1: {score_sum}")
print(f"part 2: {sum(card_count)}")
