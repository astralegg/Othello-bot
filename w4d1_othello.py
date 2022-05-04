import turtle
import math
import copy
import random
import time

# Constants
boardsize = 300
margin = 50


playerColors = {
    'black' : 'b',
    'white' : 'w',
    'w' : 'white',
    'b' : 'black'
}

# Initialization
def initializeTurtle():
    global t
    global s

    t = turtle.Turtle()
    s = turtle.Screen()
    s.tracer(0,0)
    s.bgcolor('forest green')
    s.setup(boardsize+2*margin, boardsize+2*margin)
    t.hideturtle()


def initialize(board):
    updateBoard(board, 'white', 3, 3)
    updateBoard(board, 'black', 3, 4)
    updateBoard(board, 'white', 4, 4)
    updateBoard(board, 'black', 4, 3)



# Functions

def drawBoard():
        t.penup()
        t.goto(boardsize/2,boardsize/2)
        t.pendown()
        t.setheading(270)
        for i in range(0, 4):
            t.forward(boardsize)
            t.right(90)
        for i in range(0,7):
            t.penup()
            t.goto(t.xcor()-(boardsize/8),boardsize/2)
            t.pendown()
            t.forward(boardsize)
            t.penup()
        t.setheading(180)
        t.goto(boardsize/2,boardsize/2)
        for i in range(0,7):
            t.penup()
            t.goto(boardsize/2,t.ycor()-(boardsize/8))
            t.pendown()
            t.forward(boardsize)
            t.penup()
        turtle.update()

def whichRow(y):
    return(8-math.ceil(((y+(boardsize/2))/boardsize)*8))

def whichColumn(x):
    return(math.ceil(((x+(boardsize/2))/boardsize)*8)-1)

def xFromColumn(column):
    return(column*(boardsize/8)-boardsize/2+boardsize/16)

def yFromRow(row):
    return(boardsize/2-(row*(boardsize/8))-boardsize/16)

def stampPlayer(row, column, player):

    t.penup()
    t.shape('circle')
    t.goto(xFromColumn(column),yFromRow(row))
    t.color(player)
    t.stamp()

def updateBoard(board, player, row, col):
    board[row][col] = playerColors[player]

def calculateScore(board,player):
    return(len([element for sublist in [z for z in [[y for y in x if y == playerColors[player]] for x in board] if z != []] for element in sublist]))

def updateText():

    t.color('black')
    t.goto(-boardsize/2-10, boardsize/2+10)
    t.write('black: ' + str(calculateScore(gameBoard, 'black')) + ' | ' +  'white: ' + str(calculateScore(gameBoard, 'white')))
    t.goto(-boardsize/2+70, boardsize/2+10)
    t.write('current player: '+currentPlayer)



def stampBoard(board):
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] != 0:
                stampPlayer(r, c, playerColors[board[r][c]])

def oppColor(player):
    if player == 'white':
        return 'black'
    if player == 'black':
        return 'white'


def validMove(board, player, row, column):
    if board[row][column] == 0:
        for r in [-1,0,1]:
            for c in [-1,0,1]:
                try:
                    if board[row+r][column+c] == playerColors[oppColor(player)]:
                        count = 1
                        while board[row+r*count][column+c*count] == playerColors[oppColor(player)]:
                            count+=1
                        if board[row + r*count][column + c*count] == playerColors[player] and row+r*count >= 0 and column+c*count >= 0:
                            return True
                        else:
                            pass
                except IndexError:
                    pass

    return False

def allMoves(board,player):
    output = []
    for r in range(0,8):
        for c in range(0,8):
            if validMove(board, player, r, c):
                output.append([r,c])
    return output

def nextBoard(board, player, move):
    row = move[0]
    column = move[1]
    output = [[y for y in x] for x in board]
    output[row][column] = playerColors[player]
    for r in [-1,0,1]:
        for c in [-1,0,1]:
            try:
                if board[row+r][column+c] == playerColors[oppColor(player)]:
                    count = 1
                    while board[row + r*count][column + c*count] == playerColors[oppColor(player)]and count<7:
                        count+=1
                    if board[row+r*count][column+c*count] == playerColors[player] and row+r*count >= 0 and column+c*count >= 0:
                        for i in range(count):
                            if row+r*i >= 0 and column+c*i >= 0:
                                output[row+r*i][column+c*i] = playerColors[player]
            except IndexError:
                pass
    return output

def click(x,y):
    global gameBoard
    global currentPlayer

    row = whichRow(y)
    col = whichColumn(x)
    if validMove(gameBoard,currentPlayer,row,col):
        makeMove(gameBoard,currentPlayer,[row,col])
        if len(allMoves(gameBoard,currentPlayer)) > 0:
            makeMove(gameBoard,currentPlayer,pickMove(gameBoard,currentPlayer))
        elif len(allMoves(gameBoard,oppColor(currentPlayer))) > 0:
            currentPlayer = oppColor(currentPlayer)
            clearPrints()
            updateText()
        else:
            gameEnd()
            return
        if len(allMoves(gameBoard,currentPlayer)) == 0:
            gameEnd()
            return



