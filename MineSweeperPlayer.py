# Load necessary Python modules
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
    # - 1-8 = Number of adjacent mines
    self.playerBoard = None
    self.moveQueue = []

  def print(self, gameboard=None):
    """
    """
    board = self.playerBoard if (gameboard == None) else gameboard
    print('\nPLAYER MIND MAP')
    if self.playerBoard == None:
      print('player has not yet seen the board!')
    else:
      print('\n'.join([' '.join([str(cell) for cell in row]) for row in board]))
    print('\n')

  def updatePlayerViewBoard(self, playerBoard):
    """
    """
    if self.playerBoard == None:
      self.playerBoard = [row[:] for row in playerBoard]
    else:
      for x, row in enumerate(playerBoard):
        for y, value in enumerate(row):
          if self.playerBoard[x][y] != '*':
            self.playerBoard[x][y] = playerBoard[x][y]

  def __coordinateCheck(self, x, y):
    """
    """
    if x < 0 or x >= self.xDimension:
      return False
    if y < 0 or y >= self.yDimension:
      return False
    return True
  
  def __chooseRandomMove(self):
    """
    """
    randXCoordinate = randint(0, self.xDimension - 1)
    randYCoordinate = randint(0, self.yDimension - 1)
    if self.playerBoard[randXCoordinate][randYCoordinate] == '@':
      self.moveQueue.append((randXCoordinate, randYCoordinate))
      return True
    else:
      return self.__chooseRandomMove()

  def __twoDegreeIsland(self, x, y):
    numAdjMines, _ = self.__getNumberAdj(x, y, '*')
    numAdjUnknown, _ = self.__getNumberAdj(x, y, '@')
    numAdj0, _ = self.__getNumberAdj(x, y, '-')
    numAdj1, _ = self.__getNumberAdj(x, y, 1)
    numAdj2, _ = self.__getNumberAdj(x, y, 2)
    numAdj3, _ = self.__getNumberAdj(x, y, 3)
    numAdj4, _ = self.__getNumberAdj(x, y, 4)
    numAdj5, _ = self.__getNumberAdj(x, y, 5)
    numAdj6, _ = self.__getNumberAdj(x, y, 6)
    numAdj7, _ = self.__getNumberAdj(x, y, 7)
    numAdj8, _ = self.__getNumberAdj(x, y, 8)
    if (float(numAdjUnknown) / (numAdj0 + numAdj1 + numAdj2 + numAdj3 + numAdj4 + numAdj5 + numAdj6 + numAdj7 + numAdj8 + numAdjMines + numAdjUnknown) == 1):
      numAdjMines2, _ = self.__getNumberAdj(x, y, '*', 2)
      numAdjUnknown2, _ = self.__getNumberAdj(x, y, '@', 2)
      numAdj02, _ = self.__getNumberAdj(x, y, '-', 2)
      numAdj12, _ = self.__getNumberAdj(x, y, 1, 2)
      numAdj22, _ = self.__getNumberAdj(x, y, 2, 2)
      numAdj32, _ = self.__getNumberAdj(x, y, 3, 2)
      numAdj42, _ = self.__getNumberAdj(x, y, 4, 2)
      numAdj52, _ = self.__getNumberAdj(x, y, 5, 2)
      numAdj62, _ = self.__getNumberAdj(x, y, 6, 2)
      numAdj72, _ = self.__getNumberAdj(x, y, 7, 2)
      numAdj82, _ = self.__getNumberAdj(x, y, 8, 2)
      return (float(numAdjUnknown2) / (numAdj02 + numAdj12 + numAdj22 + numAdj32 + numAdj42 + numAdj52 + numAdj62 + numAdj72 + numAdj82 + numAdjMines2 + numAdjUnknown2) == 1)
    else:
      return False

  def __formulateConstraintEq(self, x, y):
    """
    """
    if self.playerBoard[x][y] == '@' or self.playerBoard[x][y] == '-' or self.playerBoard[x][y] == '*':
      return None
    tileValue = self.playerBoard[x][y]
    variablesList = []
    mOccurrences, mCoordinates = self.__getNumberAdj(x, y, '*')
    fOccurrences, fCoordinates = self.__getNumberAdj(x, y, '@')
    if fOccurrences == 0:
      return None
    if self.__twoDegreeIsland(x, y):
      return None
    tileValue -= mOccurrences
    for fCoordinate in fCoordinates:
      variablesList.append(','.join(map(str, fCoordinate)))
    return ( (x,y), tileValue, variablesList )

  def __getAllConstraints(self):
    """
    """
    constraintList = []
    for x, row in enumerate(self.playerBoard):
      for y, value in enumerate(row):
        constraintEq = self.__formulateConstraintEq(x, y)
        if constraintEq != None:
          constraintList.append(constraintEq)
    return constraintList

  def __getNumberAdj(self, x, y, character, degree=1):
    """
    """
    totalOccurrences = 0
    occurrenceCoordinates = []
    if (self.__coordinateCheck(x, y-degree)):
      if self.playerBoard[x][y-degree] == character:
        totalOccurrences += 1
        occurrenceCoordinates.append( (x,y-degree) )
    ## Check the tile to the north-west
    if (self.__coordinateCheck(x-degree, y-degree)):
      if self.playerBoard[x-degree][y-degree] == character:
        totalOccurrences += 1
        occurrenceCoordinates.append( (x-degree,y-degree) )
    ## Check the tile to the north
    if (self.__coordinateCheck(x-degree, y)):
      if self.playerBoard[x-degree][y] == character:
        totalOccurrences += 1
        occurrenceCoordinates.append( (x-degree,y) )
    ## Check the tile to the north-east
    if (self.__coordinateCheck(x-degree, y+degree)):
      if self.playerBoard[x-degree][y+degree] == character:
        totalOccurrences += 1
        occurrenceCoordinates.append( (x-degree,y+degree) )
    ## Check the tile to the east
    if (self.__coordinateCheck(x, y+degree)):
      if self.playerBoard[x][y+degree] == character:
        totalOccurrences += 1
        occurrenceCoordinates.append( (x,y+degree) )
    ## Check the tile to the south-east
    if (self.__coordinateCheck(x+degree, y+degree)):
      if self.playerBoard[x+degree][y+degree] == character:
        totalOccurrences += 1
        occurrenceCoordinates.append( (x+degree,y+degree) )
    ## Check the tile to the south
    if (self.__coordinateCheck(x+degree, y)):
      if self.playerBoard[x+degree][y] == character:
        totalOccurrences += 1
        occurrenceCoordinates.append( (x+degree,y) )
    ## Check the tile to the south-west
    if (self.__coordinateCheck(x+degree, y-degree)):
      if self.playerBoard[x+degree][y-degree] == character:
        totalOccurrences += 1
        occurrenceCoordinates.append( (x+degree,y-degree) )
    return totalOccurrences, occurrenceCoordinates

  def __firstDegreeSolver(self):
    wasUsed = False
    for x, row in enumerate(self.playerBoard):
      for y, value in enumerate(row):
        if value != '@' and value != '-' and value != '*':
          mOccurrences, mCoordinates = self.__getNumberAdj(x, y, '*')
          fOccurrences, fCoordinates = self.__getNumberAdj(x, y, '@')
          if value - mOccurrences == 0:
            # Rest must be OK spaces
            for fCoordinate in fCoordinates:
              self.moveQueue.append(fCoordinate)
              wasUsed = True
          elif value - mOccurrences == fOccurrences:
            # Rest must be mines
            for fCoordinate in fCoordinates:
              fCX = fCoordinate[0]
              fCY = fCoordinate[1]
              self.playerBoard[fCX][fCY] = '*'
              wasUsed = True
    return wasUsed

  def __secondDegreeSolver(self):
    """
    """
    wasUsed = False
    constraintProblem = Problem()
    constraintsList = self.__getAllConstraints()
    for x in range(0,len(constraintsList) - 1):
      for y in range(x+1, len(constraintsList)):
        constraintProblem.reset()
        constraint1 = constraintsList[x]
        constraint2 = constraintsList[y]
        uniqueVariables = list(set(constraint1[2] + constraint2[2]))
        constraintProblem.addVariables(uniqueVariables, [0,1])
        constraintProblem.addConstraint(ExactSumConstraint(constraint1[1]), constraint1[2])
        constraintProblem.addConstraint(ExactSumConstraint(constraint2[1]), constraint2[2])
        solutions = constraintProblem.getSolutions()
        if len(solutions) != 0:
          for variable in uniqueVariables:
            firstVal = solutions[0][variable]
            isConsistent = True
            for solution in solutions:
              if solution[variable] != firstVal:
                isConsistent = False
                break
            if isConsistent:
              decodedX = int(variable.split(',')[0])
              decodedY = int(variable.split(',')[1])
              if firstVal == 0:
                self.moveQueue.append((decodedX, decodedY))
                wasUsed = True
              if firstVal == 1:
                self.playerBoard[decodedX][decodedY] = '*'
                wasUsed = True
    return wasUsed

  def __thirdDegreeSolver(self):
    """
    """
    wasUsed = False
    constraintProblem = Problem()
    constraintsList = self.__getAllConstraints()
    for x in range(0,len(constraintsList) - 2):
      for y in range(x+1, len(constraintsList) - 1):
        for z in range(x+2, len(constraintsList)):
          constraintProblem.reset()
          constraint1 = constraintsList[x]
          constraint2 = constraintsList[y]
          constraint3 = constraintsList[z]
          uniqueVariables = list(set(constraint1[2] + constraint2[2] + constraint3[2]))
          constraintProblem.addVariables(uniqueVariables, [0,1])
          constraintProblem.addConstraint(ExactSumConstraint(constraint1[1]), constraint1[2])
          constraintProblem.addConstraint(ExactSumConstraint(constraint2[1]), constraint2[2])
          constraintProblem.addConstraint(ExactSumConstraint(constraint3[1]), constraint3[2])
          solutions = constraintProblem.getSolutions()
          if len(solutions) != 0:
            for variable in uniqueVariables:
              firstVal = solutions[0][variable]
              isConsistent = True
              for solution in solutions:
                if solution[variable] != firstVal:
                  isConsistent = False
                  break
              if isConsistent:
                decodedX = int(variable.split(',')[0])
                decodedY = int(variable.split(',')[1])
                if firstVal == 0:
                  self.moveQueue.append((decodedX, decodedY))
                  wasUsed = True
                if firstVal == 1:
                  self.playerBoard[decodedX][decodedY] = '*'
                  wasUsed = True
    return wasUsed
  
  def __globalSolver(self):
    """
    """
    wasUsed = False
    constraintProblem = Problem()
    constraintsList = self.__getAllConstraints()
    uniqueVariables = []
    for constraint in constraintsList:
      uniqueVariables = uniqueVariables + constraint[2]
      constraintProblem.addConstraint(ExactSumConstraint(constraint[1]), constraint[2])
    uniqueVariables = list(set(uniqueVariables))
    constraintProblem.addVariables(uniqueVariables, [0,1])
    solutions = constraintProblem.getSolutions()
    if len(solutions) != 0:
      for variable in uniqueVariables:
        firstVal = solutions[0][variable]
        isConsistent = True
        for solution in solutions:
          if solution[variable] != firstVal:
            isConsistent = False
            break
        if isConsistent:
          decodedX = int(variable.split(',')[0])
          decodedY = int(variable.split(',')[1])
          if firstVal == 0:
            self.moveQueue.append((decodedX, decodedY))
            wasUsed = True
          if firstVal == 1:
            self.playerBoard[decodedX][decodedY] = '*'
            wasUsed = True
    return wasUsed

  def makeMove(self):
    """
    """
    if len(self.moveQueue) != 0:
      nextMove = self.moveQueue.pop()
      if self.playerBoard[nextMove[0]][nextMove[1]] != '@':
        return self.makeMove()
      self.print()
      return nextMove[0], nextMove[1]
    else:
      firstResults = self.__firstDegreeSolver()
      if firstResults:
        return self.makeMove()
      secondResults = self.__secondDegreeSolver()
      if secondResults:
        return self.makeMove()
      thirdResults = self.__thirdDegreeSolver()
      if thirdResults:
        return self.makeMove()
      globalResults = self.__globalSolver()
      if globalResults:
        return self.makeMove()
      randomResults = self.__chooseRandomMove()
      if randomResults:
        print('Not sure what to do... choosing random')
        return self.makeMove()

  