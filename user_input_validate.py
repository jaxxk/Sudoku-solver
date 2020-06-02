#potent number is now a user input number
#checking if that user num value already exists within the row, col, grid
#if so return the number location to "flag" that number location so user knows what number not to use
#return duplicate's coordinates and user inputs if there are duplicates
def validate(megalist, user_number, x, y):
    # check specified row that is determined thru value x
    row_check = user_number
    for g in range(9):
        if row_check == megalist[x][g]:
            # duplicate found in row --> return duplicate coords (w,v) and user input coord (x,y)
            return (x,g),(x,y)

    # check specified col that is determined thru value y
    col_check = user_number
    for p in range(9):
        if col_check == megalist[p][y]:
            # duplicate found in column --> return duplicate coords (w,v) and user input coord (x,y)
            return (p,y), (x,y)

    # check grid
    modX = x // 3
    modY = y // 3
    grid_check = user_number
    for w in range(modX * 3, modX * 3 + 3):
        for v in range(modY * 3, modY * 3 + 3):
            if grid_check == megalist[w][v]:
                #duplicate found in grid --> return duplicate coords (w,v) and user input coord (x,y)
                return (w,v), (x,y)
    return True