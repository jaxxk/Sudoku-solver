from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
from lxml import html
from tkinter import *
from tkinter import messagebox
from playsound import playsound
from PIL import ImageTk

from sudokuAlgorithm import *
from sudokuScreen import *
from sudokuValidate import *

import copy
import math
import pytesseract as tess
import PIL.Image, PIL.ImageEnhance
import requests
import time
import webbrowser

tess.pytesseract.tesseract_cmd = r'assets\Tesseract-OCR\tesseract.exe'

# UI Configurations
gridXOffset = 15
gridYOffset = 50
buttonGap = 12
buttonHeight = 30
buttonPadding = 4
buttonYOffset = 51
buttonTempFix = " "

# Image Processing Configurations
psmSetting = 10
paddingSetting = 3 # number of pixels to ignore from edges

app = Tk()

class mainScreen:
    altered, board, cells, completed, conflicted, cursor, original, solved = ([] for i in range(8))
    levels = ["Beginner", "Intermediate                ", "Advanced", "Expert", "Master"]

    psms = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    selected = () # x, y

    dropDown, dropDown2 = (StringVar(app) for i in range(2))
    emptyBD, emptyBT, solutionBD, solutionBT = (None for i in range(4))


    # tries to solve a given puzzle within n seconds
    def attemptToFindSolution(self):
        self.board = copy.deepcopy(self.altered)
        replace_empty(self.board)
        counter = 0
        for x in range(9):
            for y in range(9):
                if self.board[x][y] == 0:
                    return False

        self.original = copy.deepcopy(self.altered)
        return True


    # Creates a new board using image capture
    def captureBoard(self):
        prompt = messagebox.askyesno("Confirmation", "Would you like to generate a new board?\nCurrernt board will be discarded.")
        if not prompt:
            return

        loadingLabel = Label(app, text = "The image is processing..", font = ("SF Pro Display", 11), width = 44, height = 20)
        loadingLabel.place(x = gridXOffset, y = gridYOffset)

        messagebox.showinfo("Information", "Please capture the 9x9 Sudoku Grid from edge to edge.")

        self.board.clear()
        self.completed.clear()
        self.conflicted.clear()
        self.solved.clear()

        cap = QtWidgets.QApplication(sys.argv)
        window = screenCap()
        window.show()
        cap.aboutToQuit.connect(cap.deleteLater)
        cap.exec()

        img = window.getImg()
        dimOfGrid = (img.width + img.height) // 2 # assume this as the size of 9x9 grid for now
        padding = dimOfGrid // 100 + paddingSetting # number of pixels to ignore from edges
        
        for x in range(9):
            self.board.append([])
            self.completed.append([])
            self.conflicted.append([])
            for y in range(9):
                # calculate boundaries for each of the 81 squares
                tleft = int(img.width * x / 9) + padding
                tright = int(img.height * y / 9) + padding
                bleft = int(img.width * (x + 1) / 9) - padding
                bright = int(img.height * (y + 1) / 9) - padding

                tempImg = img.crop((tleft, tright, bleft, bright))
                tempNum = tess.image_to_string(tempImg, lang='eng', config='--psm {}'.format(psmSetting))
                num = ''.join([i for i in tempNum if i.isdigit()]) # eliminate any non-digit characters from string
                if not num:
                    num = 0
                self.board[x].append(num)
                self.completed[i].append(0)
                self.conflicted[i].append(0)

        loadingLabel.destroy()

        self.altered, self.original = (copy.deepcopy(self.board) for i in range(2))

        for x in range(9):
                for y in range(9):
                    newImage = self.selectImage(x, y, self.board[x][y])
                    photo = ImageTk.PhotoImage(newImage)
                    self.cells[x][y].config(image = photo)
                    self.cells[x][y].image = photo

        if (self.solutionBT.cget('text') == " Hide solution "):
            self.solutionBD.config(width = 105)
            self.solutionBT.config(text = " Show solution ")


    def checkForCompletions(self, x, y, noSound):
        row, col, grid = (True for i in range(3))
        comp = True

        for i in range(9):
            if self.altered[x][i] == 0 or self.conflicted[x][i] == 1:
                row = False
            if self.altered[i][y] == 0 or self.conflicted[i][y] == 1:
                col = False
        modX = x // 3
        modY = y // 3
        for w in range(modX * 3, modX * 3 + 3):
            for v in range(modY * 3, modY * 3 + 3):
                if self.altered[w][v] == 0 or self.conflicted[w][v] == 1:
                    grid = False

        if row or col or grid:
            # Play the animation
            for i in range(1, 10):
                if row:
                    for r in range(9):
                        if int(self.altered[x][r]) == i:
                            self.completed[x][r] = 1
                            self.updateImage(x, r)
                            if not noSound:
                                playsound(self.selectSound(i, "dul"), block = False)
                if col:
                    for c in range(9):
                        if int(self.altered[c][y]) == i:
                            self.completed[c][y] = 1
                            self.updateImage(c, y)
                            if not noSound:
                                playsound(self.selectSound(i, "glo"), block = False)
                if grid:
                    modX = x // 3
                    modY = y // 3
                    for w in range(modX * 3, modX * 3 + 3):
                        for v in range(modY * 3, modY * 3 + 3):
                            if int(self.altered[w][v]) == i:
                                self.completed[w][v] = 1
                                self.updateImage(w, v)
                                if not noSound:
                                    playsound(self.selectSound(i, "cel"), block = False)
                if i >= 9:
                    for a in range(9):
                        for b in range(9):
                            if self.completed[a][b] == 0:
                                comp = False
                                break
                    if comp:
                        if not noSound:
                            playsound("assets/audio/complete.wav", block = False)
                app.update_idletasks()
                time.sleep(0.06)


    def checkForConflicts(self, x, y):
        self.conflicted[x][y] = 0 # Mark itself as non-conflicted
        conflictsFound = False; # Value to return

        ogValue, checkAgainst = (int(self.altered[x][y]) for i in range(2))
        if checkAgainst == 0:
            checkAgainst = -1

        # check specified row that is determined thru value x
        for g in range(9):
            if y == g:
                continue
            if self.conflicted[x][g] == 1:
                self.altered[x][y] = -1
                self.checkForConflicts(x, g)
                self.altered[x][y] = ogValue
            if checkAgainst == int(self.altered[x][g]):
                self.conflicted[x][g] = 1
                self.updateImage(x, g)
                conflictsFound = True

        # check specified col that is determined thru value y
        for p in range(9):
            if x == p:
                continue
            if self.conflicted[p][y] == 1:
                self.altered[x][y] = -1
                self.checkForConflicts(p, y)
                self.altered[x][y] = ogValue
            if checkAgainst == int(self.altered[p][y]):
                # adding tuple of column duplicate (p,y)
                self.conflicted[p][y] = 1
                self.updateImage(p, y)
                conflictsFound = True

        # check grid
        modX = x // 3
        modY = y // 3
        for w in range(modX * 3, modX * 3 + 3):
            for v in range(modY * 3, modY * 3 + 3):
                if w == x and y == v:
                    continue
                if self.conflicted[w][v] == 1:
                    self.altered[x][y] = -1
                    self.checkForConflicts(w, v)
                    self.altered[x][y] = ogValue
                if checkAgainst == int(self.altered[w][v]):
                    # adding tuple of grid duplicate (w,v)
                    self.conflicted[w][v] = 1
                    self.updateImage(w, v)
                    conflictsFound = True
        
        if conflictsFound:
            self.conflicted[x][y] = 1

        self.updateImage(x, y)
        return conflictsFound


    # Fetches a new random table of given difficulty and replaces board
    def emptyBoard(self):
        if (self.emptyBT.cget('text') == " Generate empty board "):
            prompt = messagebox.askyesno("Confirmation", "Would you like to empty the board?\nCurrernt board will be discarded.")
            if not prompt:
                return
            messagebox.showinfo("Information", "After manually inputting the numbers, press the same button again to check it is a valid Sudoku board.")
            
            self.board.clear()
            self.completed.clear()
            self.conflicted.clear()
            self.solved.clear()

            for i in range(9):
                self.board.append([])
                self.completed.append([])
                self.conflicted.append([])
                for j in range(9):
                    self.board[i].append(0)
                    self.completed[i].append(0)
                    self.conflicted[i].append(0)
            
            for x in range(9):
                    for y in range(9):
                        newImage = self.selectImageButForEmptyBoardSoItRendersImagesCorrectly(x, y, self.board[x][y])
                        photo = ImageTk.PhotoImage(newImage)
                        self.cells[x][y].config(image = photo)
                        self.cells[x][y].image = photo

            self.altered, self.original = (copy.deepcopy(self.board) for i in range(2))

            if (self.solutionBT.cget('text') == " Hide solution "):
                self.solutionBD.config(width = 105)
                self.solutionBT.config(text = " Show solution ")

            self.emptyBD.config(width = 157)
            self.emptyBT.config(text = " Save and check board ")
        else:
            if not self.attemptToFindSolution():
                messagebox.showinfo("Information", "There is no possible solution for this board.\nPlease try again.")
                return

            self.solved = copy.deepcopy(self.board)

            self.emptyBD.config(width = 160)
            self.emptyBT.config(text = " Generate empty board ")


    # Fetches a new random table of given difficulty and replaces board
    def fetchRandomTable(self, level):
        tempBoard = []
        self.board.clear()
        self.completed.clear()
        self.conflicted.clear()
        self.solved.clear()
        link = "http://sudoku9x9.com/?level=" + str(self.levels.index(level))
        page = requests.get(link)
        tree = html.fromstring(page.content)
        i = 0

        # taking in list values and adding them as elements in midlist
        for x in range(9): # row
            for y in range(9): # col
                list = tree.xpath("//*[@id='cell{}']//text()".format(i))
                if list:
                    tempBoard.extend(list)
                else:
                    tempBoard.append(0)
                i += 1

        # adding midlist elems as rows of 9 into megalist
        # innerloopcount will continue to increment throughout the 81 elements in the midlist
        innerloopcount = 0
        for i in range(9):
            self.board.append([])
            self.completed.append([])
            self.conflicted.append([])
            for j in range(9):
                self.board[i].append(int(tempBoard[innerloopcount]))
                self.completed[i].append(0)
                self.conflicted[i].append(0)
                innerloopcount += 1

        self.altered, self.original = (copy.deepcopy(self.board) for i in range(2))

        if (self.solutionBT.cget('text') == " Hide solution "):
            self.solutionBD.config(width = 105)
            self.solutionBT.config(text = " Show solution ")


    # Event handler for key press (1 - 9)
    def keyPress(self, event):
        if self.selected: # because python doesn't have switch
            x = self.selected[0]
            y = self.selected[1]

            if self.original[x][y] != 0:
                playsound(self.selectSound(0, "cel"), block = False)
                return

            note = int(event.char)

            if note == self.altered[x][y] and self.conflicted[x][y] == 0:
                playsound(self.selectSound(note, "cel"), block = False)
                return

            self.altered[x][y] = note

            if self.checkForConflicts(x, y):
                playsound(self.selectSound(note, "con"), block = False)
            else:
                playsound(self.selectSound(note, "cel"), block = False)
                self.checkForCompletions(x, y, False)
                self.updateImage(x, y)


    # Event handler for mouseDown; opens github page or replaces selected tuple value
    def mouseDown(self, event):
        x = app.winfo_pointerx() - app.winfo_rootx()
        y = app.winfo_pointery() - app.winfo_rooty()
        if (gridXOffset < x and x < gridXOffset + 40 * 9 and gridYOffset < y and y < gridYOffset + 40 * 9):
            xth = math.ceil((x - gridXOffset) / 40) - 1
            yth = math.ceil((y - gridYOffset) / 40) - 1
            for i in range(4):
                self.cursor[i].place_forget()
            self.cursor[0].place(x = gridXOffset - 1 + xth * 40, y = gridYOffset - 1 + yth * 40)
            self.cursor[1].place(x = gridXOffset - 1 + xth * 40, y = gridYOffset - 1 + yth * 40)
            self.cursor[2].place(x = gridXOffset - 1 + xth * 40, y = gridYOffset + 37 + yth * 40)
            self.cursor[3].place(x = gridXOffset + 37 + xth * 40, y = gridYOffset - 1 + yth * 40)
            self.selected = (xth, yth)
        elif (153 < x and x < 198 and 27 < y and y < 43):
            webbrowser.open("https://github.com/jaxxk/Sudoku-solver")
        else:
            input = self.textBox.get("1.0",END)
            paddingSetting = input
        


    # Grabs new board and updates 9x9 grid
    def reGen(self, level):
        self.dropDown.set(" Random Generation")

        prompt = messagebox.askyesno("Confirmation", "Would you like to generate a new board?\nCurrernt board will be discarded.")
        if not prompt:
            return

        self.fetchRandomTable(level)
        for x in range(9):
                for y in range(9):
                    newImage = self.selectImage(x, y, self.board[x][y])
                    photo = ImageTk.PhotoImage(newImage)
                    self.cells[x][y].config(image = photo)
                    self.cells[x][y].image = photo


    # Grabs new board and updates 9x9 grid
    def resetBoard(self):
        prompt = messagebox.askyesno("Confirmation", "Would you like to reset the board?\nAny changes to the board will be discarded.")
        if not prompt:
            return

        self.board = copy.deepcopy(self.original)
        for x in range(9):
                for y in range(9):
                    newImage = self.selectImage(x, y, self.board[x][y])
                    photo = ImageTk.PhotoImage(newImage)
                    self.cells[x][y].config(image = photo)
                    self.cells[x][y].image = photo

        if (self.solutionBT.cget('text') == " Hide solution "):
            self.solutionBD.config(width = 105)
            self.solutionBT.config(text = " Show solution ")
    

    # Returns the path of image to use for x and y values
    def selectImage(self, x, y, value):
        imagePath = "assets/images/"
        colorVariant = ""
        saturateMultiplier = 1
        
        if 2 < y and y < 6:
            colorVariant = "e"
            if 2 < x and x < 6:
                colorVariant = "o"
        else:
            colorVariant = "o"
            if 2 < x and x < 6:
                colorVariant = "e"

        if self.conflicted[x][y] != 0:
            colorVariant += "c"

        if self.original[x][y] != 0:
            colorVariant += "f"

        if self.completed[x][y] == 0:
            saturateMultiplier = .2

        img = PIL.Image.open(imagePath + str(colorVariant) + str(value) + ".jpg")
        return PIL.ImageEnhance.Color(img).enhance(saturateMultiplier)


    def selectSound(self, inp, inst):
        path = "assets/audio/"
        path += str(inst) + str(inp)
        return path + ".wav"

    # Because I'm too lazy to replace selectImage with one that has a new parameter
    def selectImageButForEmptyBoardSoItRendersImagesCorrectly(self, x, y, value):
        # TODO: replace this function and replace empty button with one that toggles into 'save changes'
        imagePath = "assets/images/"
        colorVariant = ""
        
        if 2 < y and y < 6:
            colorVariant = "e"
            if 2 < x and x < 6:
                colorVariant = "o"
        else:
            colorVariant = "o"
            if 2 < x and x < 6:
                colorVariant = "e"

        return PIL.Image.open(imagePath + str(colorVariant) + str(value) + ".jpg")


    # Updates the current board with solution or hides it
    def showSolution(self):
        if not self.solved:
            counter = 0
            replace_empty(self.board)
            self.solved = copy.deepcopy(self.board)

        if (self.solutionBT.cget('text') == " Show solution "):
            prompt = messagebox.askyesno("Confirmation", "Would you like to reveal the solution?")
            if not prompt:
                return
            self.board = copy.deepcopy(self.solved)
            self.solutionBD.config(width = 98)
            self.solutionBT.config(text = " Hide solution ")
        else:
            self.board = copy.deepcopy(self.altered)
            self.solutionBD.config(width = 105)
            self.solutionBT.config(text = " Show solution ")

        for x in range(9):
            for y in range(9):
                newImage = self.selectImage(x, y, self.board[x][y])
                photo = ImageTk.PhotoImage(newImage)
                self.cells[x][y].config(image = photo)
                self.cells[x][y].image = photo


    def updateImage(self, x, y):
        newImage = self.selectImage(x, y, self.altered[x][y])
        photo = ImageTk.PhotoImage(newImage)
        self.cells[x][y].config(image = photo)
        self.cells[x][y].image = photo


    def psmChanger(self,psms):
        psmSetting = psms

    # main
    def __init__(self, root):
        # Grab a font from path to use (needs replacement)
        pathbuf = create_unicode_buffer(
            "assets\\fonts\\SF-Pro-Display-Regular.otf")
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
        AddFontResourceEx(byref(pathbuf), 0x10, 0)

        # Title and Github Button
        titleLabel = Label(app, text = "SudokuSolver", font = ("SF Pro Display", 17))
        titleLabel.place(x = 15, y = 15)

        githubLabel = Label(app, text = "Github↗", foreground = "blue", font = ("SF Pro Display", 10))
        githubLabel.place(x = 153, y = 25)
        
        # Generate new board
        generateLabel = Label(app, text = "Generate new board", font = ("SF Pro Display", 11))
        generateLabel.place(x = 381, y = buttonYOffset - 27)
       
        line1 = Frame(app, bd = 0, highlightbackground = "#666666", highlightthickness = 1, width = 172, height = 2)
        line1.place(x = 381, y = buttonYOffset - 7)

        self.dropDown.set(" Random Generation")
        generateBD = Frame(app, bd = 0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 172, height = buttonHeight)
        generateBD.place(x = 381, y = buttonYOffset)
        generateBT = OptionMenu(generateBD, self.dropDown, *self.levels, command = self.reGen)
        generateBT.config(bg = "white", font = ("SF Pro Display", 11), relief = "solid", borderwidth = 0, highlightbackground = "white", highlightthickness = 1, activebackground = "white")
        generateBT.place(x = 0, y = 0)
        
        self.emptyBD = Frame(app, bd = 0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 160, height = buttonHeight)
        self.emptyBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding))
        self.emptyBT = Button(self.emptyBD, text = buttonTempFix + "Generate empty board" + buttonTempFix, font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0, command = self.emptyBoard)
        self.emptyBT.place(x = 0, y = 0)
        
        captureBD = Frame(app, bd=0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 106, height = buttonHeight)
        captureBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 2)
        captureBT = Button(captureBD, text = buttonTempFix + "From Screen.." + buttonTempFix, font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0, command = self.captureBoard)
        captureBT.place(x = 0, y = 0)

        # Manage current board
        manageLabel = Label(app, text = "Manage current board", font = ("SF Pro Display", 11))
        manageLabel.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 3 + buttonGap)
       
        line2 = Frame(app, bd = 0, highlightbackground = "#666666", highlightthickness = 1, width = 172, height = 2)
        line2.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 3 + buttonGap + 20)

        self.solutionBD = Frame(app, bd = 0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 105, height = buttonHeight)
        self.solutionBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 3 + buttonGap + 27)
        self.solutionBT = Button(self.solutionBD, text = buttonTempFix + "Show solution" + buttonTempFix, font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0, command = self.showSolution)
        self.solutionBT.place(x = 0, y = 0)
        
        resetBD = Frame(app, bd = 0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 53, height = buttonHeight)
        resetBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 4 + buttonGap + 27)
        resetBT = Button(resetBD, text = buttonTempFix + "Reset" + buttonTempFix, font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0, command = self.resetBoard)
        resetBT.place(x = 0, y = 0)

        # Miscellaneous
        miscLabel = Label(app, text = "Miscellaneous", font = ("SF Pro Display", 11))
        miscLabel.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 5 + buttonGap * 2 + 27)
       
        line3 = Frame(app, bd = 0, highlightbackground = "#666666", highlightthickness = 1, width = 172, height = 2)
        line3.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 5 + buttonGap * 2 + 47)

        psmLabel = Label(app, text = "psm", font = ("SF Pro Display", 11))
        psmLabel.config(relief = "solid", borderwidth = 0, highlightbackground = "white", highlightthickness = 1, activebackground = "white")
        psmLabel.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 5 + buttonGap * 2 + 54)
        self.dropDown2.set(0)
        psmBD = Frame(app, bd = 0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 50, height = buttonHeight)
        psmBD.place(x = 415, y = buttonYOffset + (buttonHeight + buttonPadding) * 5 + buttonGap * 2 + 54)
        psmBT = OptionMenu(psmBD, self.dropDown2, *self.psms, command = self.psmChanger)
        psmBT.config(bg = "white", font = ("SF Pro Display", 11), relief = "solid", borderwidth = 0, highlightbackground = "white", highlightthickness = 1, activebackground = "white")
        psmBT.place(x = 0, y = 0)

        paddingLabel = Label(app, text = "padding", font = ("SF Pro Display", 11))
        paddingLabel.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 6 + buttonGap * 2 + 54)
        paddingBD = Frame(app, bd = 0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 50, height = buttonHeight)
        paddingBD.place(x = 440, y = buttonYOffset + (buttonHeight + buttonPadding) * 6 + buttonGap * 2 + 54)
        self.textBox = Text(paddingBD, height = 2, width = 50, relief = "solid", borderwidth = 0, highlightbackground = "white", highlightthickness = 1)
        self.textBox.place(x = 0, y = 0)

        # Grab a new table to work with
        self.fetchRandomTable(self.levels[2])

        # Fill completed table with 0s (to mark cells as incomplete)
        for i in range(9):
                self.completed.append([])
                self.conflicted.append([])
                for j in range(9):
                    self.completed[i].append(0)
                    self.conflicted[i].append(0)

        # Draw 9x9 grid
        for x in range(9):
            self.cells.append([])
            for y in range(9):
                image = self.selectImage(x, y, self.board[x][y])
                photo = ImageTk.PhotoImage(image)
                label = Label(image = photo)
                label.image = photo
                label.place(x = x * 40 + gridXOffset, y = y * 40 + gridYOffset)
                self.cells[x].append(label)

        # Draw cursor
        c1 = Frame(app, bd = 0, highlightbackground = "#212D40", highlightthickness = 3, width = 41, height = 3)
        self.cursor.append(c1)
        c2 = Frame(app, bd = 0, highlightbackground = "#212D40", highlightthickness = 3, width = 3, height = 41)
        self.cursor.append(c2)
        c3 = Frame(app, bd = 0, highlightbackground = "#212D40", highlightthickness = 3, width = 41, height = 3)
        self.cursor.append(c3)
        c4 = Frame(app, bd = 0, highlightbackground = "#212D40", highlightthickness = 3, width = 3, height = 41)
        self.cursor.append(c4)

        # Bind event handlers
        app.bind("<Button-1>", self.mouseDown)
        for i in range(0, 10):
            app.bind(i, self.keyPress)

def main():
    app.title("SudokuSolver")
    app.geometry("600x450")
    app["bg"] = "#F2F2F2"

    line = Canvas(app, width = 600, height = 10, highlightthickness = 0)
    line.pack()
    line.create_rectangle(0, 0, 600, 3, fill = "#696A8E")

    gui = mainScreen(app)
    app.mainloop()

if __name__=="__main__": 
    main()