
with open(f"Input", 'r') as _file:
    _lines = _file.readlines()

    listLeft = []
    listRight = []

    for line in _lines:
        listSplit = line.removesuffix("\n").split("   ")
        listLeft.append(int(listSplit[0]))
        listRight.append(int(listSplit[1]))

    listLeft.sort()
    listRight.sort()

    differences = [abs(listLeft[i] - listRight[i]) for i in range(len(listLeft))]
    similarity = [listLeft[i] * listRight.count(listLeft[i]) for i in range(len(listLeft))]

    print(f"Part 1: {sum(differences)}")
    print(f"Part 2: {sum(similarity)}")