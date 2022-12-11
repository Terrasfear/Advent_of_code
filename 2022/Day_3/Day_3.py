def item2value(item: str):
    if len(item) != 1:
        print("ERROR, multiple characters")
        quit()

    ascii_value = ord(item)

    if ascii_value >= ord("a") or ascii_value >= ord("z"):
        return ascii_value - ord("a") + 1
    elif ascii_value >= ord("A") or ascii_value >= ord("Z"):
        return ascii_value - ord("A") + 27
    else:
        print("ERROR, out of char range")
        quit()


plan = open("input", "r")
bags = plan.readlines()

count = 0
for bag in bags:
    c1 = bag[0:int(len(bag)/2)]
    c2 = bag[int(len(bag)/2):-1]
    # print(f"{c1}\t\t{len(c1)}\n{c2}\t\t{len(c2)}\n\n")
    fault = ''.join(set(c1).intersection(c2))
    if len(fault) != 1:
        print(f"ERROR finding double value: word {bag}, c1 {c1}, c2 {c2}")
        quit()
    count = count + item2value(fault)

badge_count = 0
for i in range(0, len(bags), 3):
    b1 = bags[i]
    b2 = bags[i+1]
    b3 = bags[i+2]

    badge = ''.join(set(b1).intersection(b2).intersection(b3))
    badge = badge.strip('\n')
    badge_count = badge_count + item2value(badge)

print(f"Q3.1: sum = {count}")
print(f"Q3.2: sum = {badge_count}")