#!/bin/python3

# Load necessary Python libraries
from MineSweeperBoard import MineSweeperBoard
from MineSweeperPlayer import MineSweeperPlayer

CONST_GAMEBOARD_ROWS_BEGINNER = 9
CONST_GAMEBOARD_COLS_BEGINNER = 9
CONST_GAMEBOARD_MINES_BEGINNER = 10

CONST_GAMEBOARD_ROWS_INTERMEDIATE = 16
CONST_GAMEBOARD_COLS_INTERMEDIATE = 16
CONST_GAMEBOARD_MINES_INTERMEDIATE = 40

CONST_GAMEBOARD_ROWS_EXPERT = 16
CONST_GAMEBOARD_COLS_EXPERT = 30
CONST_GAMEBOARD_MINES_EXPERT = 99

# Main application logic
if __name__ == "__main__":
    # Predefined dimensions for the gameboard (these values can be changed)
    CONST_GAMEBOARD_ROWS = CONST_GAMEBOARD_ROWS_BEGINNER
    CONST_GAMEBOARD_COLS = CONST_GAMEBOARD_COLS_BEGINNER
    CONST_GAMEBOARD_MINES = CONST_GAMEBOARD_MINES_BEGINNER
    # Create a new instance of the Minesweeper game board
    NewAIPlayer = MineSweeperPlayer(CONST_GAMEBOARD_ROWS, CONST_GAMEBOARD_COLS, CONST_GAMEBOARD_MINES)
    NewGameboard = MineSweeperBoard(CONST_GAMEBOARD_ROWS, CONST_GAMEBOARD_COLS, CONST_GAMEBOARD_MINES)
    NewGameboard.print()
    # NewGameboard.printDebug()
    # While the game is not over, the player should keep
    # being prompted for their next move
    while not NewGameboard.isGameOver():
      NewAIPlayer.updatePlayerViewBoard(NewGameboard.getPlayerBoard())
      xCoordinate, yCoordinate = NewAIPlayer.makeMove()
      print('player chose move: {},{}'.format(xCoordinate, yCoordinate))
      #xCoordinate = int(input('Please enter the x component of the tile: '))
      #yCoordinate = int(input('Please enter the y component of the tile: '))
      try:
        NewGameboard.makeMove(xCoordinate, yCoordinate)
        NewGameboard.print()
        # NewGameboard.printDebug()
      except ValueError as error:
        print(error)
        print('invalid move selected, please select another tile')
        continue
    # When the game has ended, then print a game over message
    # and exit the application
    print('GAME OVER!')
    exit(0)
