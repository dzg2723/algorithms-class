# Darren Good
# 24-Mar-2019
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

def bestYieldBottomUp(layout):

    # Find dimensions of gold mine layout
    row_dim = len(layout)
    col_dim = len(layout[0])
    print(row_dim, col_dim)

    # Create a matrix to store optimal solutions
    Memo = []
    for row in range(row_dim):
        Memo.append([])
        for col in range(col_dim):
            Memo[row].append(None)

    # Solve subproblems bottom-up
    for col in range(col_dim):
        for row in range(row_dim):

            if (col > 0):
                
                # Find Opt of (row-1, col-1)
                gold_up = 0
                if (row > 0):
                    gold_up = Memo[row-1][col-1]

                # Find Opt of (row, col-1)
                gold_left = Memo[row][col-1]

                # Find Opt of (row+1, col-1)
                gold_down = 0
                if (row < row_dim-1):
                    gold_down = Memo[row+1][col-1]

                # Yield of the best path to this point
                most_gold = layout[row][col] + max(gold_up, gold_left, gold_down)
                
            else:

                # Starting point -- no previous path to consider
                most_gold = layout[row][col]

            # Store the optimal solution
            Memo[row][col] = most_gold

    # Find which destination yields the most gold
    best_yield = 0
    for row in Memo:
        best_yield = max(best_yield, row[-1])
        
    return best_yield

# Generate a random test case
mat = randomMat()

# Start timer
start = time.time()

# Find and print the maximum yield
print(bestYieldBottomUp(mat))

# Display processing time
end = time.time()
print("Time: " + str(end-start))
    
