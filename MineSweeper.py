#!/bin/python3

# Load necessary Python libraries
import random

class MineSweeperBoard:

  def __init__(self, xDimension, yDimension, numberMines):
    """Initialization function

    Parameters
    ----------
    xDimension : int
      The number of rows the gameboard possesses
    yDimension : int
      The number of columns the gameboard possesses
    numberMines : int
      The number of mines that the board contains. The 
      number should be positive, but less than the total
      number tiles the board has
    """
    self.xDimension = xDimension
    self.yDimension = yDimension
    self.numberMines = numberMines

    # Store the coordinates of mines when they are created so
    # an O(n^2) iteration is not necessary
    self.mineCoordinates = []
    self.gameOver = False
    self.movesRemaining = (self.xDimension * self.yDimension) - self.numberMines
    if self.movesRemaining == 0:
      self.gameOver = True

    # Sanity check to make sure that there are not more mines
    # than actual tiles on the game board
    if ((self.numberMines > (self.xDimension * self.yDimension)) or self.numberMines < 0):
      raise ValueError('invalid number of mines entered')

    # Game state board consists of the following numbers:
    # -  -1 = Empty tile (only used when the board is first initialized)
    # -  -9 = Mine location
    # - 0-9 = Number of adjacent mines to a tile 
    self.gameStateBoard = [[-1 for x in range(self.yDimension)] for y in range(self.xDimension)]
    
    # Player gameboard view consists of the following symbols
    # -   @ = Unknown (not yet selected) tile
    # -   x = Mine location
    # -   - = 0 value (no adjacent mines)
    # - 1-9 = Number of adjacent mines
    self.playerViewBoard = [['@' for x in range(self.yDimension)] for y in range(self.xDimension)]

    # Seed the board with mines and then determine the correct values
    # to assign for the remaining nodes based on adjacency to mines
    self.__seedMines()
    self.__seedValues()

  def isGameOver(self):
    """Returns whether the game has been marked as over
    """
    return self.gameOver

  def __seedMines(self):
    """Seeds mines into an empty gameStateBoard

    This function should only be called by the initialization
    function. Its sole purpose is to randomly create the
    specified number of mines on the board. In the gameStateBoard,
    mines are denoted by the value: -9
    """
    minesRemaining = self.numberMines
    while minesRemaining > 0:
      x = random.randint(0, self.xDimension - 1)
      y = random.randint(0, self.yDimension - 1)
      if self.gameStateBoard[x][y] == -9:
        continue
      self.gameStateBoard[x][y] = -9
      self.mineCoordinates.append((x, y))
      minesRemaining -= 1

  def __seedValues(self):
    """Seeds values into tiles not containing mines in the gameStateBoard

    This function should only be called by the initialization 
    function. For all tiles on the gameStateBoard that do not
    contain a mine, this function determines the number of mines
    adjacent to all tiles on the gameStateBoard. These values
    can range from 0 to 8
    """
    for x, row in enumerate(self.gameStateBoard):
      for y, value in enumerate(row):
        # If the tile contains a mine, we are not interested in it
        # so go onto the next tile
        if value == -9:
          continue
        # Otherwise, calculate the number of adjacent mines, so that
        # value can then be assigned to the tile
        tileValue = self.__getNumAdjMines(x, y)
        self.gameStateBoard[x][y] = tileValue

  def print(self, gameboard=None):
    """Print the player gameboard

    This function prints the players representation of
    the minesweeper gameboard as a n x m matrix. By 
    default, the function will print the player's view 
    of the gameboard; however, if a 2D array is passed-in, 
    it will print that instead.

    Parameters
    ----------
    gameboard : array, optional
      The 2D array that should be printed if the user does
      not want to print the player's view.
    """
    board = self.playerViewBoard if (gameboard == None) else gameboard
    print('\n')
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in board]))
    print('\n')

  def printDebug(self):
    """Prints the game state board

    This function simply prints the game state board using the
    previously defined print() function and passing in the
    game state 2D array
    """
    self.print(self.gameStateBoard)

  def __hasMine(self, x, y):
    """Determines if a mine is present at the given location

    This function looks at the game state board and determines
    if the selectied location contains a mine.

    Parameters
    ----------
    x : int
      x coordinate corresponding to the location to look for a mine
    y : int
      y coordinate corresponding to the location to look for a mine
    """
    return True if self.gameStateBoard[x][y] == -9 else False

  def __revealMines(self):
    """Reveals all the mines on the player visible gameboard

    This function should only be called when the player selects a mine
    and the game is ready to end. It reveals all the mines on the player
    visible gameboard.
    """
    for coordinatePair in self.mineCoordinates:
      xCoordinate = coordinatePair[0]
      yCoordinate = coordinatePair[1]
      self.__revealTile(xCoordinate, yCoordinate)

  def __coordinateCheck(self, x, y):
    """Checks to make sure that the coordinate pair is within bounds of the board

    This is a helper function that checks to ensure that the input coordinates
    are within the dimensions of the board.

    Parameters
    ----------
    x : int
      x coordinate of the coordinate pair to check
    y : int
      y coordinate of the coordinate pair to check
    """
    if x < 0 or x >= self.xDimension:
      return False
    if y < 0 or y >= self.yDimension:
      return False
    return True
  
  def __getNumAdjMines(self, x, y):
    """Gets the number of mines adjacent to the tile located at coordinates

    This is a helper function used by the __seedValues() function to
    determine the number of mines adjacent to any given tile on the
    game state board. The return value is an integer denoting the 
    number of adjacent mines.

    Parameters
    ----------
    x : int
      x coordinate of the tile to search around
    y : int
      y coordinate of the tile to search around
    """
    totalNumMines = 0
    ## Check the tile to the west
    if (self.__coordinateCheck(x, y-1)):
      if self.__hasMine(x, y-1):
        totalNumMines += 1
    ## Check the tile to the north-west
    if (self.__coordinateCheck(x-1, y-1)):
      if self.__hasMine(x-1, y-1):
        totalNumMines += 1
    ## Check the tile to the north
    if (self.__coordinateCheck(x-1, y)):
      if self.__hasMine(x-1, y):
        totalNumMines += 1
    ## Check the tile to the north-east
    if (self.__coordinateCheck(x-1, y+1)):
      if self.__hasMine(x-1, y+1):
        totalNumMines += 1
    ## Check the tile to the east
    if (self.__coordinateCheck(x, y+1)):
      if self.__hasMine(x, y+1):
        totalNumMines += 1
    ## Check the tile to the south-east
    if (self.__coordinateCheck(x+1, y+1)):
      if self.__hasMine(x+1, y+1):
        totalNumMines += 1
    ## Check the tile to the south
    if (self.__coordinateCheck(x+1, y)):
      if self.__hasMine(x+1, y):
        totalNumMines += 1
    ## Check the tile to the south-west
    if (self.__coordinateCheck(x+1, y-1)):
      if self.__hasMine(x+1, y-1):
        totalNumMines += 1
    ## Return the total number of adjacent mines found
    return totalNumMines

  def __revealTile(self, x, y):
    """Reveals the tile specified by the input coordinates

    This is a helper function that reveals the tile found at
    coordinates (x, y) in the playerViewBoard.

    Parameters
    ----------
    x : int
      x coordinate of the coordinate pair to reveal
    y : int
      y coordinate of the coordinate pair to reveal
    """
    # If the gameStateBoard contains a mine at the input coordinates,
    # show a mine on the playerViewBoard
    if self.gameStateBoard[x][y] == -9:
      self.playerViewBoard[x][y] = 'x'
    elif self.gameStateBoard[x][y] == 0:
      self.playerViewBoard[x][y] = '-'
      self.movesRemaining -= 1
    else:
      self.playerViewBoard[x][y] = self.gameStateBoard[x][y]
      self.movesRemaining -= 1

  def __hasBeenPlayed(self, x, y):
    """Check the playerViewBoard to see if a tile has already been played

    Parameters
    ----------
    x : int
      x coordinate of the tile to check
    y : int
      y coordinate of the tile to check
    """
    return False if self.playerViewBoard[x][y] == '@' else True

  def __uncoverAdjTiles(self, x, y):
    """Uncovers tiles adjacent to the coordinates of the tile provided

    This function is used when the player selects a '0' tile on the
    game state board. Traditionally, minesweeper will reveal all
    adjacent tiles when a 0 tile is chosen. Furthermore, if any of the
    revealed tiles are 0 tiles themselves, then __uncoverAdjTiles() will
    be called on that tile.

    Parameters
    ----------
    x : int
      x coordinate of the tile that is the center of the tiles to be uncovered
    y : int
      y coordinate of the tile that is the center of the tiles to be uncovered
    """
    # Ensure that the input coordinates belong to a tile containing a
    # zero value (i.e. no adjacent mines)
    if self.gameStateBoard[x][y] == 0:
      ## Check the tile to the west
      if (self.__coordinateCheck(x, y-1)):
        if not self.__hasBeenPlayed(x, y-1):
          self.__revealTile(x, y-1)
          self.__uncoverAdjTiles(x, y-1)
      ## Check the tile to the north-west
      if (self.__coordinateCheck(x-1, y-1)):
        if not self.__hasBeenPlayed(x-1, y-1):
          self.__revealTile(x-1, y-1)
          self.__uncoverAdjTiles(x-1, y-1)
      ## Check the tile to the north
      if (self.__coordinateCheck(x-1, y)):
        if not self.__hasBeenPlayed(x-1, y):
          self.__revealTile(x-1, y)
          self.__uncoverAdjTiles(x-1, y)
      ## Check the tile to the north-east
      if (self.__coordinateCheck(x-1, y+1)):
        if not self.__hasBeenPlayed(x-1, y+1):
          self.__revealTile(x-1, y+1)
          self.__uncoverAdjTiles(x-1, y+1)
      ## Check the tile to the east
      if (self.__coordinateCheck(x, y+1)):
        if not self.__hasBeenPlayed(x, y+1):
          self.__revealTile(x, y+1)
          self.__uncoverAdjTiles(x, y+1)
      ## Check the tile to the south-east
      if (self.__coordinateCheck(x+1, y+1)):
        if not self.__hasBeenPlayed(x+1, y+1):
          self.__revealTile(x+1, y+1)
          self.__uncoverAdjTiles(x+1, y+1)
      ## Check the tile to the south
      if (self.__coordinateCheck(x+1, y)):
        if not self.__hasBeenPlayed(x+1, y):
          self.__revealTile(x+1, y)
          self.__uncoverAdjTiles(x+1, y)
      ## Check the tile to the south-west
      if (self.__coordinateCheck(x+1, y-1)):
        if not self.__hasBeenPlayed(x+1, y-1):
          self.__revealTile(x+1, y-1)
          self.__uncoverAdjTiles(x+1, y-1)

  def makeMove(self, x, y):
    """A public function called by the user when they have selected their tile.
    
    This is a public function that the player calls when they have selected a tile
    to uncover for their move. This function sanitizes the user input before
    making the corresponding changes to all three game boards.

    Parameters
    ----------
    x : int
      x coordinate of the tile selected
    y : int
      y coordinate of the tile selected
    """
    # Sanitize the user input coordinates
    if not self.__coordinateCheck(x, y):
      raise ValueError('invalid coordinate pair chosen')
    # Check if the move has already been made
    if self.__hasBeenPlayed(x, y):
      raise ValueError('move has already been played')
    # Check if the player has hit a mine
    if self.__hasMine(x, y):
      self.__revealMines()
      self.gameOver = True
      print('player has hit a mine!')
    # If a player selects a tile with a zero value
    # (i.e. no adjacent tiles contain a mine), uncover
    # all adjacent tiles
    elif self.gameStateBoard[x][y] == 0:
      self.__revealTile(x,y)
      self.__uncoverAdjTiles(x,y)
      # If there are no move valid moves the player can make
      # then the game is over; the player has won!
      if self.movesRemaining == 0:
        self.gameOver = True
        print('player has won!')
    # If the player selects a tile that contains a
    # non-negative, non-zero value - then just reveal
    # that single tile
    elif self.gameStateBoard[x][y] > 0:
      self.__revealTile(x,y)
      if self.movesRemaining == 0:
        self.gameOver = True
        print('player has won')

  def getPlayerBoard(self):
    """Returns the 2D playerViewBoard

    This function returns the 2D playerViewBoard array so that
    it can be passed to the AI player which will then make decisions
    on the next move to play.
    """
    return self.playerViewBoard

# Main application logic
if __name__ == "__main__":
    # Predefined dimensions for the gameboard (these values can be changed)
    CONST_GAMEBOARD_ROWS = 9
    CONST_GAMEBOARD_COLS = 9
    CONST_GAMEBOARD_MINES = 10
    # Create a new instance of the Minesweeper game board
    NewGameboard = MineSweeperBoard(CONST_GAMEBOARD_ROWS, CONST_GAMEBOARD_COLS, CONST_GAMEBOARD_MINES)
    NewGameboard.print()
    NewGameboard.printDebug()
    # While the game is not over, the player should keep
    # being prompted for their next move
    while not NewGameboard.isGameOver():
      xCoordinate = int(input('Please enter the x component of the tile: '))
      yCoordinate = int(input('Please enter the y component of the tile: '))
      try:
        NewGameboard.makeMove(xCoordinate, yCoordinate)
        NewGameboard.print()
        NewGameboard.printDebug()
      except ValueError as error:
        print(error)
        print('invalid move selected, please select another tile')
        continue
    # When the game has ended, then print a game over message
    # and exit the application
    print('GAME OVER!')
    exit(0)
