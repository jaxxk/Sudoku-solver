#potent number is now a user input number
#checking if that user num value already exists within the row, col, grid
#if so add it onto empty list location_list which will hold all the x,y locations of duplicates
def validate(megalist, user_number, x, y):
    location_list = []
    # check specified row that is determined thru value x
    row_check = user_number
    for g in range(9):
        if row_check == megalist[x][g]:
            # adding tuple of row duplicate (x,g)
            location_list.append((x,g))

    # check specified col that is determined thru value y
    col_check = user_number
    for p in range(9):
        if col_check == megalist[p][y]:
            # adding tuple of column duplicate (p,y)
            location_list.append((p,y))

    # check grid
    modX = x // 3
    modY = y // 3
    grid_check = user_number
    for w in range(modX * 3, modX * 3 + 3):
        for v in range(modY * 3, modY * 3 + 3):
            if grid_check == megalist[w][v]:
                # adding tuple of grid duplicate (w,v)
               location_list.append(w,v)
                
    return location_list