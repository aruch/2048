"""Define the class representing the game 2048"""

import numpy as np

GRID_SIZE = (4,4)
PROB_2 = 0.9

def pos(i, j, flip=False):
    """accessory function to access by column and row instead of row and column"""
    if flip:
        return (j, i)
    else:
        return (i, j)
        
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
        """Initialize board by creating an array of shape grid_size.

        grid_size is assumed to be the same in both dimensions"""
        self.grid = np.ones(grid_size)
        self.prob_2 = prob_2

        
    def move(self, d):
        """Moves the tiles in the direction specified

        Does not check the legitimacy of move for speed purposes

        Parameters
        ----------
        d : str
            The direction to move the tiles on the grid in ["left", "right", "up", "down"]
        """

        if d == "left" :
            start = 0
            stop = self.grid.shape[0]
            inc = 1
            flip = False
        elif d == "right" :
            start = self.grid.shape[0] -1
            stop = -1
            inc = -1
            flip = False
        elif d == "up":
            start = 0
            stop = self.grid.shape[0]
            inc = 1
            flip = True
        elif d == "down":
            start = self.grid.shape[0] -1
            stop = -1
            inc = -1
            flip = True

        for i in range(self.grid.shape[0]):
            first_empty = start
            compressed = True
            # traverse the row/column in the opposite direction of the move
            # move tiles to the first empty space seen, or if the last move didn't
            # result in a merge of two tiles check if the first non-empty space contains
            # a tile with the same value as the one being moved.  If that is the case
            # combine the two tiles together into one.
            #
            # When moving "up" or "down" flip the indices so that access is done (column, row)
            # instead of (row, column)
            for j in range(start, stop, inc):
                if self.grid[pos(i, j, flip)] != 1:
                    if (not compressed and
                        self.grid[pos(i, first_empty - inc, flip)] ==
                        self.grid[pos(i, j, flip)]):

                        self.grid[pos(i, first_empty - inc, flip)] *= 2
                        self.grid[pos(i, j, flip)] = 1
                        compressed = True
                    elif j != first_empty:
                        self.grid[pos(i, first_empty, flip)] = self.grid[pos(i, j, flip)]
                        self.grid[pos(i, j, flip)] = 1
                        first_empty += inc
                        compressed = False
                    else:
                        first_empty += inc
                        compressed = False

    def n_empty_tiles(self):
        """Calculates the number of empty tiles currently on the board"""

        return np.sum(self.grid == 1)

    def empty_tiles(self):
        """Returns a list of tuples of the positions of the empty tiles"""

        return list(zip(*np.where(self.grid == 1)))
