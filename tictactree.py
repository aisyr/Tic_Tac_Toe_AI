import numpy as np
import copy as cp
import pygame
from pygame.locals import *

BLANK = None


class TicTacToe:
      
    def __init__(self):
        self.running = 1
        self.gameOver = 0
        self.currentSymbol = "X"
        self.winner=None
        self.XO = "X"
        self.state = []
        self.dimension = 0
        self.Dict = {}
        
    def state_str(self,state, prefix=""):
        return "\n".join("%s%s" % (prefix, "".join(row)) for row in state)
    
    def move(self,state, symbol, row, col):
        if state[row][col] != BLANK: return False
        new_state = cp.deepcopy(state)
        new_state[row][col] = symbol
        return new_state
    
    def score(self,state):
        """
        Determine the score for the state:
        +1 if player "x" has a winning line of 3 "x"'s
        -1 if player "o" has a winning line of 3 "o"'s
        0 otherwise
        
        Version 1: Python lists
        Version 2: Numpy arrays    
        """
        if self.currentSymbol == "X":
            symbols = "O+X"
        elif self.currentSymbol == "O":
            symbols = "+XO"
        else:
            symbols = "XO+"
    
        for symbol, point in zip(symbols, [-1,-1,1]):
            if (state == symbol).all(axis=1).any(): return point
            if (state == symbol).all(axis=0).any(): return point
            if (np.diagonal(state) == symbol).all(): return point
            if (np.diagonal(np.rot90(state)) == symbol).all(): return point
        
        return 0
    
    
    def mnx(self,state, symbol, depth=0):
        """
        Minimax search for tic-tac-toe
        """
        v = self.score(state)
        if v in [-1, 1] or (state != BLANK).all(): return v, [], 1
        # if v in [-1, 1] or (state != BLANK).all(): return v * 9./(depth+1), [], 1
        
        stateString = state.tostring()
        if (stateString, symbol, depth) in self.Dict:
            return self.Dict[stateString, symbol, depth]
    
        v, a, n = [], [], 0
        valid_moves = np.nonzero(state == BLANK)
        for row, col in zip(*valid_moves):
            child = self.move(state, symbol, row, col)
            
            childSymbol=""
            if (symbol  == "X"): 
                childSymbol = "O"
            elif (symbol == "O"):
                childSymbol = "+"
            else:
                childSymbol = "X"
    
            v_c, a_c, n_c = self.mnx(child, childSymbol, depth+1)
            self.Dict[child.tostring(), childSymbol, depth+1] = v_c, a_c, n_c
            #v_c, a_c, n_c = self.mnx(child, childSymbol1, depth+1)
            v.append(v_c)
            a.append(a_c)
            n += n_c
#             v_c1, a_c1, n_c1 = self.mnx(child, childSymbol1, depth+1)
#             v.append(v_c1)
#             a.append(a_c1)
#             n += n_c1
            
        best = np.argmax(v) if symbol == self.currentSymbol else np.argmin(v)
        return v[best], [list(zip(*valid_moves))[best]] + a[best], n
    
    def drawStatus (self,board):
        # draw the status (i.e., player turn, etc) at the bottom of the board
        # ---------------------------------------------------------------
        # board : the initialized game board surface where the status will
        #         be drawn
    
        # gain access to global variables
        #global XO, winner, gameOver
    
        # determine the status message
        if (self.winner is None):
            message = self.XO + "'s turn"
        else:
            message = self.winner + " won!"
            self.gameOver = 1
            
        # render the status message
        font = pygame.font.Font(None, 24)
        text = font.render(message, 1, (10, 10, 10))
    
        # copy the rendered message onto the board
        board.fill ((250, 250, 250), (0, self.dimension*100, self.dimension*100, 25))
        board.blit(text, (10, self.dimension*100))
    
    def initBoard(self,ttt):
        # initialize the board and return it as a variable
        # ---------------------------------------------------------------
        # ttt : a properly initialized pyGame display variable
    
        # set up the background surface
        background = pygame.Surface (ttt.get_size())
        background = background.convert()
        background.fill ((0, 0, 0))
    
        for i in range(self.dimension):
            pygame.draw.line (background, (250,250,250), ((i+1)*100, 0), ((i+1)*100, self.dimension*100), 2)
            pygame.draw.line (background, (250,250,250), (0,(i+1)*100), (self.dimension*100,(i+1)*100), 2)
