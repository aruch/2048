import numpy as np
from py2048.board import Board

GRID_SIZE = (5,5)
PROB_2 = 0.9

def test_move_left():
    b = Board(GRID_SIZE, PROB_2)
    # no merges
    b.grid = np.array([[2, 4, 1, 1, 1],
                       [1, 2, 1, 1, 1],
                       [1, 1, 1, 8, 1],
                       [1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1]])
    b.move("left")
    assert np.all(b.grid == np.array([[2, 4, 1, 1, 1],
                                      [2, 1, 1, 1, 1],
                                      [8, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1],
                                      [1, 1, 1, 1, 1]]))
    # 1 and 2 merges
    b.grid = np.array([[2, 2, 4, 1, 1],
                       [2, 2, 2, 2, 1],
                       [64, 64, 1, 8, 1],
                       [128, 1, 128, 1, 1],
                       [128, 2, 128, 1, 1]])
    b.move("left")
    assert np.all(b.grid == np.array([[4, 4, 1, 1, 1],
                                      [4, 4, 1, 1, 1],
                                      [128, 8, 1, 1, 1],
                                      [256, 1, 1, 1, 1],
                                      [128, 2, 128, 1, 1]]))
