# Darren Good
# 20-Mar-2019
# Python 2.6.3
# Algorithms

import random, time

def randomMat():
    mat = []
    num_of_rows = random.randint(2,100)
    num_of_cols = random.randint(2,100)
    for row in range(num_of_rows):
        mat.append([])
        for col in range(num_of_cols):
            mat[row].append(random.randint(1,100))
    return mat
    
def bestYieldTopDown(row, col):

    # Break Recursion if looking for yield in non-existant field.
    if (row < 0 or col < 0 or row >= row_dim or col >= col_dim):
        return 0

    # Find Opt of (row-1, col-1)
    if (row > 0 and col > 0):
        if not Memo[row-1][col-1]:
            Memo[row-1][col-1] = bestYieldTopDown(row-1, col-1)
        prev_cell_one = Memo[row-1][col-1]
    else:
        prev_cell_one = 0

    
    # Find Opt of (row, col-1)
    if (col > 0):
        if not Memo[row][col-1]:
            Memo[row][col-1] = bestYieldTopDown(row, col-1)
        prev_cell_two = Memo[row][col-1]
    else:
        prev_cell_two = 0


    # Find Opt of (row+1, col-1)
    if (row < row_dim-1 and col > 0):
        if not Memo[row+1][col-1]:
            Memo[row+1][col-1] = bestYieldTopDown(row+1, col-1)
        prev_cell_three = Memo[row+1][col-1]
    else:
        prev_cell_three = 0

    # Largest yield up to current location
    mostGold = max(prev_cell_one, prev_cell_two, prev_cell_three) + mat[row][col]

    # Memoize and return largest yield
    Memo[row][col] = mostGold
    return Memo[row][col]


# Generate a random test case
mat = randomMat()

# Start timer
start = time.time()

# Find dimensions of gold mine layout
row_dim = len(mat)
col_dim = len(mat[0])

# Create a matrix to store optimal solutions
Memo = []
for row in range(row_dim):
    Memo.append([])
    for col in range(col_dim):
        Memo[row].append(None)

# Find the largest gold yield from end destinations
finalGold = 0
for x in range(4):
    finalGold = max(finalGold, bestYieldTopDown(x, col_dim-1))

# Print the maximum yield
print(finalGold)

# Display processing time
end = time.time()
print("Time: " + str(end-start))
    
