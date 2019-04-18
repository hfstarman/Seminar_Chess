from tkinter import *
from ChessGameParams import TkinterGameSetupParams
#from Tkinter import Tk,Frame,Label,Entry,Radiobutton,Button,StringVar,ANCHOR

class Tkinter_playerAmount:

	def __init__(self):
		self.root = Tk()
		self.root.title("Seminar Chess")
		self.frame = Frame(self.root)
		self.frame.pack()
		self.playerAmount = 0
		
		self.instructionMessage = StringVar()
		Label(self.frame, textvariable=self.instructionMessage).grid(row=0)
		self.instructionMessage.set("Welcome to Seminar Chess!")
		
		Label(self.frame, text="Number Of Players (0-32)").grid(row=1,column=0)
		self.entry_playerAmount = Entry(self.frame)
		self.entry_playerAmount.grid(row=1,column=1)
		self.entry_playerAmount.insert(ANCHOR,"4")
		

		b = Button(self.frame, text="Continue", command=self.ok)
		b.grid(row=2,column=1)

	def ok(self):
		self.playerAmount = self.entry_playerAmount.get()

		#if self.playerAmount != "":
		if 0 <= int(self.playerAmount) <= 32:
			self.frame.destroy()

	def parameterPopup(self):
		self.root.wait_window(self.frame) #waits for frame to be destroyed
		self.root.destroy()

		return TkinterGameSetupParams(self.playerAmount)

if __name__ == "__main__":		

	d = Tkinter_playerAmount()
	x = d.parameterPopup()
	print(x)