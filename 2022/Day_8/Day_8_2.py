import numpy as np

def scoring(n_idx, w_idx, forest):
    current_tree = forest[n_idx,w_idx]
    (NZ, WE) = forest.shape
    
    score = 1
    #check North
    trees_seenN = 0
    for i in reversed(range(0,n_idx)):
        trees_seenN = trees_seenN + 1
        if forest[i,w_idx] >= current_tree:
            break
    score = score * trees_seenN
    
    #check south
    trees_seenS = 0
    for i in range(n_idx+1, NZ):
        trees_seenS = trees_seenS + 1
        if forest[i,w_idx] >= current_tree:
            break
    score = score * trees_seenS
    
    #check West
    trees_seenW = 0
    for i in reversed(range(0,w_idx)):
        trees_seenW = trees_seenW + 1
        if forest[n_idx, i] >= current_tree:
            break
    score = score * trees_seenW
    
    #check East
    trees_seenE = 0
    for i in range(w_idx+1, WE):
        trees_seenE = trees_seenE + 1
        if forest[n_idx, i] >= current_tree:
            break
    score = score * trees_seenE
    
    if score < 0:
        print("score below 0")
        pass
    
        
    return score

file = open("input.txt", 'r')
lines = file.readlines()

forest = np.zeros((len(lines), len(lines[0])-1), dtype=np.int8)
scored_forest = np.zeros_like(forest,dtype=np.uint64)

for i, line in enumerate(lines):
    for j, char in enumerate(line[0:-1]):
        if not char == '\n':
            forest[i,j] = int(char)
        else:
            forest[i,j] = -1

print(forest)

(NZ, WE) = forest.shape

# no need to check the edges, as they are multiplied by 0
for n_idx in range(1,NZ-1):
    for w_idx in range(1,WE-1):
        scored_forest[n_idx,w_idx] = scoring(n_idx,w_idx,forest)
        
print(scored_forest)
print(f"Q8.2: {np.max(scored_forest)}")



# Horizontal check
# for n in range(NZ):
#     tallest_found = 0
#     for w in range(WE):
        
#         if forest[n,w] > tallest_found:
#             visible_forest[n,w] = 1
#             tallest_found = forest[n,w]
        
    
#     tallest_found = 0
#     for e in reversed(range(WE)):
#         if forest[n,e] > tallest_found:
#             visible_forest[n,e] = 1
#             tallest_found = forest[n,e]
        

# # Vertical check
    
# for w in range(WE):
#     tallest_found = 0
#     for n in range(NZ):
        
#         if forest[n,w] > tallest_found:
#             visible_forest[n,w] = 1
#             tallest_found = forest[n,w]
        
    
#     tallest_found = 0
#     for z in reversed(range(NZ)):
#         if forest[z,w] > tallest_found:
#             visible_forest[z,w] = 1
#             tallest_found = forest[z,w]
        

# print(visible_forest)

# print(f"Q8.1: {np.sum(visible_forest)}")