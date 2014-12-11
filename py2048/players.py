""" Defines a number of AI players for 2048"""

from py2048.board import Board
import copy
import numpy as np

class Player:
    """ A parent class for the other AI players.

    The general use for each subclass should be the same with only
    the initiation of the class differing.

    Example Usage:
    >>> p = Player()
    >>> p.play(verbose=True)
    """

    def __init__(self):
        self.b = Board()

    def reset_board(self):
        self.b = Board()

    def next_move(self):
        return self.b.possible_moves()[0]

    def play(self, verbose = False):
        i = 0
        while(not self.b.game_over):
            move_d = self.next_move()
            self.b.turn(move_d)
            i += 1
            if verbose and i % 3 == 0:
                print(i)
                print(np.array(self.b.grid, dtype="int"))

class MCPlayer(Player):
    """ A Monte Carlo Player for 2048.

    The players strategy is to simulate a number of moves randomly
    and pick the direction that maximizes the objective function
    for the simulated moves.

    Parameters
    ----------
    max_depth : int
        Maximum number of moves before stopping

    trials : int
        Number of times to simulate for each direction

    eval_by : str
        Expects either "min" or "sum". Either the minimum score over
        all trials is used or the total score is used. "sum" seems to
        do better.
    """

    def __init__(self, max_depth, trials, eval_by="sum"):
        self.max_depth = max_depth
        self.trials = trials
        if eval_by == "min":
            self.use_min = True
        elif eval_by == "sum":
            self.use_min = False
        else:
            raise Exception("Incorrect eval_by arg, must be either 'min' or 'sum'")
            
        self.b = Board()

    def next_move(self):
        """ Determines the best move to make next.

        For each possible move, simulates at most max_depth moves,
        ending earlier if the game is over. Picks the direction
        with the highest score over all trials"""
        
        saved_board = copy.deepcopy(self.b)
        scores = []
        for d in self.b.possible_moves():
            self.b.move(d)
            total_score = 0
            min_score = np.inf
            saved_board2 = copy.deepcopy(self.b)
            for i in range(self.trials):
                j = 0
                while(not self.b.check_game_over() and j < self.max_depth):
                    move_d = np.random.choice(self.b.possible_moves())
                    self.b.turn(move_d)
                    j += 1
            
                total_score += self.b.score
                if self.b.score < min_score:
                    min_score = self.b.score
                self.b = copy.deepcopy(saved_board2)

            if self.use_min:
                scores.append(min_score)
            else:
                scores.append(total_score)
            self.b = copy.deepcopy(saved_board)

        return self.b.possible_moves()[scores.index(max(scores))]

class ExpectimaxPlayer(Player):
    """ An expectimax tree search player for 2048.

    The players strategy is to optimize the expected value of the next
    given that the tile placed on the board will be randomly assigned
    to an empty space. The heuristic that the player uses is based
    off of how smooth the board is, how many spaces are left open,
    the score, and the number of tiles that are out of order (monotonicity)

    The weights for the heuristic are just an initial guess and
    need to be tuned. Ideas to consider are increasing the penalty
    for tiles being out of order, and possibly only considering either
    the horizontal or vertical direction.  Maybe adding a bonus for
    high tiles to be on edges and in corners.

    Parameters
    ----------
    depth : int
        Maximum number of turns before stopping. This value is either
        increased by one or decreased by one if there are few or many
        open tiles.

    h_weights : numpy.array
        Weight vector to calculate the total for the heuristic evaluation

    h_exp : numpy.array
        Vector of the exponent for each heuristic value
    """

    def __init__(self, depth,
                 h_weights=np.array([-0.1, 40, -1, 1]),
                 h_exp=np.array([1, 0.5, 1, 1])):
        self.depth = depth
        self.h_weights = h_weights
        self.h_exp = h_exp

        self.b = Board()

    def next_move(self):
        """ Determine the next move using the expectimax function.  Alters
        the depth of search based on how many tiles are currently empty."""

        saved_board = copy.deepcopy(self.b)
        scores = []
        if self.b.n_empty_tiles() >= 10:
            depth = self.depth -1
        elif self.b.n_empty_tiles() <= 5:
            depth = self.depth + 1
        else:
            depth = self.depth
        for d in self.b.possible_moves():
            self.b.move(d)
            scores.append(self.expectimax("add", depth))
            self.b = copy.deepcopy(saved_board)

        return self.b.possible_moves()[scores.index(max(scores))]

    def expectimax(self, turn, depth):
        """ Uses a version of expectiminmax algorithm to evaluate the board.
        Only performs max and random steps because there is no opposing player.
        """

        if depth == 0:
            return self.evaluate_board()
        elif turn == "move":
            if self.b.check_game_over():
                return self.evaluate_board()
            saved_board = copy.deepcopy(self.b)
            scores = []
            for d in self.b.possible_moves():
                self.b.move(d)
                scores.append(self.expectimax("add", depth))
                self.b = copy.deepcopy(saved_board)
            return max(scores)
        elif turn == "add":
            twos = []
            fours = []
            for i in self.b.empty_tiles():
                self.b.grid[i] = 2
                twos.append(self.expectimax("move", depth-1))
                self.b.grid[i] = 4
                fours.append(self.expectimax("move", depth-1))
                self.b.grid[i] = 1

            return 0.9 * np.sum(twos) + 0.1 * np.sum(fours)

    def evaluate_board(self):
        return self.board_options()

    def board_options(self):
        """ Uses a combination of four heuristics to evaluate the board: 
        the score of the game, the smoothness of the board, the number of
        empty tiles and the number of tiles that are out of place"""
        
        h = np.array([self.b.smoothness(), self.b.n_empty_tiles(),
                      self.b.n_out_of_order(), self.b.score])
        return self.h_weights.dot(h**self.h_exp)


if __name__ == "__main__":
    p = ExpectimaxPlayer(2)
    p.play(verbose=True)
