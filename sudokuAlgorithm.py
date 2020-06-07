import time
def printgrid(megalist):
    for i in range (9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range (9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
        
            if j == 8:
                print(megalist[j][i]) 
            else:
                print(str(megalist[j][i]) + " ", end="")
#display megalist as a 9 * 9 "grid"
# printgrid(megalist)

# finding empty slot, iterate thru the grid
# maybe make it into a function

def find_empty(megalist):
	for i in range(9):
		for j in range(9):
			if megalist[i][j] == 0:
				return (i, j)
	return (-1, -1)
			
#set it a possible value

def countdown():
    start = 4
    while start > 0:
        start -= 1
        time.sleep(1)
        if start == 0:
            return False
        else:
            return True

def replace_empty(megalist):
    #countdown right here
    #if countdown == 0 and find_empty == true --> no solution found
    state = countdown()
    loc = find_empty(megalist)
    if state == False and loc != (-1, -1):  # no solution; might change == to "is" if it doesnt work
        return False

    x, y = loc
    if x == -1:
        return True
    for i in range(1,10):
        if validate(megalist, i, x, y):
            megalist[x][y] = i
            if replace_empty(megalist):
                return True
            megalist[x][y] = 0


    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True		


potent_number = 0
index_num = 0
def validate(megalist, potent_number, x, y): #, index_num):
    #check specified row that is determined thru value x
    row_check = potent_number
    for g in range(9):
        if row_check == megalist[x][g]:
            return False #as in there are duplicates
    
    #check specified col that is determined thru value y
    col_check = potent_number
    for p in range(9):
        if col_check == megalist[p][y]:
	            #print(potent_number)
            return False #as in there are duplicates

    #check grid
    modX = x // 3
    modY = y // 3
    grid_check = potent_number
    for w in range(modX * 3, modX * 3 + 3):
        for v in range(modY * 3, modY * 3 + 3):
            if grid_check == megalist[w][v]:
                return False
    return True

# replace_empty(megalist)
# print("-------------------------------")
# print("Solved board\n")
# printgrid(megalist)