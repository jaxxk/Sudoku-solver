from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
from lxml import html
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

import requests
import webbrowser

# Configurations
gridXOffset = 15
gridYOffset = 50
midlist, megalist, cells = ([] for i in range(3))


def fetchRandomTable(midlist, megalist):
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


def openGithub():
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


def motion(event):
    x,y = event.x,event.y
    if (x >= 0 and x <= 46):
         if (y >6 and y <= 8):
            openGithub()
class mainScreen:
    def __init__(self, master):

        fetchRandomTable(midlist, megalist)

        pathbuf = create_unicode_buffer(
            "assets\\fonts\\SF-Pro-Display-Light.otf")
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
        AddFontResourceEx(byref(pathbuf), 0x10, 0)

        titleLabel = Label(app, text = "SudokuSolver", font = ("SF Pro Display", 17))
        titleLabel.place(x = 15, y = 15)


        buttonStyle = Style()
        buttonStyle.configure("github.TButton", font = ("SF Pro Display", 10), foreground = "#3399FF", background = "#F2F2F2")
        githubLabel = Label(app, text = "Github↗",foreground = "blue")
        githubLabel.place(x = 150, y = 25)
        

        generateLabel = Label(app, text = "Generate New Board",font = ("SF Pro Display", 13))
        generateLabel.place(x = 400, y = 25)


        for x in range(9):
            cells.append([])
            for y in range(9):
                image = selectImage(x, y, megalist[x][y])
                photo = ImageTk.PhotoImage(image)
                label = Label(image = photo)
                label.image = photo
                label.place(x = x * 40 + gridXOffset, y = y * 40 + gridYOffset)
                cells[x].append(label)


app = Tk()
app.title("SudokuSolver")
app.geometry("600x450")
app["bg"] = "#F2F2F2"
app.bind("<Button-1>",motion)


line = Canvas(app, width = 600, height = 10, highlightthickness = 0)
line.pack()
line.create_rectangle(0, 0, 600, 4, fill = "#696A8E")

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
