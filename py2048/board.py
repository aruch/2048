"""Define the class representing the game 2048"""

import numpy as np
import copy

GRID_SIZE = (4,4)
PROB_2 = 0.9
DIRS = ["left", "right", "up", "down"]

def pos(i, j, flip=False):
    """Accessory function to access by column and row instead of row and column"""
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
    game_over : bool
        Represents whether the game is over
    score : int
        Current score of the game
    """
    def __init__(self, grid_size=GRID_SIZE, prob_2=PROB_2):
        """Initialize board by creating an array of shape grid_size.

        grid_size is assumed to be the same in both dimensions"""
        self.grid = np.ones(grid_size)
        self.prob_2 = prob_2
        self.game_over = False
        self.score = 0

        self.add_random_tile()
        self.add_random_tile()

    def move(self, d, check_only=False):
        """Moves the tiles in the direction specified, or checks if a
        move could be made in that direction.

        Does not check the legitimacy of move for speed purposes.
        Increments the score when two tiles are merged.

        Parameters
        ----------
        d : str
            The direction to move the tiles on the grid
            should be in ["left", "right", "up", "down"]
        check_only : bool
            Method returns True if a move could be made in the direction d
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
            # move tiles to the first empty space seen, or if the last move
            # didn't result in a merge of two tiles check if the first
            # non-empty space contains a tile with the same value as the one
            # being moved.  If that is the case combine the two tiles together
            # into one.
            #
            # When moving "up" or "down" flip the indices so that access is
            # done (column, row) instead of (row, column)
            for j in range(start, stop, inc):
                if self.grid[pos(i, j, flip)] != 1:
                    if (not compressed and
                        self.grid[pos(i, first_empty - inc, flip)] ==
                        self.grid[pos(i, j, flip)]):

                        if check_only:
                            return True
                        self.grid[pos(i, first_empty - inc, flip)] *= 2
                        self.score += self.grid[pos(i, first_empty - inc, flip)]
                        self.grid[pos(i, j, flip)] = 1
                        compressed = True
                    elif j != first_empty:
                        if check_only:
                            return True
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

    def add_random_tile(self):
        """Adds a tile to a random empty spot on the grid.  The value
        of the tile is randomly determined."""
        tile_value = 2 if np.random.random() < self.prob_2 else 4

        empty_tiles = self.empty_tiles()
        self.grid[empty_tiles[np.random.choice(len(empty_tiles))]] = tile_value

    def possible_moves(self):
        """Returns a list of the possible move directions"""
        moves = []
        for d in DIRS:
            if self.move(d, check_only=True):
                moves.append(d)

        return moves

    def check_game_over(self):
        return self.n_empty_tiles() == 0 and self.possible_moves() == []

    def turn(self, d):
        """Taking a turn in the game consists of making a move followed by
        adding a tile to the board.

        Assumes game is not over to start and
        checks if the game is over at the end."""
        self.move(d)
        self.add_random_tile()
        self.game_over = self.check_game_over()

    def n_merges_available(self):
        """Count the number of tiles that can be merged

        Returns : int"""
        saved_grid = self.grid.copy()
        saved_score = self.score
        init_empty = self.n_empty_tiles()
        self.move("left")
        horizontal_merges = self.n_empty_tiles() - init_empty 
        self.grid = saved_grid.copy()
        self.move("up")
        vertical_merges = self.n_empty_tiles() - init_empty 
        self.grid = saved_grid.copy()

        return horizontal_merges + vertical_merges

    def smoothness(self):
        """Smoothness is a measure of how similar adjacent tiles are

        Calculates the log difference of adjacent tiles.  Adjacent doesn't
        necessarily mean within one space. Totals the horizontal and
        vertical directions.

        Returns : float
        """

        smoothness = 0

        log_grid = np.log(self.grid)

        for i in range(self.grid.shape[0]):
            previous_tile = 0
            for j in range(self.grid.shape[1]):
                if log_grid[i, j] != 0:
                    if previous_tile != 0:
                        smoothness += np.abs(previous_tile - log_grid[i, j])
                    previous_tile = log_grid[i, j]

        for i in range(self.grid.shape[1]):
            previous_tile = 0
            for j in range(self.grid.shape[0]):
                if log_grid[j, i] != 0:
                    if previous_tile != 0:
                        smoothness += np.abs(previous_tile - log_grid[j, i])
                    previous_tile = log_grid[j, i]

        return smoothness

    def n_out_of_order(self):
        """Measure of the monotonicity of the board

        Sums the swaps necessary to put the board in order.
        Runs a vertical and horizontal pass picking the minimum
        (out of either left and right or up and down) for each.

        Returns : int
        """
        l_out_of_order = 0
        r_out_of_order = 0
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]-1):
                cur_val = self.grid[i, j]
                if cur_val != 1:
                    cur_slice = self.grid[i, (j+1):]
                    l_out_of_order += np.sum((cur_slice > cur_val) &
                                             (cur_slice != 1))
                    r_out_of_order += np.sum((cur_slice < cur_val) &
                                             (cur_slice != 1))

        h_out_of_order = min(l_out_of_order, r_out_of_order)

        u_out_of_order = 0
        d_out_of_order = 0
        for i in range(self.grid.shape[1]):
            for j in range(self.grid.shape[0]-1):
                cur_val = self.grid[j, i]
                if cur_val != 1:
                    cur_slice = self.grid[(j+1):, i]
                    u_out_of_order += np.sum((cur_slice > cur_val) &
                                             (cur_slice != 1))
                    d_out_of_order += np.sum((cur_slice < cur_val) &
                                             (cur_slice != 1))
        v_out_of_order = min(u_out_of_order, d_out_of_order)

        return h_out_of_order + v_out_of_order
