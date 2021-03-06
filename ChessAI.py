#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessAI.py
 Description:  Contains the AI classes.

 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """

from ChessRules import ChessRules
from ChessBoard import ChessBoard
import random
import datetime
import sys

class hankAI:
    def __init__(self, pieceName, board):
        self.type = 'AI' #might not need this
        self.pieceName = pieceName
        self.board = board
        self.color = self.getColor()
        self.Rules = ChessRules()

    def getType(self):
        return self.type

    def getPieceName(self):
        return self.pieceName

    def getColor(self):
        if 'b' in self.pieceName:
            return 'black'
        else:
            return 'white'

    def minimax(self, piece, board, color):
        # Chance for random move to progress game
        cur = None
        for i in range(8):
            for j in range(8):
                if board[i][j] == piece:
                    cur = (i,j)
        legalMoves = self.Rules.GetListOfValidMoves(board,color,cur)
        if random.random() < 0.0001:
            move = legalMoves[random.randint(0,len(legalMoves)-1)]
            return move
        # Otherwise do minimax
        color1="black"
        if color == "black":
            color1="white"
        best_move = None
        best_score = 0
        for move in legalMoves:
            newBoard = ChessBoard()

            score = 0
            score = newBoard.getCaptureValue(board[move[0]][move[1]])
  
            for i in range(8):
                for j in range(8):
                    newBoard.squares[i][j] = board[i][j]
            board1 = newBoard.GetState()
            moveTuple = (cur, move)
            newBoard.MovePieceAI(moveTuple)
            board1 = newBoard.GetState()
            myPieces = self.GetMyPiecesWithLegalMoves(board1,color1)
            for (x,y) in myPieces:
                piece = board1[x][y]
                legalMoves1 = self.Rules.GetListOfValidMoves(board1,color1,(x,y))
                if len(legalMoves1) == 0:
                    continue
                move1 = legalMoves1[random.randint(0,len(legalMoves1)-1)]
                moveTuple = ((x,y), move1)
                newBoard.MovePieceAI(moveTuple)
            score += newBoard.getScore(piece, newBoard.GetState()) + newBoard.getCaptureValue(newBoard.GetState()[move[0]][move[1]])
            if score > best_score:
                best_score = score
                best_move = move
        print("best move", (cur, best_move))
        if best_move == None:
            return None
        return (cur, best_move)

    def GetMyPiecesWithLegalMoves(self,board,color):
        #print "In ChessAI_random.GetMyPiecesWithLegalMoves"
        if color == "black":
            myColor = 'b'
            enemyColor = 'w'
        else:
            myColor = 'w'
            enemyColor = 'b'

        #get list of my pieces
        myPieces = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if myColor in piece:
                    if len(self.Rules.GetListOfValidMoves(board,color,(row,col))) > 0 and (row,col):
                        myPieces.append((row,col))

        return myPieces

class likeOMGimSoooooRandumbAI(hankAI):

    def testMethod(self):
        print(self.pieceName)

    def randomLegalMoveTuple(self):

        #30% chance of not moving
        if random.randint(1,10) <= 3:
            return None

        current_coordinate = ChessBoard.getCoordinateByPieceName(self.pieceName, self.board)
        moveList = self.Rules.GetListOfValidMoves(self.board, self.color, current_coordinate)

        #no move is possible
        if moveList == []:
            return None

        random.shuffle(moveList)

        #returns a move tuple
        return (current_coordinate, moveList[0])

    # def move_AI(self):
    #     moveTuple = self.randomLegalMoveTuple()
    #     return ChessBoard.movePiece(moveTuple)

class ChessAI:
    def __init__(self,name,color):
        #print "In ChessAI __init__"
        self.name = name
        self.color = color
        self.type = 'AI'
        self.Rules = ChessRules()

    def GetName(self):
        return self.name

    def GetColor(self):
        return self.color

    def GetType(self):
        return self.type


class ChessAI_random(ChessAI):
    #Randomly pick any legal move.

    def __init__(self, name, color):
        #load policies
        self.name = name
        self.color = color
        self.type = 'AI'
        self.Rules = ChessRules()
        file_name="GGEZ.txt"
        self.move_set = {}  # dict
        if file_name is not None:
            self.load_move_set(file_name)
        else:
            self.create_random_moveset('new_moveset_' + str(datetime.datetime.now()) + '.txt')

    def GetName(self):
        return self.name

    def GetColor(self):
        return self.color

    def GetType(self):
        return self.type

    def load_move_set(self, file_name):
        self.move_set = {}
        f = open(file_name, 'r')
        for line in f:
            line = line.split('\t')
            key = (line[0], line[1], line[2])
            value = (int(line[3]), int(line[4].strip()))
            self.move_set[key] = value
        f.close()






    def generate_random_policies(self):
        pieces = ['bR1','bT1','bB1','bQ','bK','bB2','bT2','bR2',
                    'bP1','bP2','bP3','bP4','bP5','bP6','bP7','bP8',
                    'wP1','wP2','wP3','wP4','wP5','wP6','wP7','wP8',
                    'wR1','wT1','wB1','wQ','wK','wB2','wT2','wR2',
                    'wQ1', 'wQ2', 'wQ3', 'wQ4', 'wQ5', 'wQ6', 'wQ7', 'wQ8',
                    'bQ1', 'bQ2', 'bQ3', 'bQ4', 'bQ5', 'bQ6', 'bQ7', 'bQ8']
        #file_name = 'GGEZ_' + str(datetime.datetime.now()) + '.txt'
        file_name = 'GGEZ.txt'
        f = open(file_name, 'w+')
        for piece in pieces:
            for i in range(8):
                for j in range(8):
                    color = 'black'
                    if piece[0] == 'w':
                        color = 'white'
                    cb = ChessBoard(9001)   # over 9000, initializes blank board
                    board = cb.GetState()
                    board[i][j] = piece
                    fromTuple = (i, j)
                    CR = ChessRules()
                    moves = CR.GetListOfValidMoves(board,color,fromTuple)
                    moves.append((i, j))
                    move = random.choice(moves)
                    f.write(piece + '\t' + str(i) + '\t' + str(j) + '\t' + str(move[0]) + '\t' + str(move[1]) + '\n')
        f.close()
        return

    def get_piece_pose(self, piece, board):
        for i in range(8):
            for j in range(8):
                if board[i][j] == piece:
                    return i, j
        return None, None

    def get_move_AI(self, board, color, movedToList):
        myPieces = self.GetMyPiecesWithLegalMoves(board,color,movedToList)
        moves_out = []
        if len(myPieces) < 1:
            return None
        for (x,y) in myPieces:
            piece = board[x][y]
            move = self.move_set[(piece, str(x), str(y))]  #string
            if random.random() < 0.0001:
                legalMoves = self.Rules.GetListOfValidMoves(board,color,(x,y))
                move = legalMoves[random.randint(0,len(legalMoves)-1)]
            if self.Rules.IsLegalMove(board, color, (x,y), move):
                moves_out.append(((x,y), move))
            else:
                moves_out.append(((x,y), (-1,-1)))
        return moves_out

    def GetMove(self,board,color, movedToList):
        #print "In ChessAI_random.GetMove"
        myPieces = self.GetMyPiecesWithLegalMoves(board,color,movedToList)

        if len(myPieces) < 1:
            return None

        #pick a random piece, then a random legal move for that piece
        fromTuple = myPieces[random.randint(0,len(myPieces)-1)]
        legalMoves = self.Rules.GetListOfValidMoves(board,color,fromTuple)
        toTuple = legalMoves[random.randint(0,len(legalMoves)-1)]

        moveTuple = (fromTuple,toTuple)
        return moveTuple

    def GetMyPiecesWithLegalMoves(self,board,color,movedToList):
        #print "In ChessAI_random.GetMyPiecesWithLegalMoves"
        if color == "black":
            myColor = 'b'
            enemyColor = 'w'
        else:
            myColor = 'w'
            enemyColor = 'b'

        #get list of my pieces
        myPieces = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if myColor in piece:
                    if len(self.Rules.GetListOfValidMoves(board,color,(row,col))) > 0 and (row,col) not in movedToList:
                        myPieces.append((row,col))

        return myPieces

class ChessAI_defense(ChessAI_random):
    #For each piece, find it's legal moves.
    #Find legal moves for all opponent pieces.
    #Throw out my legal moves that the opponent could get next turn.
    #From remaining moves, if it puts opponent in check by performing the move, take it.
    #Otherwise pick a random remaining move.

    #Limitation(s): Doesn't include blocking or sacrificial moves of a lesser piece to protect better one.

    def __init__(self,name,color,protectionPriority=("queen","rook","bishop","knight","pawn")):
        self.piecePriority = protectionPriority
        ChessAI.__init__(self,name,color)

    def GetMove(self,board,color,movedToList):
        #print "In ChessAI_defense.GetMove"

        myPieces = self.GetMyPiecesWithLegalMoves(board,color,movedToList)
        enemyPieces = self.GetEnemyPiecesWithLegalMoves(board,color)

        #Get "protected" moves - move piece such that opponent can't capture it next turn
        protectedMoveTuples = self.GetProtectedMoveTuples(board,color,myPieces,enemyPieces)

        #Top priority - pick a protected move that puts the enemy in check
        #print "Looking for move that puts enemy in check..."
        movesThatPutEnemyInCheck = self.GetMovesThatPutEnemyInCheck(board,color,protectedMoveTuples)
        if len(movesThatPutEnemyInCheck) > 0:
            #print "Picking move that puts enemy in check"
            return movesThatPutEnemyInCheck[random.randint(0,len(movesThatPutEnemyInCheck)-1)]

        #Priority #2 - pick a protected move that will move one of player's pieces out of the line of fire
        #piecePriority set when class instantiated
        for pieceType in self.piecePriority:
            #print "Looking for move that protects my "+pieceType+"..."
            piecesProtectedMoves = self.GetMovesThatProtectPiece(board,color,pieceType,protectedMoveTuples)
            if len(piecesProtectedMoves) > 0:
                #print "Picking move that removes "+pieceType+" from danger"
                return piecesProtectedMoves[random.randint(0,len(piecesProtectedMoves)-1)]

        #Priority #3 - pick a protected move that will capture one of the enemy's pieces
        for pieceType in self.piecePriority:
            #print "Looking for move that captures enemy "+pieceType+"..."
            capturePieceMoves = self.GetMovesThatCaptureEnemyPiece(board,color,pieceType,protectedMoveTuples)
            if len(capturePieceMoves) > 0:
                #print "Picking move that captures enemy "+pieceType
                return capturePieceMoves[random.randint(0,len(capturePieceMoves)-1)]

        #If nothing from priority 1,2,and 3, then just pick any protected move
        if len(protectedMoveTuples) > 0:
            #print "Picking random protected move"
            return protectedMoveTuples[random.randint(0,len(protectedMoveTuples)-1)]
        else:
            #If there aren't any protected moves, revert to random AI
            #print "No protected move exists; going to random's GetMove"
            return ChessAI_random.GetMove(self,board,color)

    def GetEnemyPiecesWithLegalMoves(self,board,color):
        #print "In GetEnemyPiecesWithLegalMoves"
        if color == "black":
            myColor = 'b'
            enemyColor = 'w'
            enemyColor_full = 'white'
        else:
            myColor = 'w'
            enemyColor = 'b'
            enemyColor_full = 'black'

        #get list of opponent pieces that have legal moves
        enemyPieces = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if enemyColor in piece:
                    if len(self.Rules.GetListOfValidMoves(board,enemyColor_full,(row,col))) > 0:
                        enemyPieces.append((row,col))

        return enemyPieces

    def GetProtectedMoveTuples(self,board,color,myPieces,enemyPieces):
        #print "In GetProtectedMoveTuples"
        if color == "black":
            myColor = 'b'
            enemyColor = 'w'
            enemyColor_full = 'white'
        else:
            myColor = 'w'
            enemyColor = 'b'
            enemyColor_full = 'black'
        #Get possible moves that opponent can't get next turn
        protectedMoveTuples = []
        for my_p in myPieces:
            my_legalMoves = self.Rules.GetListOfValidMoves(board,color,my_p)
            toBeRemoved = []
            for my_m in my_legalMoves:
                #make hypothetical move
                fromSquare_r = my_p[0]
                fromSquare_c = my_p[1]
                toSquare_r = my_m[0]
                toSquare_c = my_m[1]
                fromPiece = board[fromSquare_r][fromSquare_c]
                toPiece = board[toSquare_r][toSquare_c]
                board[toSquare_r][toSquare_c] = fromPiece
                board[fromSquare_r][fromSquare_c] = 'e'

                for enemy_p in enemyPieces:
                    enemy_moves = self.Rules.GetListOfValidMoves(board,enemyColor_full,enemy_p)
                    for enemy_m in enemy_moves:
                        if enemy_m in my_legalMoves:
                            toBeRemoved.append(enemy_m)

                #undo temporary move
                board[toSquare_r][toSquare_c] = toPiece
                board[fromSquare_r][fromSquare_c] = fromPiece

            for remove_m in toBeRemoved:
                if remove_m in my_legalMoves:
                    my_legalMoves.remove(remove_m)

            for my_m in my_legalMoves: #now, "dangerous" moves are removed
                protectedMoveTuples.append((my_p,my_m))

        return protectedMoveTuples

    def GetMovesThatProtectPiece(self,board,color,pieceType,protectedMoveTuples):
        piecesProtectedMoves = []
        piecePositions = self.PiecePositions(board,color,pieceType)
        if len(piecePositions)>0:
            for p in piecePositions:
                if self.PieceCanBeCaptured(board,color,p):
                    piecesProtectedMoves.extend(self.GetPiecesMovesFromMoveTupleList(p,protectedMoveTuples))
        return piecesProtectedMoves

    def GetMovesThatCaptureEnemyPiece(self,board,color,pieceType,protectedMoveTuples):
        if color == "black":
            myColor = 'b'
            enemyColor = 'w'
            enemyColor_full = 'white'
        else:
            myColor = 'w'
            enemyColor = 'b'
            enemyColor_full = 'black'

        capturePieceMoves = []
        enemyPiecePositions = self.PiecePositions(board,enemyColor,pieceType)
        if len(enemyPiecePositions)>0:
            for p in enemyPiecePositions:
                if self.PieceCanBeCaptured(board,enemyColor,p):
                    capturePieceMoves.extend(self.GetCapturePieceMovesFromMoveTupleList(p,protectedMoveTuples))
        return capturePieceMoves

    def GetMovesThatPutEnemyInCheck(self,board,color,protectedMoveTuples):
        #print "In GetMovesThatPutEnemyInCheck"
        if color == "black":
            myColor = 'b'
            enemyColor = 'w'
            enemyColor_full = 'white'
        else:
            myColor = 'w'
            enemyColor = 'b'
            enemyColor_full = 'black'

        movesThatPutEnemyInCheck = []
        for mt in protectedMoveTuples:
            if self.Rules.DoesMovePutPlayerInCheck(board,enemyColor_full,mt[0],mt[1]):
                movesThatPutEnemyInCheck.append(mt)

        return movesThatPutEnemyInCheck

    def PiecePositions(self,board,color,pieceType):
        #returns list of piece positions; will be empty if color piece doesn't exist on board
        if color == "black":
            myColor = 'b'
        else:
            myColor = 'w'

        if pieceType == "king":
            myPieceType = 'K'
        elif pieceType == "queen":
            myPieceType = 'Q'
        elif pieceType == "rook":
            myPieceType = 'R'
        elif pieceType == "knight":
            myPieceType = 'T'
        elif pieceType == "bishop":
            myPieceType = 'B'
        elif pieceType == "pawn":
            myPieceType = 'P'

        piecePositions = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if myColor in piece and myPieceType in piece:
                    piecePositions.append((row,col))
        return piecePositions

    def PieceCanBeCaptured(self,board,color,p):
        #true if opponent can capture the piece as board currently exists.
        if color == "black":
            myColor = 'b'
            enemyColor = 'w'
            enemyColorFull = 'white'
        else:
            myColor = 'w'
            enemyColor = 'b'
            enemyColorFull = 'black'

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if enemyColor in piece:
                    if self.Rules.IsLegalMove(board,enemyColorFull,(row,col),p):
                        return True
        return False

    def GetCapturePieceMovesFromMoveTupleList(self,p,possibleMoveTuples):
        #returns a subset of possibleMoveTuples that end with p
        moveTuples = []
        for m in possibleMoveTuples:
            if m[1] == p:
                moveTuples.append(m)
        return moveTuples

    def GetPiecesMovesFromMoveTupleList(self,p,possibleMoveTuples):
        #returns a subset of possibleMoveTuples that start with p
        moveTuples = []
        for m in possibleMoveTuples:
            if m[0] == p:
                moveTuples.append(m)
        return moveTuples

class ChessAI_offense(ChessAI_defense):
    #Same as defense AI, except capturing enemy piece is higher priority than protecting own pieces
    def GetMove(self,board,color,movedToList):
        #print "In ChessAI_offense.GetMove"

        myPieces = self.GetMyPiecesWithLegalMoves(board,color,movedToList)
        enemyPieces = self.GetEnemyPiecesWithLegalMoves(board,color)

        #Get "protected" moves - move piece such that opponent can't capture it next turn
        protectedMoveTuples = self.GetProtectedMoveTuples(board,color,myPieces,enemyPieces)

        #Top priority - pick a protected move that puts the enemy in check
        #print "Looking for move that puts enemy in check..."
        movesThatPutEnemyInCheck = self.GetMovesThatPutEnemyInCheck(board,color,protectedMoveTuples)
        if len(movesThatPutEnemyInCheck) > 0:
            #print "Picking move that puts enemy in check"
            return movesThatPutEnemyInCheck[random.randint(0,len(movesThatPutEnemyInCheck)-1)]

        #Priority #2 - pick a protected move that will capture one of the enemy's pieces
        for pieceType in self.piecePriority:
            #print "Looking for move that captures enemy "+pieceType+"..."
            capturePieceMoves = self.GetMovesThatCaptureEnemyPiece(board,color,pieceType,protectedMoveTuples)
            if len(capturePieceMoves) > 0:
                #print "Picking move that captures enemy "+pieceType
                return capturePieceMoves[random.randint(0,len(capturePieceMoves)-1)]

        #Priority #3 - pick a protected move that will move one of player's pieces out of the line of fire
        #piecePriority set when class instantiated
        for pieceType in self.piecePriority:
            #print "Looking for move that protects my "+pieceType+"..."
            piecesProtectedMoves = self.GetMovesThatProtectPiece(board,color,pieceType,protectedMoveTuples)
            if len(piecesProtectedMoves) > 0:
                #print "Picking move that removes "+pieceType+" from danger"
                return piecesProtectedMoves[random.randint(0,len(piecesProtectedMoves)-1)]

        #If nothing from priority 1,2,and 3, then just pick any protected move
        if len(protectedMoveTuples) > 0:
            #print "Picking random protected move"
            return protectedMoveTuples[random.randint(0,len(protectedMoveTuples)-1)]
        else:
            #If there aren't any protected moves, revert to random AI
            #print "No protected move exists; going to random's GetMove"
            return ChessAI_random.GetMove(self,board,color)

if __name__ == "__main__":

    foo = ChessAI_random("test", "black")
    foo.generate_random_policies()
    foo.load_move_set('GGEZ.txt')
    """
    from ChessBoard import ChessBoard
    cb = ChessBoard(3)
    board = cb.GetState()
    color = 'black'

    from ChessGUI_pygame import ChessGUI_pygame
    gui = ChessGUI_pygame()
    gui.Draw(board,highlightSquares=[])
    defense = ChessAI_defense('Bob','black')

    myPieces = defense.GetMyPiecesWithLegalMoves(board,color,movedToList)
    enemyPieces = defense.GetEnemyPiecesWithLegalMoves(board,color)
    protectedMoveTuples = defense.GetProtectedMoveTuples(board,color,myPieces,enemyPieces)
    movesThatPutEnemyInCheck = defense.GetMovesThatPutEnemyInCheck(board,color,protectedMoveTuples)
    print("MyPieces = ", cb.ConvertSquareListToAlgebraicNotation(myPieces))
    print("enemyPieces = ", cb.ConvertSquareListToAlgebraicNotation(enemyPieces))
    print("protectedMoveTuples = ", cb.ConvertMoveTupleListToAlgebraicNotation(protectedMoveTuples))
    print("movesThatPutEnemyInCheck = ", cb.ConvertMoveTupleListToAlgebraicNotation(movesThatPutEnemyInCheck))
    c = input("Press any key to quit.")#pause at the end
    """
