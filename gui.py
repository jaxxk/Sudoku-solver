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
		self.rbutton = tk.Button(self, text="Random Sudoku Solver",command = lambda:controller.show_frame(RandomPage))
		self.rbutton.pack()

		self.mbutton = tk.Button(self, text="Manual Input",command = lambda:controller.show_frame(ManulPage))
		self.mbutton.pack()

class RandomPage(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		self.label = tk.Label(self,text="Random Sudoku",font=LARGEFONT)
		self.label.pack()

		self.showButton = tk.Button(self, text="Show Solution",command = self.showRes)
		self.showButton.pack()

		self.eraseButton = tk.Button(self, text="Erase",command =  self.delete)
		self.eraseButton.pack()
		self.returnButton = tk.Button(self, text="Main Meanu",command = lambda:controller.show_frame(StartPage))
		self.returnButton.pack()
		
		self. dele = 0
		p = sub.Popen('test',stdout=sub.PIPE,stderr=sub.PIPE)
		self.output, errors = p.communicate()


	def showRes(self):
		self.text = Text(self)
		self.text.pack()
		self.text.insert(END,self.output)
	def delete(self):
	 	self.dele = 1
	 	self.text.pack_forget()
	 	self.eraseButton.pack_forget()
	
class ManulPage(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		self.label = tk.Label(self,text="Manual Sudoku",font=LARGEFONT)
		self.label.pack()
		# self.grid()
  #       self.create_widgets()

	# def create_widgets(self):
 #        self.entries = {}
 #        self.tableheight = 9
 #        self.tablewidth = 9
 #        counter = 0
 #        for row in xrange(self.tableheight):
 #            for column in xrange(self.tablewidth):
 #                self.entries[counter] = Entry(self, width=5)
 #                self.entries[counter].grid(row=row, column=column)
 #                counter += 1


app = MainScreen()
app.mainloop()

