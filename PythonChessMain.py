#! /usr/bin/env python
"""
 Project: Python Chess
 File name: PythonChessMain.py
 Description:  Chess for player vs. player, player vs. AI, or AI vs. AI.
    Uses Tkinter to get initial game parameters.  Uses Pygame to draw the
    board and pieces and to get user mouse clicks.  Run with the "-h" option
    to get full listing of available command line flags.

 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 *******
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful, but
 WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
 for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 *******
 Version history:

 v 0.7 - 27 April 2009.  Dramatically lowered CPU usage by using
   "pygame.event.wait()" rather than "pygame.event.get()" in
   ChessGUI_pygame.GetPlayerInput().

 v 0.6 - 20 April 2009.  Some compatibility fixes: 1) Class: instead of
   Class(), 2) renamed *.PNG to *.png, 3) rendered text with antialias flag on.
   Also changed exit() to sys.exit(0). (Thanks to tgfcoder from pygame website
   for spotting these errors.)

 v 0.5 - 16 April 2009.  Added new AI functionality - created
   "ChessAI_defense" and "ChessAI_offense."  Created PythonChessAIStats
   class for collecting AI vs. AI stats.  Incorporated Python module
   OptionParser for better command line parsing.

 v 0.4 - 14 April 2009.  Added better chess piece graphics from Wikimedia
   Commons.  Added a Tkinter dialog box (ChessGameParams.py) for getting
   the game setup parameters.  Converted to standard chess notation for
   move reporting and added row/col labels around the board.

 v 0.3 - 06 April 2009.  Added pygame graphical interface.  Includes
   addition of ScrollingTextBox class.

 v 0.2 - 04 April 2009.  Broke up the program into classes that will
   hopefully facilitate easily incorporating graphics or AI play.

 v 0.1 - 01 April 2009.  Initial release.  Draws the board, accepts
   move commands from each player, checks for legal piece movement.
   Appropriately declares player in check or checkmate.

 Possible improvements:
   - Chess Rules additions, ie: Castling, En passant capture, Pawn Promotion
   - Better AI
   - Network play

"""

from ChessBoard import ChessBoard
from ChessAI import likeOMGimSoooooRandumbAI, ChessAI_random, ChessAI_defense, ChessAI_offense, hankAI
from ChessPlayer import ChessPlayer
from ChessGUI_text import ChessGUI_text
from ChessGUI_pygame import ChessGUI_pygame
from ChessRules import ChessRules
from ChessGameParams import TkinterGameSetupParams
from player_amount_popup import Tkinter_playerAmount

from optparse import OptionParser
import time, random

