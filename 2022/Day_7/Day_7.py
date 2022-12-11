import re


class Tree:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.parent = None
        self.leaf = True

        self.files = {}
        self.internal_size = 0
        self.upward_size = 0

    def add_parent(self, parent):
        self.parent = parent

    def add_child(self, child):
        self.children.update({child.name: child})
        self.leaf = False

        child.add_parent(self)

    def add_file(self, file):
        self.files.update(file)

    def increase_upward_size(self, size):
        self.upward_size = self.upward_size + size

    def compute_internal_size(self):
        self.internal_size = sum(self.files.values())

    def down_propagate(self, size=None):
        if size == None:
            size = self.internal_size

        if not self.parent == None:
            self.parent.increase_upward_size(size)
            self.parent.down_propagate(size)

        # propagates downwards until root
        # per parent:
        #   add size to upward_size
        #   call down_propagate with size

        # call this when finding a leaf node (i.e. no children)
        pass


def find_sizes(node: Tree, folder_list: list, max_size):
    print(f"sizing {node.name}")
    dir_size = node.internal_size + node.upward_size

    if max_size == None or dir_size <= max_size:
        folder_list.append(dir_size)

    if len(node.children):
        for child in node.children:
            find_sizes(node.children[child], folder_list, max_size)


file = open("input", 'r')
lines = file.readlines()

# building tree.
root = Tree("root")
current = None

dir_list = []
processing_ls = False
for line in lines:
    if processing_ls:
        if re.search("^\$", line):
            print("reading ls done")
            processing_ls = False
            print(f"compute internal size of {current.name}")
            current.compute_internal_size()

            print(f"downpropagate {current.name}")
            current.down_propagate()

        if re.search("^dir", line):
            print(f"\tadding dir {line[4:-1]} to {current.name}")
            current.add_child(Tree(line[4:-1]))
            continue
        if re.search("^\d+", line):
            regex_line = re.search("(\d+)\s([\w|\.]+)", line)
            file_size = int(regex_line.group(1))
            file_name = regex_line.group(2)
            print(f"\tadding file {file_name} of size {file_size} to {current.name}")
            current.add_file({file_name: file_size})
            continue

    if not processing_ls:
        if re.search("^\$ cd /", line):
            print("enter root")
            current = root
            continue
        if re.search("^\$ cd \.\.", line):
            print(f"return to {current.parent.name}")
            current = current.parent
            continue
        if re.search("^\$ cd", line):
            print(f"enter {line[5:-1]}")
            current = current.children[line[5:-1]]
            continue
        if re.search("^\$ ls", line):
            print("reading ls")
            processing_ls = True
            continue

print("\nTree done\n")
# check which folders are smaller than 100000
folder_list = []
max_size = 100000

find_sizes(root, folder_list, None)

folder_list.sort()

below_max_list = [i for i in folder_list if i <= max_size]

print(below_max_list)

disk_size = 70000000
required_size = 30000000

remaining_size = disk_size - (root.internal_size + root.upward_size)
missing_size = required_size - remaining_size

print(f"Q7.1: {sum(below_max_list)}")
print(f"Q7.2: {[i for i in folder_list if i >= missing_size][0]}")
