import json

file = open("Input", 'r')
lines = file.readlines()


def compare_lists(left, right) -> int:
    l_len = len(left)
    r_len = len(right)
    l_idx = 0
    r_idx = 0
    while True:
        # check if we're running out of items
        if l_idx >= l_len and r_idx >= r_len:
            # both out of range => inconclusive
            return 0
        elif l_idx >= l_len and r_idx < r_len:
            # left ran out first -> correct
            return 1
        elif l_idx < l_len and r_idx >= r_len:
            # right ran out first -> incorrect
            return -1

        # check item types
        if isinstance(left[l_idx],list) and isinstance(right[r_idx], list):
            # both lists, go deeper
            result = compare_lists(left[l_idx], right[r_idx])
            if result:
                # conclusive result found, forward
                return result

        elif isinstance(left[l_idx], int) and isinstance(right[r_idx], int):
            # both ints, compare values
            if left[l_idx] < right[r_idx]:
                return 1
            elif left[l_idx] > right[r_idx]:
                return -1
        else:
            # one of the two is not a list, convert to list and go deeper
            if not isinstance(left[l_idx], list):
                result = compare_lists([left[l_idx]], right[r_idx])
                if result:
                    # conclusive result found, forward
                    return result
            elif not isinstance(right[r_idx], list):
                result = compare_lists(left[l_idx], [right[r_idx]])
                if result:
                    # conclusive result found, forward
                    return result

        l_idx += 1
        r_idx += 1

    # no conclusion
    return 0


# convert to packets
packets = []
for line in lines:
    if not line[0] == '\n':
        packets.append(json.loads(line))

#### Q1
num_comparisons = len(packets)//2

idx_sum = 0
for i in range(num_comparisons):
    left = packets[i*2]
    right = packets[i*2+1]

    print(f"pair nr {i+1}")
    print(f"{left=}")
    print(f"{right=}")
    result = compare_lists(left,right)

    if result == 1:
        print("correct order")
        idx_sum += i+1
    elif result == -1:
        print("wrong order")
    else:
        print("inconclusive")
    print()

print(f"sum = {idx_sum}")

####Q2
packets.extend([[[2]], [[6]]])

# bubble sort
while True:
    swapped = False

    for i in range(len(packets) - 1):
        result = compare_lists(packets[i], packets[i+1])

        if result == -1:
            packets[i], packets[i+1] = packets[i+1], packets[i]
            swapped = True

    if not swapped:
        break

decoder_key = 1
for i, packet in enumerate(packets):
    if packet == [[2]] or packet == [[6]]:
        decoder_key *= (i+1)

    print(packet)

print(f"{decoder_key=}")