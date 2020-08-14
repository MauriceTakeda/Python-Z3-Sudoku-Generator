from z3 import *
import random

#----------Functions----------

def generateSudoku(s):
    """Generates filled out sudoku board and returns that board as a 9x9 array"""
    # Convert solver result into an array of integers
    m = s.model()
    b = [str(m[y]) for y in x]
    b = [int(num) for num in b]
    # Store those integers in a 9x9 array
    Board = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            Board[i][j] = b[9*i+j]
    # Return the 9x9 array
    return Board

def randomSudoku(s):
    """Returns a clause that blocks the current solution"""
    m = s.model()
    return Or([y != m[y] for y in x])

def reduceSudoku(Board):
    """Reduces numbers on the board to create starting puzzle"""
    row = random.randrange(9)
    col = random.randrange(9)
    while(Board[row][col] == 0):
        row = random.randrange(9)
        col = random.randrange(9)
    prevnum = Board[row][col]
    Board[row][col] = 0
    return Board, row, col, prevnum

def printSudoku(Board):
    """Prints sudoku board given a 9x9 integer array"""
    print("-------------------------")
    for i in range(9):
        for j in range(9):
            if(j%9 == 0):
                print("|", end=" ")
            print(Board[i][j], end=" ")
            if((j-2)%3 == 0):
                print("|", end=" ")
        print("")
        if((i-2)%3 == 0):
            print("-------------------------")

def inputSudoku():
    """Allows the user to input values to board"""
    row = input("Choose a row 1-9: ")
    row = int(row) - 1
    col = input("Choose a col 1-9: ")
    col = int(col) - 1
    val = input("Choose a value 1-9: ")
    val = int(val)
    return row, col, val

def checkSudoku(Board):
    """Checks if input will lead to the correct solution"""
    out = 0
    c = Solver()
    x = [Int('x%s' % (i)) for i in range(81)]
    for i in range(0, 81, 9):
        for j in range(9):
            if(Board[i//9][j] != 0):
                c.add(x[i+j] == Board[i//9][j])
    for i in range(0, 81, 9):
        for j in range(9):
            if(Board[i//9][j] != 0):
                c.add(x[i+j] == Board[i//9][j])
    for i in range(0, 81, 9):
        c.add(Distinct([x[i+j] for j in range(9)]))
    for i in range(9):
        c.add(Distinct([x[i+j] for j in range(0, 81, 9)]))
    for i in range(81):
        c.add(And(x[i] > 0, x[i] < 10))
    for i in range(0, 54, 27):
        for j in range(0, 6, 3):
            c.add(Distinct(x[0+i+j], x[1+i+j], x[2+i+j], x[9+i+j], x[10+i+j], x[11+i+j], x[18+i+j], x[19+i+j], x[20+i+j]))
    result = c.check()
    if result == sat:
        print("Good choice!")
        out = 1
    else:
        print('ERROR: The number you have placed will not lead to the correct solution')
        out = 0
    c.reset()
    return out
    
def completeSudoku(Board):
    """Checks if board is filled in"""
    for i in range(9):
        for j in range(9):
            if(Board[i][j] == 0):
                return 0
    return 1

# ---------------Sudoku Rules----------------

s = Solver()
x = [Int('x%s' % (i)) for i in range(81)]
# Rows
for i in range(0, 81, 9):
    s.add(Distinct([x[i+j] for j in range(9)]))
# Columns
for i in range(9):
    s.add(Distinct([x[i+j] for j in range(0, 81, 9)]))
# Subsections
for i in range(0, 54, 27):
    for j in range(0, 6, 3):
        s.add(Distinct(x[0+i+j], x[1+i+j], x[2+i+j], x[9+i+j], x[10+i+j], x[11+i+j], x[18+i+j], x[19+i+j], x[20+i+j]))
# Values
for i in range(81):
    s.add(And(x[i] > 0, x[i] < 10))

#----------Generate random Sudoku board----------

i = random.randrange(3)
j = 0
result = s.check()
if result == sat:
    while(j<i):
        s.check(randomSudoku(s))
        j = j + 1
Board = generateSudoku(s)
#----------Reduce numbers on board to create initial puzzle----------

PrevBoard = Board
Board, row, col, prevnum = reduceSudoku(Board)
for i in range(0, 81, 9):
        for j in range(9):
            if(Board[i//9][j] != 0):
                s.add(x[i+j] == Board[i//9][j])
result = s.check()
while(s.check(randomSudoku(s)) == unsat):
    PrevBoard = Board
    Board, row, col, prevnum = reduceSudoku(Board)
    s.reset()
    for i in range(0, 81, 9):
        for j in range(9):
            if(Board[i//9][j] != 0):
                s.add(x[i+j] == Board[i//9][j])
    for i in range(0, 81, 9):
        s.add(Distinct([x[i+j] for j in range(9)]))
    for i in range(9):
        s.add(Distinct([x[i+j] for j in range(0, 81, 9)]))
    for i in range(81):
        s.add(And(x[i] > 0, x[i] < 10))
    for i in range(0, 54, 27):
        for j in range(0, 6, 3):
            s.add(Distinct(x[0+i+j], x[1+i+j], x[2+i+j], x[9+i+j], x[10+i+j], x[11+i+j], x[18+i+j], x[19+i+j], x[20+i+j]))
    result = s.check()
Board = PrevBoard

#--------------------Gameplay--------------------
complete = 0
print("----------SUDOKU----------")
printSudoku(Board)
while(complete == 0):
    i = 0
    j = 0
    while(i == 0):
        row, col, val = inputSudoku()
        if((val > 9) or (val < 1) or (row < 0) or (row > 8) or (col < 0) or (col > 8)):
            print("Error: Inputs out of bounds")
        elif(Board[row][col] == 0):
            Board[row][col] = val
            j = checkSudoku(Board)
            if(j == 1):
                i = 1
            else:
                Board[row][col] = 0
        else:
            print("ERROR: Please enter a position that is not already filled!")
        print("-----SUDOKU-----")
        printSudoku(Board)
    i = 0
    complete = completeSudoku(Board)
print("----------Puzzle Solved----------")
