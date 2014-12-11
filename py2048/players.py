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
