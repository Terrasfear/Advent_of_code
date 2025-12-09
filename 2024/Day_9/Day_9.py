class Block:
    def __init__(self, idx: int):
        self.id = idx


class File:
    def __init__(self, length, id, start):
        self.length = length
        self.id = id
        self.start = start

    def checksumValue(self):
        return sum([self.start + i for i in range(self.length)]) * self.id

    def __len__(self):
        return self.length

    def print(self):
        print(f"{self.id}" * self.length, end="")


class FreeSpace:
    def __init__(self, length, start):
        self.length = length
        self.start = start

    def checksumValue(self):
        return 0

    def __len__(self):
        return self.length

    def print(self):
        print("." * self.length, end="")

    def overwrite(self, overwritten_length):
        self.start += overwritten_length
        self.length -= overwritten_length
        return self.length > 0


class DiskBlockBased:
    def __init__(self):
        self.disk = []

    def extend(self, it):
        self.disk.extend(it)

    def print(self):
        for block in self.disk:
            if isinstance(block, Block):
                print(block.id, end="")
            elif isinstance(block, str):
                print(block, end="")
        print()

    def popBlock(self):
        while isinstance(self.disk[-1], str):
            self.disk.pop()
        return self.disk.pop()

    def prune(self):
        while isinstance(self.disk[-1], str):
            self.disk.pop()

    def refactor(self):
        idx = 0
        while idx < self.__len__():
            if isinstance(self.disk[idx], str):
                self.disk[idx] = self.popBlock()
                self.prune()
            idx += 1
        self.prune()

    def __len__(self):
        return len(self.disk)

    def checksum(self):
        return sum([idx * block.id for (idx, block) in enumerate(self.disk) if isinstance(block, Block)])


class DiskFileBased:
    def __init__(self):
        self.disk = []
        self.disk_size = 0

    def add(self, file_id, file_size):
        if isinstance(file_id, int):
            self.disk.append(File(file_size, file_id, self.disk_size))
        else:
            self.disk.append(FreeSpace(file_size, self.disk_size))

        self.disk_size += file_size

    def prune(self):
        while isinstance(self.disk[-1], FreeSpace):
            self.disk.pop()

    def print(self):
        for file in self.disk:
            file.print()
        print()

    def moveFile(self, source_file: File, target_space: FreeSpace):
        file_idx_on_disk = self.disk.index(source_file)
        free_space_idx_on_disk = self.disk.index(target_space)

        self.disk[file_idx_on_disk] = FreeSpace(len(source_file), source_file.start)
        self.disk.insert(free_space_idx_on_disk, source_file)

        source_file.start = target_space.start
        target_space.overwrite(len(source_file))

    def refactor(self):
        files_to_reorganise = [file for file in self.disk if isinstance(file, File)]

        num_files = len(files_to_reorganise)

        while files_to_reorganise:
            if len(files_to_reorganise) %50 == 0:
                print(f"{len(files_to_reorganise)}/{num_files}")

            file_to_reorganise = files_to_reorganise.pop()
            free_spaces = [free_space for free_space in self.disk
                           if isinstance(free_space, FreeSpace)
                           and len(free_space) >= len(file_to_reorganise)
                           and free_space.start < file_to_reorganise.start]
            if free_spaces:
                self.moveFile(file_to_reorganise, free_spaces[0])

    def checksum(self):
        return sum(file.checksumValue() for file in self.disk)


with open("Input", "r") as _file:
    _disk_map = _file.readlines()[0].removesuffix("\n")

    _disk1 = DiskBlockBased()
    _disk2 = DiskFileBased()
    _id = 0
    for _idx, size in enumerate(_disk_map):
        if _idx & 1:
            _disk1.extend(["."] * int(size))
            _disk2.add(".", int(size))
        else:
            _disk1.extend([Block(_id) for _ in range(int(size))])
            _disk2.add(_id, int(size))
            _id += 1

_disk1.refactor()
_disk2.refactor()

print(f"Part 1: {_disk1.checksum()}")
print(f"Part 2: {_disk2.checksum()}")
