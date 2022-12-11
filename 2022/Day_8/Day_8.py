import numpy as np

file = open("input.txt", 'r')
lines = file.readlines()

forest = np.zeros((len(lines), len(lines[0])-1), dtype=np.int8)
visible_forest = np.zeros_like(forest)


for i, line in enumerate(lines):
    for j, char in enumerate(line[0:-1]):
        if not char == '\n':
            forest[i,j] = int(char)
        else:
            forest[i,j] = -1
    
        if i == 0 or i == len(lines)-1 or j == 0 or j == len(line)-2:
            visible_forest[i,j] = 1
        
print(forest)
print(visible_forest)

(NZ, WE) = forest.shape
# Horizontal check
for n in range(NZ):
    tallest_found = 0
    for w in range(WE):
        
        if forest[n,w] > tallest_found:
            visible_forest[n,w] = 1
            tallest_found = forest[n,w]
        
    
    tallest_found = 0
    for e in reversed(range(WE)):
        if forest[n,e] > tallest_found:
            visible_forest[n,e] = 1
            tallest_found = forest[n,e]
        

# Vertical check
    
for w in range(WE):
    tallest_found = 0
    for n in range(NZ):
        
        if forest[n,w] > tallest_found:
            visible_forest[n,w] = 1
            tallest_found = forest[n,w]
        
    
    tallest_found = 0
    for z in reversed(range(NZ)):
        if forest[z,w] > tallest_found:
            visible_forest[z,w] = 1
            tallest_found = forest[z,w]
        

print(visible_forest)

print(f"Q8.1: {np.sum(visible_forest)}")