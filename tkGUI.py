from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
from lxml import html
from tkinter import *
from PIL import Image, ImageTk
from test import *

import copy
import requests
import webbrowser

# Configurations
gridXOffset = 15
gridYOffset = 50
buttonGap = 12
buttonHeight = 30
buttonPadding = 4
buttonYOffset = 51
solutionHidden = False;

midlist, megalist, cells, original, solved = ([] for i in range(5))

app = Tk()


def mouseDown(event):
    x = app.winfo_pointerx() - app.winfo_rootx()
    y = app.winfo_pointery() - app.winfo_rooty()
    if (gridXOffset < x and x < gridXOffset + 40 * 9 and gridYOffset < y and y < gridYOffset + 40 * 9):
        print("x: " + str((x - gridXOffset) / 40) + ", y: " + str((y - gridYOffset) / 40))
    elif (153 < x and x < 198 and 27 < y and y < 43):
        webbrowser.open("https://github.com/jaxxk/Sudoku-solver")


def selectImage(x, y, value):
    imagePath = "assets/images/"
    colorVariant = ""
    if 2 < y and y < 6:
        colorVariant = "o"
        if 2 < x and x < 6:
            colorVariant = "e"
    else:
        colorVariant = "e"
        if 2 < x and x < 6:
            colorVariant = "o"

    return Image.open(imagePath + str(colorVariant) + str(value) + ".jpg")


def fetchRandomTable(midlist, megalist):
    midlist.clear()
    megalist.clear()

    page = requests.get("http://sudoku9x9.com")
    tree = html.fromstring(page.content)
    i = 0

    # taking in list values and adding them as elements in midlist
    for x in range(9):  # row
        for y in range(9):  # col
            list = tree.xpath("//*[@id='cell{}']//text()".format(i))
            if list:
                midlist.extend(list)
            else:
                midlist.append(0)
            i += 1

    # adding midlist elems as rows of 9 into megalist
    # innerloopcount will continue to increment throughout the 81 elements in the midlist
    innerloopcount = 0
    for i in range(9):
        megalist.append([])
        for j in range(9):
            megalist[i].append(int(midlist[innerloopcount]))
            innerloopcount += 1
            j += 1
        i += 1

def reGen():
    fetchRandomTable(midlist, megalist)
    for x in range(9):
            for y in range(9):
                newImage = selectImage(x, y, megalist[x][y])
                photo = ImageTk.PhotoImage(newImage)
                cells[x][y].config(image = photo)
                cells[x][y].image = photo

def showSolution(bt):
    global original, solved, megalist
    if not solved:
        print(original) # should be empty
        original = copy.deepcopy(megalist)
        print(original) # should store original
        replace_empty(megalist)
        print(original) # why is this same as megalist?
        solved = copy.deepcopy(megalist)

    if (bt.cget('text') == " Show solution "):
        megalist = copy.deepcopy(solved)
        bt.config(text = " Hide solution ")
    else:
        megalist = copy.deepcopy(original)
        bt.config(text = " Show solution ")

    for x in range(9):
        for y in range(9):
            newImage = selectImage(x, y, megalist[x][y])
            photo = ImageTk.PhotoImage(newImage)
            cells[x][y].config(image = photo)
            cells[x][y].image = photo
    