#             
#         # draw the grid lines
#         # vertical lines...
#         pygame.draw.line (background, (250,250,250), (100, 0), (100, 400), 2)
#         pygame.draw.line (background, (250,250,250), (200, 0), (200, 400), 2)
#         pygame.draw.line (background, (250,250,250), (300, 0), (300, 400), 2)
#     
#         # horizontal lines...
#         pygame.draw.line (background, (250,250,250), (0, 100), (400, 100), 2)
#         pygame.draw.line (background, (250,250,250), (0, 200), (400, 200), 2)
#         pygame.draw.line (background, (250,250,250), (0, 300), (400, 300), 2)
    
        # return the board
        return background
    
    def boardPos (self,mouseX, mouseY):
        # given a set of coordinates from the mouse, determine which board space
        # (row, column) the user clicked in.
        # ---------------------------------------------------------------
        # mouseX : the X coordinate the user clicked
        # mouseY : the Y coordinate the user clicked
    
        # determine the row the user clicked
        
        for dim in range(self.dimension):
            if(mouseX < (dim+1)*100):
                col = dim
                break
        
        for dim in range(self.dimension):
            if(mouseY < (dim + 1)*100):
                row = dim
                break
        
#         if (mouseY < 100):
#             row = 0
#         elif (mouseY < 200):
#             row = 1
#         elif (mouseY < 300):
#             row = 2
#         else: 
#             row = 3
#     
#         # determine the column the user clicked
#         if (mouseX < 100):
#             col = 0
#         elif (mouseX < 200):
#             col = 1
#         elif (mouseX < 300):
#             col = 2
#         else:
#             col = 3
    
        # return the tuple containg the row & column
        return (row, col)
    
    def drawMove (self,board, boardRow, boardCol, Piece):
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
        self.state [boardRow][boardCol] = Piece
    
    def clickBoard(self,board, symbol):
        # determine where the user clicked and if the space is not already
        # occupied, draw the appropriate piece there (X or O)
        # ---------------------------------------------------------------
        # board : the game board surface
            
        (mouseX, mouseY) = pygame.mouse.get_pos()
        (row, col) = self.boardPos (mouseX, mouseY)
    
        # make sure no one's used this space
        if ((self.state[row][col] == "X") or (self.state[row][col] == "O") 
            or (self.state[row][col] == "+")):
            # this space is in use
            return
    
        if (self.gameOver == 0):
            # draw an X or O
            self.currentSymbol = symbol
            self.drawMove (board, row, col, symbol)
    
            # toggle XO to the other player's move
            # if (XO == "X"):
            #     XO = "O"
            # else:
            #     XO = "X"
    
    
    def gameWon(self,board):
        # determine if anyone has won the game
        # ---------------------------------------------------------------
        # board : the game board surface
    #    global state, winner
        gameWon = False
        
        # check for winning rows
        for row in range (self.dimension):
            if (self.state[row] == self.currentSymbol).all():
                self.winner = self.currentSymbol    
                gameWon = True
                pygame.draw.line (board, (250,0,0), (0, (row + 1)*100 - 50), \
                                  (self.dimension * 100, (row + 1)*100 - 50), 2)
                break
    
        # check for winning columns
        for col in range (self.dimension):
            if (self.state[:,col] == self.currentSymbol).all():
                self.winner = self.currentSymbol    
                gameWon = True
                pygame.draw.line (board, (250,0,0), ((col + 1)* 100 - 50, 0), \
                                  ((col + 1)* 100 - 50, self.dimension*100), 2)
                break
            
        # check for diagonal winners
        if (np.diagonal(self.state) == self.currentSymbol).all():
            self.winner = self.currentSymbol
            gameWon = True
            pygame.draw.line (board, (250,0,0), (50, 50), (self.dimension*100-50, self.dimension*100-50), 2)
        
        if (np.diagonal(np.rot90(self.state)) == self.currentSymbol).all():
            self.winner = self.currentSymbol
            gameWon = True
            pygame.draw.line (board, (250,0,0), (self.dimension*100-50, 50), (50, self.dimension*100-50), 2)
        
        return gameWon
    
    def text1(self,word,x,y):
        font = pygame.font.SysFont(None, 25)
        text = font.render("{}".format(word), True, (0,0,0))
        return ttt.blit(text,(x,y))
    
    def inpt(self):
        word=""
        self.text1("Please enter your name: ",0,10)
    
    def showBoard (self,ttt, board):
        # redraw the game board on the display
        # ---------------------------------------------------------------
        # ttt   : the initialized pyGame display
        # board : the game board surface
    
        self.drawStatus (board)
        ttt.blit (board, (0, 0))
        pygame.display.flip()
    
    def initStates (self,board, state):
        for row in range(len(state)):
            for col in range(len(state[row])):
                if (self.state[row][col] != None):
                    self.drawMove (board, row, col, self.state[row][col])
    
    
    def performAIMove(self,board, symbolAI):
        if (self.gameOver == 0):
            self.currentSymbol = symbolAI
            value, actions, number = self.mnx(self.state, symbolAI)
            
            row, col = actions[0]
    
            self.drawMove (board, row, col, symbolAI)
    
    def preFillData(self):
        self.state[0][0] = "O"
        self.state[1][1] = "O"
        self.state[1][2] = "+"
        self.state[1][3] = "+"
        self.state[2][0] = "+"
        self.state[2][1] = "O"
        self.state[2][2] = "+"
        self.state[2][3] = "+"
        self.state[3][1] = "O"
        self.state[3][2] = "+"
        self.state[3][3] = "+"
        
    def setupGame(self,dimension):
        pygame.init()
        #self.dimension = dimension
        dim = input("Enter dimension of board:")
        self.dimension = int(dim)
        ttt = pygame.display.set_mode ((self.dimension*100, self.dimension*100 + 25))
        self.state = np.full((self.dimension,self.dimension),BLANK)
        self.preFillData()
        pygame.display.set_caption ('Tic Tac Toe')
        board = self.initBoard (ttt)
        self.initStates(board, ticTacToeInstance.state)
        return ttt,board
        
