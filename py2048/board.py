"""Define the class representing the game 2048"""

import numpy as np

GRID_SIZE = (5,5)
PROB_2 = 0.9

class Board:
    """Represents the board of the game 2048

    The grid is of variable size, and uses 1s to represent blank spaces.
    Knows how to move, add random tiles, and evaluate various heuristics.
    Needs to be initializes.

    Parameters
    ----------
    grid_size : 2-tuple
        Dimensions of the grid for this board
    prob_2 : numeric in [0,1]
        The probability of generating a 2 when a random tile is added

    Attributes
    ----------
    grid : ndarray
        array representing the current state of the game
    prob_2 : numeric in [0,2]
        Initialized probability of generating a 2
    """
    def __init__(self, grid_size=GRID_SIZE, prob_2=PROB_2):
        """ones represent empty spaces"""
        self.grid = np.ones(grid_size)

    def move(self, d):
        """Moves the tiles in the direction specified

        Does not check the legitimacy of move for speed purposes

        Parameters
        ----------
        d : str
            The direction to move the tiles on the grid in ["left", "right", "up", "down"]
        """

        for i in range(self.grid.shape[0]):
            first_empty = 0
            compressed = True
            for j in range(self.grid.shape[1]):
                if self.grid[i, j] != 1:
                    if (not compressed and
                        self.grid[i, first_empty - 1] == self.grid[i, j]):

                        self.grid[i, first_empty - 1] *= 2
                        self.grid[i, j] = 1
                        compressed = True
                    elif j != first_empty:
                        self.grid[i, first_empty] = self.grid[i, j]
                        self.grid[i, j] = 1
                        first_empty += 1
                        compressed = False
                    else:
                        first_empty += 1
                        compressed = False
