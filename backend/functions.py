import sys
import numpy as np
import random
import re
import copy

blank = 0
x = 1
o = 2
X = 3
O = 4

N = 8
WIN_SCORE = sys.maxsize
PAWN_SCORE = 20
KING_SCORE = 50

maxDepth = 3

ERROR = -1

def isError(B):
    if type(B) == int:
        return B == ERROR
    else:
        return False

def isX(p):
    return p % 2 == x

def isO(p):
    return p != blank and p % 2 == o % 2

def belongsToPlayer(piece, player):
    if player == x:
        return isX(piece)
    else:
        return isO(piece)
    
def getEmptyBoard():
    return np.zeros((N,N)).astype(int)

def setRow(board,row,values):
    if len(values) > len(board) or row < 0 or row >= len(board):
        return ERROR
    for col, val in enumerate(values):
        board[row][col] = val
    return board

def getStartingBoard():
    b = getEmptyBoard()
    setRow(b,0,[0, o]*4)
    setRow(b,1,[o, 0]*4)
    setRow(b,2,[0, o]*4)
    setRow(b,5,[x, 0]*4)
    setRow(b,6,[0, x]*4)
    setRow(b,7,[x, 0]*4)
    return b

def findAvailableMovesForKing(board,pieceLoc,isOpponent):
    row = pieceLoc[0]
    col = pieceLoc[1]
    availableMoves = []
    if col > 0 and row > 0 and board[row-1][col-1] == blank:
        availableMoves.append([row-1, col-1])
    elif col > 1 and row > 1 and isOpponent(board[row-1][col-1]) and board[row-2][col-2] == blank:
        availableMoves.append([row-2, col-2])
    if col < 7 and row > 0 and board[row-1][col+1] == blank:
        availableMoves.append([row-1, col+1])
    elif col < 6 and row > 1 and isOpponent(board[row-1][col+1]) and board[row-2][col+2] == blank:
        availableMoves.append([row-2, col+2])
    if col > 0 and row < 7 and board[row+1][col-1] == blank:
        availableMoves.append([row+1, col-1])
    elif col > 1 and row < 6 and isOpponent(board[row+1][col-1]) and board[row+2][col-2] == blank:
        availableMoves.append([row+2, col-2])
    if col < 7 and row < 7 and board[row+1][col+1] == blank:
        availableMoves.append([row+1, col+1])
    elif col < 6 and row < 6 and isOpponent(board[row+1][col+1]) and board[row+2][col+2] == blank:
        availableMoves.append([row+2, col+2])
    return availableMoves

    
def findAvailableMoves(board,pieceLoc):
    row = pieceLoc[0]
    col = pieceLoc[1]
    piece = board[row][col]
    
    availableMoves = []
    
    if piece == x and row > 0:
        if col > 0 and board[row-1][col-1] == blank:
            availableMoves.append([row-1, col-1])
        elif col > 1 and row > 1 and isO(board[row-1][col-1]) and board[row-2][col-2] == blank:
            availableMoves.append([row-2, col-2])
        if col < 7 and board[row-1][col+1] == blank:
            availableMoves.append([row-1, col+1])
        elif col < 6 and row > 1 and isO(board[row-1][col+1]) and board[row-2][col+2] == blank:
            availableMoves.append([row-2, col+2])
    elif piece == o and row < 7:
        if col > 0 and board[row+1][col-1] == blank:
            availableMoves.append([row+1, col-1])
        elif col > 1 and row < 6 and isX(board[row+1][col-1]) and board[row+2][col-2] == blank:
            availableMoves.append([row+2, col-2])
        if col < 7 and board[row+1][col+1] == blank:
            availableMoves.append([row+1, col+1])
        elif col < 6 and row < 6 and isX(board[row+1][col+1]) and board[row+2][col+2] == blank:
            availableMoves.append([row+2, col+2])
    elif piece == X:
        availableMoves += findAvailableMovesForKing(board,pieceLoc,isO)
    elif piece == O:
        availableMoves += findAvailableMovesForKing(board,pieceLoc,isX)
    
    return availableMoves
    

