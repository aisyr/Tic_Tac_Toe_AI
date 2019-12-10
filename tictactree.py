import numpy as np
import copy as cp
import pygame
from pygame.locals import *

BLANK = None

# main event loop
running = 1

gameOver = 0

currentSymbol = "+"

value = []

# declare our global variables for the game
XO   = "X"   # track whose turn it is; X goes first
state = np.array([
        ["O", BLANK, BLANK, BLANK],
        [BLANK, "O", "+", "+"],
        ["+", "O", "+", "+"],
        [BLANK, "O", "+", "+"]])

winner = None

def state_str(state, prefix=""):
    return "\n".join("%s%s" % (prefix, "".join(row)) for row in state)

def move(state, symbol, row, col):
    if state[row][col] != BLANK: return False
    new_state = cp.deepcopy(state)
    new_state[row][col] = symbol
    return new_state

def score(state, playerSymbol):
    """
    Determine the score for the state:
    +1 if player "x" has a winning line of 3 "x"'s
    -1 if player "o" has a winning line of 3 "o"'s
    0 otherwise
    
    Version 1: Python lists
    Version 2: Numpy arrays    
    """
    global currentSymbol

    if currentSymbol == "X":
        symbols = "OX"
    elif currentSymbol == "O":
        symbols = "+O"
    else:
        symbols = "X+"

    for symbol, point in zip(symbols, [-1,1]):
        if (state == symbol).all(axis=1).any(): return point
        if (state == symbol).all(axis=0).any(): return point
        if (np.diagonal(state) == symbol).all(): return point
        if (np.diagonal(np.rot90(state)) == symbol).all(): return point
    
    return 0

# def mnx(state, symbol, depth=0):
#     """
#     Minimax search for tic-tac-toe
#     """
#     v = score(state)
#     if v in [-1, 1] or (state != BLANK).all(): return v, [], 1
#     # if v in [-1, 1] or (state != BLANK).all(): return v * 9./(depth+1), [], 1

#     v, a, n = [], [], 0
#     valid_moves = np.nonzero(state == BLANK)
#     for row, col in zip(*valid_moves):
#         child = move(state, symbol, row, col)      
#         childSymbol=""
#         childSymbol1=""

#         if (symbol  == "X"):
#             childSymbol = "O"
#             childSymbol1 = "+"
#         elif (symbol == "O"):
#             childSymbol = "+"
#             childSymbol1 = "X"
#         else:
#             childSymbol = "X"
#             childSymbol1 = "O"

#         v_c, a_c, n_c = mnx(child, childSymbol, depth+1)
#         v.append(v_c)
#         a.append(a_c)
#         v_c1, a_c1, n_c1 = mnx(child, childSymbol1, depth+1)
#         v.append(v_c1)
#         a.append(a_c1)
#         n += n_c
#         n += n_c1       

#     best = np.argmax(v) if symbol == currentSymbol else np.argmin(v)
#     return v[best], [list(zip(*valid_moves))[best]] + a[best], n

    
def mnx(state, symbol, depth=0):
    """
    Minimax search for tic-tac-toe
    """
    global value
    
    v = score(state, symbol)
    if v in [-1, 1] or (state != BLANK).all(): return v, [], 1
    # if v in [-1, 1] or (state != BLANK).all(): return v * 9./(depth+1), [], 1

    v, a, n = [], [], 0
    valid_moves = np.nonzero(state == BLANK)
    for row, col in zip(*valid_moves):
        child = move(state, symbol, row, col)

        if (symbol  == "X"): 
            childSymbol = "O"
        elif (symbol == "O"):
            childSymbol = "+"
        else:
            childSymbol = "X"

        v_c, a_c, n_c = mnx(child, childSymbol, depth+1)
        v.append(v_c)
        a.append(a_c)
        n += n_c
    
    best = np.argmax(v) if symbol == currentSymbol else np.argmin(v)
    return v[best], [list(zip(*valid_moves))[best]] + a[best], n