def gameEnd():
    clearPrints()
    t.color('black')
    t.goto(-boardsize/2-10, boardsize/2+10)
    if calculateScore(gameBoard,'black')>calculateScore(gameBoard,'white'):
        t.write('Game Over. Black Wins.')
    if calculateScore(gameBoard,'white')>calculateScore(gameBoard,'black'):
        t.write('Game Over. White Wins.')


def makeMove(board, player, move):
    global gameBoard
    global currentPlayer
    clearPrints()
    gameBoard = nextBoard(gameBoard,currentPlayer,move)
    currentPlayer = oppColor(currentPlayer)
    updateText()
    stampBoard(gameBoard)


def clearPrints():
    t.pensize(10)
    t.penup()
    t.color('forest green')
    t.goto(boardsize/2-10, boardsize/2+15)
    t.pendown()
    t.forward(boardsize)
    t.penup()



#bot functions

def pickMove(board,player):
    global currentPlayer
    # return random.choice(allMoves(board,player))
    return minimax(gameBoard,currentPlayer,'maxNode',4)[1]


    return random.choice(allMoves(board,player))

def evaluateBoard(board, player):
    my_color = playerColors[player]
    opp_color = playerColors[oppColor(player)]
    my_tiles = 0
    opp_tiles = 0
    my_front_tiles = 0
    opp_front_tiles = 0
    x = 0
    y = 0
    p = 0
    c = 0
    l = 0
    m = 0
    f = 0
    d = 0
    X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
    Y1 = [0, 1, 1, 1, 0, -1, -1, -1]
    V = [[0 for _ in range(8)] for _ in range(8)]
    V[0] = [20, -3, 11, 8, 8, 11, -3, 20]
    V[1] = [-3, -7, -4, 1, 1, -4, -7, -3]
    V[2] = [11, -4, 2, 2, 2, 2, -4, 11]
    V[3] = [8, 1, 2, -3, -3, 2, 1, 8]
    V[4] = [8, 1, 2, -3, -3, 2, 1, 8]
    V[5] = [11, -4, 2, 2, 2, 2, -4, 11]
    V[6] = [-3, -7, -4, 1, 1, -4, -7, -3]
    V[7] = [20, -3, 11, 8, 8, 11, -3, 20]

# Piece difference, frontier disks and disk squares
    for row in range(8):
        for column in range(8):
            if board[row][column] == my_color:
                d += V[row][column]
                my_tiles += 1
            elif board[row][column] == opp_color:
                d -= V[row][column]
                opp_tiles += 1
            if board[row][column] != 0:
                for k in range(8):
                    x = row + X1[k]
                    y = column + Y1[k]
                    if x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] == 0:
                        if board[row][column] == my_color:
                            my_front_tiles += 1
                        else:
                            opp_front_tiles += 1
    if my_tiles > opp_tiles :
        p = (100.0 * my_tiles)/(my_tiles + opp_tiles)
    elif my_tiles < opp_tiles:
        p = -(100.0 * opp_tiles)/(my_tiles + opp_tiles)
    else:
        p = 0

    if my_front_tiles > opp_front_tiles:
        f = -(100.0 * my_front_tiles)/(my_front_tiles + opp_front_tiles)
    elif my_front_tiles < opp_front_tiles:
        f = (100.0 * opp_front_tiles)/(my_front_tiles + opp_front_tiles)
    else:
        f = 0

#  Corner occupancy
    my_tiles = opp_tiles = 0
    if board[0][0] == my_color:
        my_tiles += 1
    elif board[0][0] == opp_color:
        opp_tiles += 1
    if board[0][7] == my_color:
         my_tiles += 1
    elif board[0][7] == opp_color:
        opp_tiles += 1
    if board[7][0] == my_color:
        my_tiles += 1
    elif board[7][0] == opp_color:
        opp_tiles += 1
    if board[7][7] == my_color:
        my_tiles += 1
    elif board[7][7] == opp_color:
        opp_tiles += 1
    c = 25 * (my_tiles - opp_tiles)

#  Corner closeness
    my_tiles = opp_tiles = 0

    if board[0][0] == 0:
        if board[0][1] == my_color:
            my_tiles +=1
        elif board[0][1] == opp_color:
            opp_tiles += 1
        if board[1][1] == my_color:
            my_tiles += 1
        elif board[1][1] == opp_color:
            opp_tiles += 1
        if board[1][0] == my_color:
            my_tiles += 1
        elif board[1][0] == opp_color:
            opp_tiles += 1

    if board[0][7] == 0:
        if board[0][6] == my_color:
            my_tiles += 1
        elif board[0][6] == opp_color:
            opp_tiles += 1
        if board[1][6] == my_color:
            my_tiles += 1
        elif board[1][6] == opp_color:
            opp_tiles += 1
        if board[1][7] == my_color:
            my_tiles += 1
        elif board[1][7] == opp_color:
            opp_tiles += 1

    if board[7][0] == 0:
        if board[7][1] == my_color:
            my_tiles += 1
        elif board[7][1] == opp_color:
            opp_tiles += 1
        if board[6][1] == my_color:
            my_tiles += 1
        elif board[6][1] == opp_color:
            opp_tiles += 1
        if board[6][0] == my_color:
            my_tiles += 1
        elif board[6][0] == opp_color:
            opp_tiles += 1

    if board[7][7] == 0:
        if board[6][7] == my_color:
            my_tiles += 1
        elif board[6][7] == opp_color:
            opp_tiles += 1
        if board[6][6] == my_color:
            my_tiles += 1
        elif board[6][6] == opp_color:
            opp_tiles += 1
        if board[7][6] == my_color:
            my_tiles += 1
        elif board[7][6] == opp_color:
            opp_tiles += 1

    l = -12.5 * (my_tiles - opp_tiles);