def makeMove(board,player,moveFrom,moveTo):
    pieceToMove = board[moveFrom[0]][moveFrom[1]]
    # check to ensure valid piece is being moved
    if not belongsToPlayer(pieceToMove, player):
        return ERROR
    # check to ensure move is valid
    if moveTo not in findAvailableMoves(board,moveFrom):
        return ERROR
    # remove jumped piece if there is a jump
    if abs(moveTo[1] - moveFrom[1]) == 2:
        board[round((moveFrom[0] + moveTo[0]) / 2)][round((moveFrom[1] + moveTo[1]) / 2)] = blank
    # check if piece upgrades to a king, update if so
    if pieceToMove == x and moveTo[0] == 0:
        pieceToMove = X
    elif pieceToMove == o and moveTo[0] == 7:
        pieceToMove = O
    # update board with move
    board[moveTo[0]][moveTo[1]] = pieceToMove
    board[moveFrom[0]][moveFrom[1]] = blank
    return board

def checkWin(board, player):
    for row in reversed(range(N)):
        for col in reversed(range(N)):
            if not belongsToPlayer(board[row][col], player):
                return 0
    return player


def getListOfPiecePositions(board, player):
    pieces = []
    for row in reversed(range(N)):
        for col in reversed(range(N)):
            if belongsToPlayer(board[row][col], player):
                pieces.append([row, col])
    return pieces


# evaluates the board with respect to 'o' player
def eval(board):
    if checkWin(board, x) == x:
        return -WIN_SCORE
    elif checkWin(board, o) == o:
        return WIN_SCORE
    score = 0
    for row in range(N):
        for col in range(N):
            piece = board[row][col]
            if piece == blank:
                continue
            elif piece == x:
                score -= PAWN_SCORE
            elif piece == o:
                score += PAWN_SCORE
            elif piece == X:
                score -= KING_SCORE
            elif piece == O:
                score += KING_SCORE
    return score


# random player plays as 'o' or 'O'
def randomPlayer(board):
    pieces = getListOfPiecePositions(board, o)
    moveFrom = random.choice(pieces)
    while len(findAvailableMoves(board, moveFrom)) == 0:
        moveFrom = random.choice([x for x in pieces if x != moveFrom])
    return [moveFrom, random.choice(findAvailableMoves(board, moveFrom))]


def minimax(board, player, depth, alpha, beta):
    board = copy.deepcopy(board)
    score = eval(board)
    if depth == maxDepth or abs(score) == sys.maxsize:
        return (score, None)
    
    if player == o: # MAXIMIZING PLAYER (o)
        (best_score, best_move) = (-sys.maxsize, None)
        for piece in getListOfPiecePositions(board, o):
            for move in findAvailableMoves(board, piece):
                backupBoard = copy.deepcopy(board)
                makeMove(board, player, piece, move)
                (val, _) = minimax(board, x, depth+1, alpha, beta)
                board = backupBoard
                if val >= best_score:
                    (best_score, best_move) = (val, [piece, move])
                alpha = max(alpha, best_score)
                if beta < alpha:
                    break
        return (best_score, best_move)
    else: # MINIMIZING PLAYER (x)
        (best_score, best_move) = (sys.maxsize, None)
        for piece in getListOfPiecePositions(board, x):
            for move in findAvailableMoves(board, piece):
                backupBoard = copy.deepcopy(board)
                makeMove(board, player, piece, move)
                (val, _) = minimax(board, o, depth+1, alpha, beta)
                board = backupBoard
                if val <= best_score:
                    (best_score, best_move) = (val, [piece, move])
                beta = min(beta, best_score)
                if beta < alpha:
                    break
        return (best_score, best_move)
    
    
def minimaxPlayer(board):
    (_, move) = minimax(board, o, 0, -sys.maxsize, sys.maxsize)
    return move