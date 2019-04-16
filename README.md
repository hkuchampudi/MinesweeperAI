# MineSweeper AI

## Introduction
This repository hosts the final project for CIS 4930: Introduction to AI for the Spring 2019 semester. Our project was to build an AI agent that plays Minesweeper using Python3.

## Running the Code
To run the code, the user just has to enter the command `python3 MineSweeper.py` in this root directory of the program.

## Changing the Board Difficulty
Minesweeper has 3 levels of difficulty: beginner, intermediate, and expert. By default the board is configured to be a beginner board (9 rows, 9 columns, 10 mines); however, the user can change the board difficulty by editing lines 22-24 of `MineSweeper.py`. For example, if the user wanted the AI to play on an intermediate board, they would modify lines 22-24 as follows:
```python3
CONST_GAMEBOARD_ROWS = CONST_GAMEBOARD_ROWS_INTERMEDIATE
CONST_GAMEBOARD_COLS = CONST_GAMEBOARD_COLS_INTERMEDIATE
CONST_GAMEBOARD_MINES = CONST_GAMEBOARD_MINES_INTERMEDIATE
```

## Notes

### NP-Completeness and Degenerative Cases
Minesweeper is a [provable NP-complete problem](http://simon.bailey.at/random/kaye.minesweeper.pdf). Therefore, there are some board configurations where our algorithm is degenerative and will hang the computer while it tries to solve the constraint satisfaction problem (CSP); this is especially prevalent on more complex boards like the EXPERT board. If the algorithm stalls for more than 50 seconds, it is probably better to exit the program using `[CTRL-C]` and try running the program again with a different board configuration.

## Resources
Gustavo Niemeyer's Constraint Satisfaction Solver for Python: https://github.com/python-constraint/python-constraint