class PythonChessMain:
    def __init__(self,options):
        if options.debug:
            self.Board = ChessBoard(2)
            self.debugMode = True
        else:
            self.Board = ChessBoard(0)#0 for normal board setup; see ChessBoard class for other options (for testing purposes)
            self.debugMode = False

        self.Rules = ChessRules()

    def SetUp(self,options):
        #gameSetupParams: Player 1 and 2 Name, Color, Human/AI level
        if self.debugMode:
            player1Name = 'Kasparov'
            player1Type = 'human'
            player1Color = 'white'
            player2Name = 'Light Blue'
            player2Type = 'randomAI'
            player2Color = 'black'
        else:
            temp = Tkinter_playerAmount()
            GameParams = temp.parameterPopup()
            playerInfo = GameParams.GetGameSetupParams()

            player1Name = playerInfo[0]
            player1Color = playerInfo[1]
            player1Type = playerInfo[2]
            player2Name = playerInfo[3]
            player2Color = playerInfo[4]
            player2Type = playerInfo[5]

            self.playerAmount = playerInfo[6]
            self.playerNamesList = playerInfo[-1]

            #This area of the setup will create the controllerDict
            #When  piece's abbreviation is put into the controllerDict
            #then the name of the player which controls that piece is returned
            #if the controller is 'None' then thats when the AI takes over
            self.blackPieces = ['bR1','bT1','bB1','bQ','bK','bB2','bT2','bR2',
                                'bP1','bP2','bP3','bP4','bP5','bP6','bP7','bP8']
            self.whitePieces = ['wP1','wP2','wP3','wP4','wP5','wP6','wP7','wP8',
                                'wR1','wT1','wB1','wQ','wK','wB2','wT2','wR2']

            self.captureDict = {}
            for piece in (self.blackPieces+self.whitePieces):
                self.captureDict[piece] = 0


            random.shuffle(self.playerNamesList)
            random.shuffle(self.blackPieces)
            random.shuffle(self.whitePieces)

            #first half of player list will be the white people and the second half will control the blacks
            white_people = self.playerNamesList[:len(self.playerNamesList)//2]
            black_people = self.playerNamesList[len(self.playerNamesList)//2:]

            self.controllerDict = {}
            controller = ""
            i = 0
            for piece in self.whitePieces:
                try:
                    controller = white_people[i]
                except:
                    controller = None

                self.controllerDict[piece] = controller
                if 'P' in piece:
                    promoted_pawn = 'wQ' + piece[-1] #change this to be more general if we change abbr of pieces
                    self.controllerDict[promoted_pawn] = controller

                i += 1

            i = 0
            for piece in self.blackPieces:
                try:
                    controller = black_people[i]
                except:
                    controller = None

                self.controllerDict[piece] = controller
                if 'P' in piece:
                    promoted_pawn = 'bQ' + piece[-1] #change this to be more general if we change abbr of pieces
                    self.controllerDict[promoted_pawn] = controller

                i += 1

            #(player1Name, player1Color, player1Type, player2Name, player2Color, player2Type) = GameParams.GetGameSetupParams()

        self.player = [0,0]
        if player1Type == 'human':
            self.player[0] = ChessPlayer(player1Name,player1Color)
        elif player1Type == 'randomAI':
            self.player[0] = ChessAI_random(player1Name,player1Color)
        elif player1Type == 'defenseAI':
            self.player[0] = ChessAI_defense(player1Name,player1Color)
        elif player1Type == 'offenseAI':
            self.player[0] = ChessAI_offense(player1Name,player1Color)

        if player2Type == 'human':
            self.player[1] = ChessPlayer(player2Name,player2Color)
        elif player2Type == 'randomAI':
            self.player[1] = ChessAI_random(player2Name,player2Color)
        elif player2Type == 'defenseAI':
            self.player[1] = ChessAI_defense(player2Name,player2Color)
        elif player2Type == 'offenseAI':
            self.player[1] = ChessAI_offense(player2Name,player2Color)

        if 'AI' in self.player[0].GetType() and 'AI' in self.player[1].GetType():
            self.AIvsAI = True
        else:
            self.AIvsAI = False

        if options.pauseSeconds > 0:
            self.AIpause = True
            self.AIpauseSeconds = int(options.pauseSeconds)
        else:
            self.AIpause = False

        #create the gui object - didn't do earlier because pygame conflicts with any gui manager (Tkinter, WxPython...)
        if options.text:
            self.guitype = 'text'
            self.Gui = ChessGUI_text()
        else:
            self.guitype = 'pygame'
            if options.old:
                self.Gui = ChessGUI_pygame(0)
            else:
                self.Gui = ChessGUI_pygame(1)

    def sim_setup(self,options):
        #gameSetupParams: Player 1 and 2 Name, Color, Human/AI level
        player1Name = 'Kulikowski'
        player1Type = 'randomAI'
        player1Color = 'white'
        player2Name = 'William, The OP'
        player2Type = 'randomAI'
        player2Color = 'black'

        self.player = [0,0]
        if player1Type == 'human':
            self.player[0] = ChessPlayer(player1Name,player1Color)
        elif player1Type == 'randomAI':
            self.player[0] = ChessAI_random(player1Name,player1Color)

        if player2Type == 'human':
            self.player[1] = ChessPlayer(player2Name,player2Color)
        elif player2Type == 'randomAI':
            self.player[1] = ChessAI_random(player2Name,player2Color)

        if 'AI' in self.player[0].GetType() and 'AI' in self.player[1].GetType():
            self.AIvsAI = True
        else:
            self.AIvsAI = False

        if options.pauseSeconds > 0:
            self.AIpause = True
            self.AIpauseSeconds = int(options.pauseSeconds)
        else:
            self.AIpause = False

        self.guitype = 'text'
        self.Gui = ChessGUI_text()

    def getWhitePieces(self):
        white_list = []
        board = self.Board.GetState()

        for i in range(8):
            for j in range(8):
                if 'w' in board[i][j]:
                    white_list.append(board[i][j])

        return white_list


    def getBlackPieces(self):
        black_list = []
        board = self.Board.GetState()

        for i in range(8):
            for j in range(8):
                if 'b' in board[i][j]:
                    black_list.append(board[i][j])

        return black_list

    def MainLoop(self):
        currentPlayerIndex = 0
        turnCount = 0
        moveCount = 0

        isKingCaptured = False
        while not isKingCaptured:

            self.whitePieces = self.getWhitePieces()
            self.blackPieces = self.getBlackPieces()
            random.shuffle(self.whitePieces)
            random.shuffle(self.blackPieces)
            piecesAvailableToColor = [self.whitePieces, self.blackPieces]

            for currentPiece in piecesAvailableToColor[currentPlayerIndex]:
                board = self.Board.GetState()
                currentColor = self.player[currentPlayerIndex].GetColor()
                #hardcoded so that player 1 is always white
                if currentColor == 'white' and moveCount == 0:
                    turnCount = turnCount + 1
                self.Gui.PrintMessage("")
                baseMsg = "TURN %s - %s (%s)" % (str(turnCount),self.controllerDict[currentPiece],self.Board.GetFullString(currentPiece))
                self.Gui.PrintMessage("-----%s-----" % baseMsg)
                self.Gui.Draw(board)

                if self.Rules.IsInCheck(board,currentColor):
                    self.Gui.PrintMessage("Warning..."+self.player[currentPlayerIndex].GetName()+" ("+self.player[currentPlayerIndex].GetColor()+") is in check!")

                #When there is no controller then the AI takes over that piece
                moveTuple = None
                if self.controllerDict[currentPiece] == None:
                    hank = hankAI(currentPiece, board)
                    moveTuple = hank.minimax(currentPiece, board, currentColor)
                    time.sleep(.1)
                else:
                    moveTuple = self.Gui.GetPlayerInput(board,currentColor, currentPiece)
                    
                moveReport = self.Board.MovePiece(moveTuple, self.captureDict) #moveReport = string like "White Bishop moves from A1 to C3" (+) "and captures ___!"

                self.Gui.PrintMessage(moveReport)

                kings = 0
                for i in range(8):
                    for j in range(8):
                        if board[i][j] == 'bK' or board[i][j] == 'wK':
                            kings += 1
                if kings != 2:
                    isKingCaptured = True
                    break

                moveCount += 1


            currentPlayerIndex = (currentPlayerIndex+1)%2 #this will cause the currentPlayerIndex to toggle between 1 and 0
            moveCount = 0

            if self.AIvsAI and self.AIpause:
                time.sleep(self.AIpauseSeconds)

        
        self.Gui.PrintMessage("KING CAPTURED!")
        winnerIndex = (currentPlayerIndex+1)%2

        for piece in self.captureDict:
            self.captureDict[piece] += self.Board.getScore(piece, self.Board.GetState())

        print(self.captureDict)
        self.Gui.PrintMessage(self.player[winnerIndex].GetColor()+" won the game!")
        self.Gui.EndGame(board)
        self.winnerIndex = winnerIndex
        self.turnCount = turnCount

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", dest="debug",
                      action="store_true", default=False, help="Enable debug mode (different starting board configuration)")
    parser.add_option("-t", dest="text",
                      action="store_true", default=False, help="Use text-based GUI")
    parser.add_option("-o", dest="old",
                      action="store_true", default=False, help="Use old graphics in pygame GUI")
    parser.add_option("-p", dest="pauseSeconds", metavar="SECONDS",
                      action="store", default=0, help="Sets time to pause between moves in AI vs. AI games (default = 0)")


    (options,args) = parser.parse_args()

    game = PythonChessMain(options)
    game.SetUp(options)
    game.MainLoop()