#  Mobility
    my_tiles = len(allMoves(board, player))
    opp_tiles = len(allMoves(board, oppColor(player)))
    if my_tiles > opp_tiles:
        m = (100.0 * my_tiles)/(my_tiles + opp_tiles);
    elif my_tiles < opp_tiles:
        m = -(100.0 * opp_tiles)/(my_tiles + opp_tiles);
    else:
        m = 0

#  final weighted score
    score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)
    return score




    # return calculateScore(board,player)


def minFirst(a,b):
    if a[0] <= b[0]:
        return a
    else:
        return b

def maxFirst(a,b):
    if a[0] >= b[0]:
        return a
    else:
        return b



# def minimax(board,player,n,depth,alpha = [-math.inf,['no','no']], beta = [math.inf,['no','no']]):
#     moveVal = []
#     print(depth)
#     if depth == 0:
#         return [evaluateBoard(board,player),'no']
#
#     if n == 'minNode':
#         for moveChild in allMoves(board,player):
#             newMoveVal = [minimax(nextBoard(board, player, moveChild), player, 'maxNode', depth-1, alpha, beta)[0],moveChild]
#             beta[0] = min(beta[0], newMoveVal[0])
#             if beta[0] <= alpha[0]:
#                 return beta
#                 # moveVal = beta
#             # moveVal = beta
#
#         #     if newMoveVal[0] < moveVal[0]:
#         #         moveVal = newMoveVal
#         # return moveVal
#         return beta
#
#     if n == 'maxNode':
#         for moveChild in allMoves(board,player):
#             newMoveVal = [minimax(nextBoard(board, player, moveChild), player, 'minNode', depth-1, alpha, beta)[0],moveChild]
#             alpha[0] = max(alpha[0], newMoveVal[0])
#             if beta[0] <= alpha[0]:
#                 return alpha
#             #     moveVal = alpha
#             # moveVal = alpha
#
#         #     if newMoveVal[0] > moveVal[0]:
#         #         moveVal = newMoveVal
#         # return moveVal
#         return alpha


# def minimax(board,player,n,depth):
#
#     if depth == 0:
#         return [evaluateBoard(board,player),'no']
#
#     if n == 'minNode':
#         moveVal = [math.inf,['no','no']]
#         for moveChild in allMoves(board,player):
#             newMoveVal = [minimax(nextBoard(board, player, moveChild), player, 'maxNode', depth-1)[0],moveChild]
#
#             if newMoveVal[0] < moveVal[0]:
#                 moveVal = newMoveVal
#
#     if n == 'maxNode':
#         moveVal = [-math.inf,['no','no']]
#         for moveChild in allMoves(board,player):
#             newMoveVal = [minimax(nextBoard(board, player, moveChild), player, 'minNode', depth-1)[0],moveChild]
#
#             if newMoveVal[0] > moveVal[0]:
#                 moveVal = newMoveVal
#     return moveVal


def minimax(board,player,n,depth,alpha=[-math.inf,['no','no']],beta=[math.inf,['no','no']]):
    print(board)
    if depth == 0:
        return [evaluateBoard(board,player),'no']

    if n == 'minNode':
        moveVal = [math.inf,['no','no']]
        for moveChild in allMoves(board,player):
            newMoveVal = [minimax(nextBoard(board, player, moveChild), player, 'maxNode', depth-1, alpha, beta)[0],moveChild]
            moveVal = minFirst(newMoveVal,moveVal)
            beta = minFirst(beta, moveVal)
            if beta[0] <= alpha[0]:
                break
        return moveVal
    if n == 'maxNode':
        moveVal = [-math.inf,['no','no']]
        for moveChild in allMoves(board,player):

            newMoveVal = [minimax(nextBoard(board, player, moveChild), player, 'minNode', depth-1, alpha, beta)[0],moveChild]
            moveVal = maxFirst(newMoveVal,moveVal)
            alpha = maxFirst(alpha, moveVal)

            if beta[0] <= alpha[0]:
                break

        return moveVal


# Game running
gameBoard = [[0 for _ in range(8)] for _ in range(8)]

# gameBoard = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 'b', 0, 0, 0, 0], [0, 0, 0, 'b', 'b', 0, 0, 0], [0, 0, 0, 'b', 'w', 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

initializeTurtle()
initialize(gameBoard)
drawBoard()
stampBoard(gameBoard)
currentPlayer = 'black'
updateText()

# print(allMoves(gameBoard,'white'))

s.onclick(click)
turtle.mainloop()