if __name__ == "__main__":

    #global state

    # symbolNow = "X"

    counter = 0

    symbol_one = "X"
    symbol_two = "O"
    symbol_three = "+"

    ticTacToeInstance  = TicTacToe();
    
    ttt,board = ticTacToeInstance.setupGame(4)
#     pygame.init()
#     
#     dimensions = 5
#     
#     ttt = pygame.display.set_mode ((dimensions*100, dimensions*100 + 25))
#     pygame.display.set_caption ('Tic Tac Toe')
# 
#     
#     board = ticTacToeInstance.initBoard (ttt)
# 
#     ticTacToeInstance.initStates(board, ticTacToeInstance.state)
    gameTer = False
    while (ticTacToeInstance.running == 1):
        for event in pygame.event.get():
            if event.type is QUIT:
                ticTacToeInstance.running = 0
            elif event.type is MOUSEBUTTONDOWN:
                # the user clicked; place an X or O
                counter = counter+1

                if(counter % 3 == 1 and gameTer == False):
                    ticTacToeInstance.clickBoard(board, symbol_one)
                    gameTer = ticTacToeInstance.gameWon (board)
                elif(counter % 3 == 2 and gameTer == False):
                    ticTacToeInstance.clickBoard(board, symbol_two)
                    gameTer = ticTacToeInstance.gameWon (board)
                    if(gameTer == False):
                        ticTacToeInstance.performAIMove(board, symbol_three)
                        gameTer = ticTacToeInstance.gameWon (board)
                    
                # else:
                


                # if (symbolNow == "X"):
                #     clickBoard(board, symbol_one)
                # if (symbolNow == "O"):
                #     clickBoard(board, symbol_two)
                # if (symbolNow == "+"):
                #     performAIMove(board, symbol_three)

            # if (symbolNow == "X"):
            #     symbolNow = "O"
            # elif (symbolNow == "O"):
            #     symbolNow = "+"
            # else:
            #     symbolNow = "X"

            # check for a winner
            #gameWon (board)

            # update the display
            ticTacToeInstance.showBoard (ttt, board)

    

    # state = np.array([
    #     ["x", "o", "o"],
    #     ["x", BLANK, BLANK],
    #     [BLANK, BLANK, BLANK]]).T
    # symbol = "x"

    # state = np.array([
    #     ["o", "x", "x"],
    #     ["o", BLANK, BLANK],
    #     [BLANK, BLANK, BLANK]])
    # symbol = "x"

#     state = np.array([
#         ["x", BLANK, "o"],
#         ["x", BLANK, BLANK],
#         [BLANK, BLANK, BLANK]])
#     symbol = "o"

    # state = np.array([
    #     ["x", "o", "o"],
    #     ["x", BLANK, BLANK],
    #     ["x", BLANK, BLANK]])
    # symbol = "o"

#     state = np.array([
#         ["x", "o", "o"],
#         ["x", "x", "o"],
#         [BLANK, "x", BLANK]])
#     symbol = "x"

    # v, actions, n = mnx(state, symbol)
    # print(state)
    # print(actions)
    # print(v, n)

    # v_ab, actions_ab, n_ab = mnx_ab(state, symbol)
    # print(state)
    # print(actions_ab)
    # print(v_ab, n_ab)


