from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
from lxml import html
from tkinter import *
from tkinter import messagebox
from playsound import playsound

from sudokuAlgorithm import *
from sudokuBoard import *

import copy
import math
import requests
import webbrowser

# Configurations
gridXOffset = 15
gridYOffset = 50
buttonGap = 12
buttonHeight = 30
buttonPadding = 4
buttonYOffset = 51

app = Tk()

class mainScreen:
    board, cells, cursor, original, solved = ([] for i in range(5))
    levels = ["Beginner", "Intermediate                    ", "Advanced", "Expert", "Master"]
    selected = () # x, y

    dropDown = StringVar(app)
    solutionBD, solutionBT = (None for i in range(2))

    # Fetches a new random table of given difficulty and replaces board
    def emptyBoard(self):
        prompt = messagebox.askyesno("Confirmation", "Would you like to empty the board?")
        if not prompt:
            return

        self.board.clear()
        self.solved.clear()

        for i in range(9):
            self.board.append([])
            for j in range(9):
                self.board[i].append(0)

        for x in range(9):
                for y in range(9):
                    newImage = selectImage(x, y, self.board[x][y])
                    photo = ImageTk.PhotoImage(newImage)
                    self.cells[x][y].config(image = photo)
                    self.cells[x][y].image = photo

        self.original = copy.deepcopy(self.board)

        if (self.solutionBT.cget('text') == " Hide solution "):
            self.solutionBD.config(width = 105)
            self.solutionBT.config(text = " Show solution ")


    # Fetches a new random table of given difficulty and replaces board
    def fetchRandomTable(self, level):
        tempBoard = []
        self.board.clear()
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
            for j in range(9):
                self.board[i].append(int(tempBoard[innerloopcount]))
                innerloopcount += 1

        self.original = copy.deepcopy(self.board)

        if (self.solutionBT.cget('text') == " Hide solution "):
            self.solutionBD.config(width = 105)
            self.solutionBT.config(text = " Show solution ")


    # Grabs new board and updates 9x9 grid
    def reGen(self, level):
        self.dropDown.set(" Random Generation")
        self.fetchRandomTable(level)
        for x in range(9):
                for y in range(9):
                    newImage = selectImage(x, y, self.board[x][y])
                    photo = ImageTk.PhotoImage(newImage)
                    self.cells[x][y].config(image = photo)
                    self.cells[x][y].image = photo


    # Event handler for key press (1 - 9)
    def keyPress(self, event):
        if self.selected:
            note = event.char
            if note == "1":
                playsound("assets/audio/celC5.wav", block = False)
            elif note == "2":
                playsound("assets/audio/celD5.wav", block = False)
            elif note == "3":
                playsound("assets/audio/celE5.wav", block = False)
            elif note == "4":
                playsound("assets/audio/celF5.wav", block = False)
            elif note == "5":
                playsound("assets/audio/celFs5.wav", block = False)
            elif note == "6":
                playsound("assets/audio/celG5.wav", block = False)
            elif note == "7":
                playsound("assets/audio/celA5.wav", block = False)
            elif note == "8":
                playsound("assets/audio/celB5.wav", block = False)
            elif note == "9":
                playsound("assets/audio/celC6.wav", block = False)
            elif note == "0":
                playsound("assets/audio/celC4.wav", block = False)

            x = self.selected[0]
            y = self.selected[1]
            self.board[x][y] = int(note)
            newImage = selectImage(x, y, self.board[x][y])
            photo = ImageTk.PhotoImage(newImage)
            self.cells[x][y].config(image = photo)
            self.cells[x][y].image = photo


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


    # Updates the current board with solution or hides it
    def showSolution(self):
        if not self.solved:
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
            self.board = copy.deepcopy(self.original)
            self.solutionBD.config(width = 105)
            self.solutionBT.config(text = " Show solution ")

        for x in range(9):
            for y in range(9):
                newImage = selectImage(x, y, self.board[x][y])
                photo = ImageTk.PhotoImage(newImage)
                self.cells[x][y].config(image = photo)
                self.cells[x][y].image = photo


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
        
        emptyBD = Frame(app, bd = 0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 160, height = buttonHeight)
        emptyBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding))
        emptyBT = Button(emptyBD, text = " Generate empty board ", font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0, command = self.emptyBoard)
        emptyBT.place(x = 0, y = 0)
        
        captureBD = Frame(app, bd=0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 106, height = buttonHeight)
        captureBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 2)
        captureBT = Button(captureBD, text = " From Screen.. ", font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0)
        captureBT.place(x = 0, y = 0)

        # Manage current board
        manageLabel = Label(app, text = "Manage current board", font = ("SF Pro Display", 11))
        manageLabel.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 3 + buttonGap)
       
        line2 = Frame(app, bd = 0, highlightbackground = "#666666", highlightthickness = 1, width = 172, height = 2)
        line2.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 3 + buttonGap + 20)

        self.solutionBD = Frame(app, bd = 0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 105, height = buttonHeight)
        self.solutionBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 3 + buttonGap + 27)
        self.solutionBT = Button(self.solutionBD, text = " Show solution ", font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0, command = self.showSolution)
        self.solutionBT.place(x = 0, y = 0)
        
        resetBD = Frame(app, bd = 0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 53, height = buttonHeight)
        resetBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 4 + buttonGap + 27)
        resetBT = Button(resetBD, text = " Reset ", font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0)
        resetBT.place(x = 0, y = 0)

        # Miscellaneous
        miscLabel = Label(app, text = "Miscellaneous", font = ("SF Pro Display", 11))
        miscLabel.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 5 + buttonGap * 2 + 27)
       
        line3 = Frame(app, bd = 0, highlightbackground = "#666666", highlightthickness = 1, width = 172, height = 2)
        line3.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 5 + buttonGap * 2 + 47)

        # Grab a new table to work with
        self.fetchRandomTable(self.levels[2])

        # Draw 9x9 grid
        for x in range(9):
            self.cells.append([])
            for y in range(9):
                image = selectImage(x, y, self.board[x][y])
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