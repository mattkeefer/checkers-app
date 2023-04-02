from flask import Flask, request
from functions import getStartingBoard, makeMove, checkWin, randomPlayer, minimaxPlayer

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Checkers by Matt Keefer'

@app.route('/newBoard')
def resetBoard():
    return convertBoardToResponse(getStartingBoard())

@app.route('/makeMove')
def move():
    board = getBoardFromParams()
    player = request.args.get('player')
    moveFromRow = request.args.get('moveFromRow')
    moveFromCol = request.args.get('moveFromCol')
    moveToRow = request.args.get('moveToRow')
    moveToCol = request.args.get('moveToCol')
    return convertBoardToResponse(makeMove(board, int(player), [int(moveFromRow), int(moveFromCol)], [int(moveToRow), int(moveToCol)]))

@app.route('/checkWin')
def win():
    board = getBoardFromParams()
    player = request.args.get('player')
    return str(checkWin(board, int(player)))

@app.route('/randomPlayer')
def random():
    board = getBoardFromParams()
    return randomPlayer(board)

@app.route('/minimaxPlayer')
def minimax():
    board = getBoardFromParams()
    return minimaxPlayer(board)

def getBoardFromParams():
    board = []
    for i in range(8):
        row = []
        for c in request.args.get(str(i)):
            row.append(int(c))
        board.append(row)
    return board

def convertBoardToResponse(board):
    if board == -1:
        return -1
    response = {}
    for i,row in enumerate(board):
        response[str(i)] = list(map(int, list(row)))
    return response