def drawStatus (board):
    # draw the status (i.e., player turn, etc) at the bottom of the board
    # ---------------------------------------------------------------
    # board : the initialized game board surface where the status will
    #         be drawn

    # gain access to global variables
    global currentSymbol, winner, gameOver, state

    if (currentSymbol == "X"):
        nextSymbol = "O"
    elif (currentSymbol == "O"):
        nextSymbol = "+"
    else:
        nextSymbol = "X"

    # determine the status message
    if (winner is None):
        message = nextSymbol + "'s turn"
    else:
        message = winner + " won!"
        gameOver = 1

    flagGameOver = 1
    for row in range(len(state)):
        for col in range(len(state[row])):
            if (state[row][col] == None):
                flagGameOver = 0

    if (flagGameOver == 1):
        message = "Game Over"

    # render the status message
    font = pygame.font.Font(None, 24)
    text = font.render(message, 1, (10, 10, 10))

    # copy the rendered message onto the board
    board.fill ((250, 250, 250), (0, 400, 400, 25))
    board.blit(text, (10, 400))

def initBoard(ttt):
    # initialize the board and return it as a variable
    # ---------------------------------------------------------------
    # ttt : a properly initialized pyGame display variable

    # set up the background surface
    background = pygame.Surface (ttt.get_size())
    background = background.convert()
    background.fill ((0, 0, 0))

    # draw the grid lines
    # vertical lines...
    pygame.draw.line (background, (250,250,250), (100, 0), (100, 400), 2)
    pygame.draw.line (background, (250,250,250), (200, 0), (200, 400), 2)
    pygame.draw.line (background, (250,250,250), (300, 0), (300, 400), 2)

    # horizontal lines...
    pygame.draw.line (background, (250,250,250), (0, 100), (400, 100), 2)
    pygame.draw.line (background, (250,250,250), (0, 200), (400, 200), 2)
    pygame.draw.line (background, (250,250,250), (0, 300), (400, 300), 2)

    # return the board
    return background

def boardPos (mouseX, mouseY):
    # given a set of coordinates from the mouse, determine which board space
    # (row, column) the user clicked in.
    # ---------------------------------------------------------------
    # mouseX : the X coordinate the user clicked
    # mouseY : the Y coordinate the user clicked

    # determine the row the user clicked
    if (mouseY < 100):
        row = 0
    elif (mouseY < 200):
        row = 1
    elif (mouseY < 300):
        row = 2
    else: 
        row = 3

    # determine the column the user clicked
    if (mouseX < 100):
        col = 0
    elif (mouseX < 200):
        col = 1
    elif (mouseX < 300):
        col = 2
    else:
        col = 3

    # return the tuple containg the row & column
    return (row, col)

def drawMove (board, boardRow, boardCol, Piece):
    # draw an X or O (Piece) on the board in boardRow, boardCol
    # ---------------------------------------------------------------
    # board     : the game board surface
    # boardRow,
    # boardCol  : the Row & Col in which to draw the piece (0 based)
    # Piece     : X or O
    
    # determine the center of the square
    centerX = ((boardCol) * 100) + 50
    centerY = ((boardRow) * 100) + 50

    #if (running == 1):

    # draw the appropriate piece
    if (Piece == 'O'):
        pygame.draw.circle (board, (250,250,250), (centerX, centerY), 44, 2)
    elif(Piece == '+'):
        pygame.draw.line (board, (250,250,250), (centerX-30, centerY), \
                        (centerX+30, centerY), 2)
        pygame.draw.line (board, (250,250,250), (centerX, centerY-30), \
                        (centerX, centerY+30), 2)
    else:
        pygame.draw.line (board, (250,250,250), (centerX - 22, centerY - 22), \
                        (centerX + 22, centerY + 22), 2)
        pygame.draw.line (board, (250,250,250), (centerX + 22, centerY - 22), \
                        (centerX - 22, centerY + 22), 2)

    # mark the space as used
    state [boardRow][boardCol] = Piece

