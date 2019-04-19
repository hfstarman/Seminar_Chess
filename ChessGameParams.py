#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessGameParams.py
 Description:  Creates a Tkinter dialog window to get game
	parameters.
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """

from tkinter import *
#from Tkinter import Tk,Frame,Label,Entry,Radiobutton,Button,StringVar,ANCHOR

class TkinterGameSetupParams:

	def __init__(self, playerAmount):
		self.playerAmount = int(playerAmount)
		self.root = Tk()
		self.root.title("Welcome to Python Chess!")
		self.frame = Frame(self.root)
		self.frame.pack()
		
		self.instructionMessage = StringVar()
		Label(self.frame, textvariable=self.instructionMessage).grid(row=0)
		self.instructionMessage.set("Please Enter Player Names.")

		#Column 2 label
		Label(self.frame, text="Name").grid(row=1,column=1)


		self.entry_playerNames = [None]*self.playerAmount
		for i in range(self.playerAmount):
			default_name = "Player " + str(i+1)
			Label(self.frame, text=default_name).grid(row=(i+5),column=0)
			self.entry_playerNames[i] = Entry(self.frame)
			self.entry_playerNames[i].grid(row=(i+5),column=1)
			self.entry_playerNames[i].insert(ANCHOR,default_name)
		

		b = Button(self.frame, text="Start the Game!", command=self.ok)
		b.grid(row=i+6,column=1)

	def ok(self):
		self.player1Name = "" #self.entry_player1Name.get()
		#hardcoded so that player 1 is always white
		self.player1Color = "white"
		self.player1Type = "human" #self.tk_player1Type.get()
		self.player2Name = "" #self.entry_player2Name.get()
		self.player2Color = "black"
		self.player2Type = "randomAI" #self.tk_player2Type.get()

		self.playerNames = []
		for name_object in self.entry_playerNames:
			self.playerNames.append(name_object.get())

		self.frame.destroy()

	def GetGameSetupParams(self):
		self.root.wait_window(self.frame) #waits for frame to be destroyed
		self.root.destroy() #noticed that with "text" gui mode, the tk window stayed...this gets rid of it.
		return (self.player1Name, self.player1Color, self.player1Type, 
				self.player2Name, self.player2Color, self.player2Type, self.playerAmount, self.playerNames)



if __name__ == "__main__":		

	d = TkinterGameSetupParams()
	x = d.GetGameSetupParams()
	print(x)
