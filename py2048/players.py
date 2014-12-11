""" Defines a number of AI players for 2048"""

from py2048.board import Board
import copy
import time
import numpy as np

class Player:
    """ A parent class for the other AI players """
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
