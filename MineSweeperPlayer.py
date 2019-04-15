# Load necessary Python modules
from queue import Queue
from random import randint
from constraint import *

class MineSweeperPlayer:

  def __init__(self, xDimension, yDimension, numberMines):
    """
    """
    self.xDimension = xDimension
    self.yDimension = yDimension
    self.numberMines = numberMines

    # Player gameboard view consists of the following symbols
    # -   @ = Unknown (not yet selected) tile
    # -   * = Mine location
    # -   - = 0 value (no adjacent mines)
    # - 1-9 = Number of adjacent mines
    self.playerViewBoard = [['@' for x in range(self.yDimension)] for y in range(self.xDimension)]
    self.moveQueue = []
  
  def updatePlayerViewBoard(self, playerViewBoard):
    """
    """
    for x, row in enumerate(playerViewBoard):
      for y, value in enumerate(row):
        if self.playerViewBoard[x][y] != '*':
          self.playerViewBoard[x][y] = playerViewBoard[x][y]

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

  def __formulateConstraint(self, x, y):
    tileValue = self.playerViewBoard[x][y]
    variablesList = []
    containsUncoveredTile = False

    if (self.__coordinateCheck(x, y-1)):
      if self.playerViewBoard[x][y-1] == '*':
        tileValue -= 1
      if self.playerViewBoard[x][y-1] == '@':
        containsUncoveredTile = True
        variablesList.append(','.join([str(x),str(y-1)]))
      
    ## Check the tile to the north-west
    if (self.__coordinateCheck(x-1, y-1)):
      if self.playerViewBoard[x-1][y-1] == '*':
        tileValue -= 1
      if self.playerViewBoard[x-1][y-1] == '@':
        containsUncoveredTile = True
        variablesList.append(','.join([str(x-1),str(y-1)]))

    ## Check the tile to the north
    if (self.__coordinateCheck(x-1, y)):
      if self.playerViewBoard[x-1][y] == '*':
        tileValue -= 1
      if self.playerViewBoard[x-1][y] == '@':
        containsUncoveredTile = True
        variablesList.append(','.join([str(x-1),str(y)]))

    ## Check the tile to the north-east
    if (self.__coordinateCheck(x-1, y+1)):
      if self.playerViewBoard[x-1][y+1] == '*':
        tileValue -= 1
      if self.playerViewBoard[x-1][y+1] == '@':
        containsUncoveredTile = True
        variablesList.append(','.join([str(x-1),str(y+1)]))

    ## Check the tile to the east
    if (self.__coordinateCheck(x, y+1)):
      if self.playerViewBoard[x][y+1] == '*':
        tileValue -= 1
      if self.playerViewBoard[x][y+1] == '@':
        containsUncoveredTile = True
        variablesList.append(','.join([str(x),str(y+1)]))

    ## Check the tile to the south-east
    if (self.__coordinateCheck(x+1, y+1)):
      if self.playerViewBoard[x+1][y+1] == '*':
        tileValue -= 1
      if self.playerViewBoard[x+1][y+1] == '@':
        containsUncoveredTile = True
        variablesList.append(','.join([str(x+1),str(y+1)]))

    ## Check the tile to the south
    if (self.__coordinateCheck(x+1, y)):
      if self.playerViewBoard[x+1][y] == '*':
        tileValue -= 1
      if self.playerViewBoard[x+1][y] == '@':
        containsUncoveredTile = True
        variablesList.append(','.join([str(x+1),str(y)]))

    ## Check the tile to the south-west
    if (self.__coordinateCheck(x+1, y-1)):
      if self.playerViewBoard[x+1][y-1] == '*':
        tileValue -= 1
      if self.playerViewBoard[x+1][y-1] == '@':
        containsUncoveredTile = True
        variablesList.append(','.join([str(x+1),str(y-1)]))

    if not containsUncoveredTile:
      return None
    
    return ((x,y), tileValue, variablesList)

  def __getConstraints(self):
    """
    """
    constraintList = []
    for x, row in enumerate(self.playerViewBoard):
      for y, value in enumerate(row):
        if value != '@' and value != '*' and value != '-':
          constraint = self.__formulateConstraint(x, y)
          if constraint:
            constraintList.append(constraint)
    return constraintList
  
  def __performCSP(self):
    # Get list of board constraints
    constraintList = self.__getConstraints()
    uniqueVariables = {}
    uniqueVariablesList = None
    # Create a new satisfaction problem
    sProblem = Problem()
    # Add constraints to the problem
    for constraint in constraintList:
      tileValue = constraint[1]
      variableList = constraint[2]
      for variable in variableList:
        if variable not in uniqueVariables:
          uniqueVariables[variable] = True
      sProblem.addConstraint(ExactSumConstraint(tileValue), variableList)
    # Add the list of unique variables to the problem
    uniqueVariablesList = list(uniqueVariables)
    sProblem.addVariables(uniqueVariablesList, [0,1])
    solutions = sProblem.getSolutions()
    if len(solutions) != 0:
      for variable in uniqueVariablesList:
        decodedVariable = [int(x) for x in variable.split(',')]
        variableVal = solutions[0][variable]
        isConsistent = True
        for solution in solutions:
          if variableVal != solution[variable]:
            isConsistent = False
            break
        if isConsistent:
          if variableVal == 0:
            self.moveQueue.append(decodedVariable)
          if variableVal == 1:
            self.playerViewBoard[decodedVariable[0]][decodedVariable[1]] = '*'

  def __chooseRandomMove(self):
    randXCoordinate = randint(0, self.xDimension - 1)
    randYCoordinate = randint(0, self.yDimension - 1)
    if self.playerViewBoard[randXCoordinate][randYCoordinate] == '@':
      return randXCoordinate, randYCoordinate
    else:
      return self.__chooseRandomMove()
  
  def makeMove(self):
    if len(self.moveQueue) != 0:
      nextMove = self.moveQueue.pop()
      # Make sure that the move has not already been played.
      # If it has been, discard it and choose another move
      if self.playerViewBoard[nextMove[0]][nextMove[1]] != '@':
        return self.makeMove()
      return nextMove[0], nextMove[1]
    else:
      self.__performCSP()
      if len(self.moveQueue) != 0:
        nextMove = self.moveQueue.pop()
        return nextMove[0], nextMove[1]
      else:
        print('AI: Fuck! I do not know what to do next')
        print('AI: Choosing a random move...')
        # Choose a random move
        return self.__chooseRandomMove()