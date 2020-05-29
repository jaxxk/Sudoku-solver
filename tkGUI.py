from tkinter import *
import tkinter as tk
# from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk
from tkinter import font  as tkfont # python 3

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")
        for x in range(3):
	        image = Image.open("sudoku.png")
	        photo = ImageTk.PhotoImage(image)
	        label = Label(image=photo)
	        label.image = photo
	        label.grid(row=0,column=x)

        # image = Image.open("sudoku.png")
        # photo2 = ImageTk.PhotoImage(image)
        # label2 = Label(image=photo)
        # label2.image = photo
        # label2.grid(row=0,column=2)

        # self.close_button = Button(master, text="Close", command=master.quit)
        # self.close_button.grid()

    def greet(self):
        print("Greetings!")

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()

# class SampleApp(tk.Tk):

#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)

#         self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

#         # the container is where we'll stack a bunch of frames
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
#         '''Show a frame for the given page name'''
#         frame = self.frames[page_name]
#         frame.tkraise()


# class StartPage(tk.Frame):

#     def __init__(self, parent, controller):
#     	tk.Frame.__init__(self, parent)
#     	self.controller = controller
#     	label = tk.Label(self, text="This is the start page", font=controller.title_font)
#     	label.pack(side="top", fill="x", pady=10)
#     	button1 = tk.Button(self, text="Go to Page One",
#                             command= self.nextPage())
#     	image = Image.open("test.png")
#     	photo = ImageTk.PhotoImage(image)
#     	self.label = Label(image=photo)
#     	self.label.image = photo
#     	self.label.pack()
#     	button1.pack()
#     def nextPage(self):
#     	return self.controller.show_frame("PageOne")


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