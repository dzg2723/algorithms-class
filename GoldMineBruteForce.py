# Darren Good
# 20-Mar-2019
# Python 2.6.3
# Algorithms

import random, time

def randomMat():
    mat = []
    num_of_rows = 5
    num_of_cols = 5
    for row in range(num_of_rows):
        mat.append([])
        for col in range(num_of_cols):
            mat[row].append(random.randint(1,100))
    return mat
    
def bestYieldBruteForce(layout, row, col):

    # Return empty list if dimensions are outside mine layout
    if (row < 0 or col < 0 or row >= row_dim):
        return []

    # Starting point -- no previous path to consider
    if (col == 0):
        return [layout[row][col]]

    # Check all possible paths up to this point
    paths_up = bestYieldBruteForce(layout, row-1, col-1)
    paths_left = bestYieldBruteForce(layout, row, col-1)
    paths_down = bestYieldBruteForce(layout, row+1, col-1)

    # Add this field's gold to each possible path
    previous_paths = paths_up + paths_left + paths_down
    possible_paths = []
    for i in previous_paths:
        possible_paths.append(layout[row][col] + i)

    # Return all paths that contain this field
    return possible_paths

# Generate a random test case
mat = randomMat()

# Start timer
start = time.time()

# Find dimensions of gold mine layout
row_dim = len(mat)
col_dim = len(mat[0])

# Collect a list of yields from every possible path through the gold mine
all_yields = []
for row in range(row_dim):
    all_yields += bestYieldBruteForce(mat, row, col_dim-1)
    
# Print the maximum yield
print(max(all_yields))
print("Length: " + str(len(all_yields)))

# Display processing time
end = time.time()
print(end-start)

    









    
