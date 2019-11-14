problem = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def print_prob(prob):
    for row in range(0,9):
        if row % 3 == 0 and row != 0:
            print("- "*11)
        for col in range(0,9):
            if col % 3 == 0 and col != 0:
                print("| ",end="")
            print(str(prob[row][col])+" ",end="")
        print()


def find_next_empty(prob):
    for row in range(0,9):
        for col in range(0,9):
            if prob[row][col] == 0:
                return(row,col)
    return None

def isvalid(prob, num, pos):
    ##pos is index of mtrix and num is munber to b inserted
    ##check row 
    for n in range(len(prob[0])):
        if prob[pos[0]][n] == num and pos[1] != (num-1):
            return False
    ##check col
    for n in range(len(prob[0])):
        if prob[n][pos[1]] == num and pos[0] != (num-1):
            return False
    ##check box
    
    x_box = pos[0] // 3
    y_box = pos[1] // 3 
    
    #print(x_box,y_box)
    for row_box in range(x_box*3,x_box*3+3):
        for col_box in range(y_box*3,y_box*3+3):
            if num == prob[row_box][col_box] and pos!=(row_box,col_box):
                return False
    return True

def solve(prob):
    print_prob(prob)
    print()
    find_empty = find_next_empty(prob)
    if not find_empty:
        return True
    else:
        row,col = find_empty
    
    for n in range(1,10):
        if isvalid(prob,n,(row,col)):
            prob[row][col] = n

            if solve(prob):
                return True
            
            prob[row][col] = 0
    ### if none of the number satisfies
    return False

print("_________________\n Problem\n_________________")
solve(problem)
print("_________________\n Solution\n_________________")
print_prob(problem)