def clickBoard(board, symbol):
    # determine where the user clicked and if the space is not already
    # occupied, draw the appropriate piece there (X or O)
    # ---------------------------------------------------------------
    # board : the game board surface

    global state, XO, gameOver, currentSymbol

    currentSymbol = symbol
    
    (mouseX, mouseY) = pygame.mouse.get_pos()
    (row, col) = boardPos (mouseX, mouseY)

    # make sure no one's used this space
    if ((state[row][col] == "X") or (state[row][col] == "O") or (state[row][col] == "+")):
        # this space is in use
        return

    if (gameOver == 0):
        # draw an X or O
        drawMove (board, row, col, symbol)

        # toggle XO to the other player's move
        # if (XO == "X"):
        #     XO = "O"
        # else:
        #     XO = "X"


def gameWon(board):
    # determine if anyone has won the game
    # ---------------------------------------------------------------
    # board : the game board surface
    
    global state, winner

    # check for winning rows
    for row in range (0, 4):
        if ((state [row][0] == state[row][1] == state[row][2] == state[row][3]) and \
           (state [row][0] is not None)):
            # this row won
            winner = state[row][0]
            pygame.draw.line (board, (250,0,0), (0, (row + 1)*100 - 50), \
                              (400, (row + 1)*100 - 50), 2)
            break

    # check for winning columns
    for col in range (0, 4):
        if (state[0][col] == state[1][col] == state[2][col] == state[3][col]) and \
           (state[0][col] is not None):
            # this column won
            winner = state[0][col]
            pygame.draw.line (board, (250,0,0), ((col + 1)* 100 - 50, 0), \
                              ((col + 1)* 100 - 50, 400), 2)
            break

    # check for diagonal winners
    if (state[0][0] == state[1][1] == state[2][2] == state[3][3]) and \
       (state[0][0] is not None):
        # game won diagonally left to right
        winner = state[0][0]
        pygame.draw.line (board, (250,0,0), (50, 50), (350, 350), 2)

    if (state[0][3] == state[1][2] == state[2][1] == state[3][0]) and \
       (state[0][3] is not None):
        # game won diagonally right to left
        winner = state[0][3]
        pygame.draw.line (board, (250,0,0), (350, 50), (50, 350), 2)


def showBoard (ttt, board):
    # redraw the game board on the display
    # ---------------------------------------------------------------
    # ttt   : the initialized pyGame display
    # board : the game board surface

    drawStatus (board)
    ttt.blit (board, (0, 0))
    pygame.display.flip()

def initStates (board, state):
    for row in range(len(state)):
        for col in range(len(state[row])):
            if (state[row][col] != None):
                drawMove (board, row, col, state[row][col])


def performAIMove(board, symbolAI):
    global currentSymbol, gameOver

    if (gameOver == 0):
        currentSymbol = symbolAI
        value, actions, number = mnx(state, symbolAI)
        
        print (actions)
        if (len(actions) != 0):
            row, col = actions[0]

            drawMove (board, row, col, symbolAI)

    else:
        print('Game is over!!')
 

if __name__ == "__main__":

    global state

    counter = 0

    symbol_one = "X"
    symbol_two = "O"
    symbol_three = "+"

    pygame.init()
    ttt = pygame.display.set_mode ((400, 425))
    pygame.display.set_caption ('Tic Tac Toe')

    board = initBoard (ttt)

    initStates(board, state)

    while (running == 1):
        for event in pygame.event.get():
            if event.type is QUIT:
                running = 0
            elif event.type is MOUSEBUTTONDOWN:
                # the user clicked; place an X or O
                counter = counter+1

                if(counter % 2 == 1):
                    clickBoard(board, symbol_one)
                    # check for a winner
                    gameWon (board)
                    # update the display
                    showBoard (ttt, board)

                elif(counter % 2 == 0):
                    clickBoard(board, symbol_two)
                    # check for a winner
                    gameWon (board)
                    # update the display
                    showBoard (ttt, board)

                    performAIMove(board, symbol_three)
                    # check for a winner
                    gameWon (board)
                    # update the display
                    showBoard (ttt, board)

            # update the display
            showBoard (ttt, board)