class mainScreen:
    def __init__(self, master):
        fetchRandomTable(midlist, megalist)

        pathbuf = create_unicode_buffer(
            "assets\\fonts\\SF-Pro-Display-Light.otf")
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
       
        line1 = Frame(app, bd=0, highlightbackground = "#666666", highlightthickness = 1, width = 150, height = 2)
        line1.place(x = 381, y = buttonYOffset - 7)

        generateBD = Frame(app, bd=0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 144, height = buttonHeight)
        generateBD.place(x = 381, y = buttonYOffset)
        generateBT = Button(generateBD, text = " Random Generation ", font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0, command = reGen)
        generateBT.place(x = 0, y = 0)
        
        manualBD = Frame(app, bd=0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 98, height = buttonHeight)
        manualBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding))
        manualBT = Button(manualBD, text = " Manual Input ", font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0)
        manualBT.place(x = 0, y = 0)
        
        captureBD = Frame(app, bd=0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 106, height = buttonHeight)
        captureBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 2)
        captureBT = Button(captureBD, text = " From Screen.. ", font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0)
        captureBT.place(x = 0, y = 0)

        # Manage current board
        manageLabel = Label(app, text = "Manage current board", font = ("SF Pro Display", 11))
        manageLabel.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 3 + buttonGap)
       
        line2 = Frame(app, bd=0, highlightbackground = "#666666", highlightthickness = 1, width = 150, height = 2)
        line2.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 3 + buttonGap + 20)

        solutionBD = Frame(app, bd=0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 137, height = buttonHeight)
        solutionBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 3 + buttonGap + 27)
        solutionBT = Button(solutionBD, text = " Show solution ", font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0)
        solutionBT.config(command = lambda: showSolution(solutionBT))
        solutionBT.place(x = 0, y = 0)
        
        resetBD = Frame(app, bd=0, highlightbackground = "#CCCCCC", highlightthickness = 1, width = 53, height = buttonHeight)
        resetBD.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 4 + buttonGap + 27)
        resetBT = Button(resetBD, text = " Reset ", font = ("SF Pro Display", 11), bg = "white", relief = "solid", borderwidth = 0)
        resetBT.place(x = 0, y = 0)

        # Miscellaneous
        miscLabel = Label(app, text = "Miscellaneous", font = ("SF Pro Display", 11))
        miscLabel.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 5 + buttonGap * 2 + 27)
       
        line3 = Frame(app, bd=0, highlightbackground = "#666666", highlightthickness = 1, width = 150, height = 2)
        line3.place(x = 381, y = buttonYOffset + (buttonHeight + buttonPadding) * 5 + buttonGap * 2 + 47)

        for x in range(9):
            cells.append([])
            for y in range(9):
                image = selectImage(x, y, megalist[x][y])
                photo = ImageTk.PhotoImage(image)
                label = Label(image = photo)
                label.image = photo
                label.place(x = x * 40 + gridXOffset, y = y * 40 + gridYOffset)
                cells[x].append(label)


app.title("SudokuSolver")
app.geometry("600x450")
app["bg"] = "#F2F2F2"
app.bind("<Button-1>",mouseDown)

line = Canvas(app, width = 600, height = 10, highlightthickness = 0)
line.pack()
line.create_rectangle(0, 0, 600, 3, fill = "#696A8E")

gui = mainScreen(app)
app.mainloop()

# class SampleApp(tk.Tk):

#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)

#         self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold", slant="italic")

#         # the container is where we"ll stack a bunch of frames
#         # on top of each other, then the one we want visible
#         # will be raised above the others
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

#         self.frames = {}
#         for F in (StartPage, PageOne):
#             page_name = F.__name__
#             frame = F(parent=container, controller=self)
#             self.frames[page_name] = frame

#             # put all of the pages in the same location;
#             # the one on the top of the stacking order
#             # will be the one that is visible.
#             frame.grid(row=0, column=0, sticky="nsew")

#         self.show_frame("StartPage")

#     def show_frame(self, page_name):
#         "Show a frame for the given page name"
#         frame = self.frames[page_name]
#         frame.tkraise()


# class StartPage(tk.Frame):

#     def __init__(self, parent, controller):
#       tk.Frame.__init__(self, parent)
#       self.controller = controller
#       label = tk.Label(self, text="This is the start page", font=controller.title_font)
#       label.pack(side="top", fill="x", pady=10)
#       button1 = tk.Button(self, text="Go to Page One",
#                             command= self.nextPage())
#       image = Image.open("test.png")
#       photo = ImageTk.PhotoImage(image)
#       self.label = Label(image=photo)
#       self.label.image = photo
#       self.label.pack()
#       button1.pack()
#     def nextPage(self):
#       return self.controller.show_frame("PageOne")


# class PageOne(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         label = tk.Label(self, text="This is page 1", font=controller.title_font)
#         label.pack(side="top", fill="x", pady=10)
#         self.label.pack_forget()
#         button = tk.Button(self, text="Go to the start page",
#                            command=lambda: controller.show_frame("StartPage"))
#         button.pack()


# if __name__ == "__main__":
#     app = SampleApp()
#     app.mainloop()
