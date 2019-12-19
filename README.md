# Tic Tac Toe - AI Version

>   We all know the regular Tic Tac Toe. How much of an effort would it be to make an AI learn the game?? How would complexity increase if we make it an 3 player game??
  
>   This project is an attempt to explore and answer the questions above.
  
>   The attempt includes building the game for 3 players including 1 AI component as a player. Each player will take turns and fill the board trying to make a straight line. Obviously, in order to facilitate 3 players, the board also needs to be bigger and hence, we are starting with a board size of 4x4. Any player who can successfully complete 1 straight line of their symbols vertically, horizontally or diagonally, wins the game. If nobody is able to get 1 straight line, then it is a draw.

>   The AI agent in itself will use the min-max tree algorithm to make decisions for a move. The min-max tree algorithm is based on the principle that a player will always try to maximize his score at any given state of system/game while minimizing other player's scores. The underlying principal for this to work is with the assumpution and prespective that we always see from only 1 player's perspective where the player always choses the maximizing score from the options he has from the branches and the other player always selects the lowest score from its brances. The min-max tree is iteratively calculated at each new state since the game is played from a top-down perspective and the AI agent would have to calculate every possible moves each time. This obviously is computationally intensive but nevertheless very effective. 

>   There is a neural network machine learning involved as well. How, you may ask? Well, we have to make the AI agent learn making the right decision every single time. 


## Dependency

- pygame
- numpy
- matplotlib
- torch

Please keep ```tic-tac-toe-4.csv``` in the root directory. Its a data set for training the model.

## How to Run

1. First, Install the python modules which are specified above.
2. Run ```python tictactree.py```
3. It will ask for ```Do you want to play with the trained model or do you want to simulate a new model ?```. If you want to play the actual game of 3 player Tic Tac Toe, then enter ```P``` or if you want to simulate a new model for Tic Tac Toe Game for 100 game iterations then enter ```S```. Graph will be shown in simulation mood for the learning curve
4. Then it will ask for ```Do you want to use the trained model or new model ?```. If you want to use the already trained model then enter ```T``` or to use new model, enter ```N```.
