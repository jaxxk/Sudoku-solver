from tkinter import *
import tkinter as tk
from tkinter import ttk
# from tkinter import *
import subprocess as sub
from test import *


LARGEFONT = ("Verdana",12)
class MainScreen(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		container = tk.Frame(self)
		container.pack(side="top",fill="both",expand=True)

		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)

		self.frames = {}

		for F in (StartPage,RandomPage,ManulPage):
			frame = F(container,self)
			self.frames[F] = frame
			frame.grid(row=0,column=0,sticky="N")

		self.show_frame(StartPage)

	def show_frame(self,cont):
		frame = self.frames[cont]
		frame.tkraise()



class StartPage(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		# label = tk.Label(self,text="jack",font=LARGEFONT)
		# label.pack()

		rbutton = tk.Button(self, text="Random Sudoku Solver",command = lambda:controller.show_frame(RandomPage))
		rbutton.pack()

		mbutton = tk.Button(self, text="Manual Input",command = lambda:controller.show_frame(ManulPage))
		mbutton.pack()

class RandomPage(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text="Random Sudoku",font=LARGEFONT)
		label.pack()

		showButton = tk.Button(self, text="Show Solution",command = self.showRes)
		showButton.pack()
		
		eraseButton = tk.Button(self, text="Erase",command =  self.delete)
		eraseButton.pack()

		returnButton = tk.Button(self, text="Main Meanu",command =  lambda:controller.show_frame(StartPage))
		returnButton.pack()

		p = sub.Popen('test',stdout=sub.PIPE,stderr=sub.PIPE)
		self.output, errors = p.communicate()
		self.text = Text(self)
	def delete(self):
		self.text.delete('1.0', END)

	def showRes(self):
		self.text.pack()
		self.text.insert(END, self.output)
	


class ManulPage(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text="Manual Sudoku",font=LARGEFONT)
		label.pack()

		returnButton = tk.Button(self, text="Back to home",command = lambda:controller.show_frame(StartPage))
		returnButton.pack()

app = MainScreen()
app.mainloop()

