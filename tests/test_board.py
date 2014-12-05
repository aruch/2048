import numpy as np
from py2048.board import Board

GRID_SIZE = (4,4)
PROB_2 = 0.9

def test_move_left():
    b = Board(GRID_SIZE, PROB_2)
    # no merges
    b.grid = np.array([[2, 4, 1, 1],
                       [1, 2, 1, 1],
                       [1, 1, 1, 8],
                       [1, 1, 1, 1]])
    b.move("left")
    assert np.all(b.grid == np.array([[2, 4, 1, 1],
                                      [2, 1, 1, 1],
                                      [8, 1, 1, 1],
                                      [1, 1, 1, 1]]))
    # 1 and 2 merges
    b.grid = np.array([[2, 2, 4, 1],
                       [2, 2, 2, 2],
                       [64, 64, 1, 8],
                       [128, 2, 128, 1]])
    b.move("left")
    assert np.all(b.grid == np.array([[4, 4, 1, 1],
                                      [4, 4, 1, 1],
                                      [128, 8, 1, 1],
                                      [128, 2, 128, 1]]))

def test_move_right():
    b = Board(GRID_SIZE, PROB_2)
    # no merges
    b.grid = np.array([[2, 4, 1, 1],
                       [1, 2, 1, 1],
                       [1, 1, 1, 8],
                       [1, 1, 1, 1]])
    b.move("right")
    assert np.all(b.grid == np.array([[1, 1, 2, 4],
                                      [1, 1, 1, 2],
                                      [1, 1, 1, 8],
                                      [1, 1, 1, 1]]))
    # 1 and 2 merges
    b.grid = np.array([[2, 2, 4, 1],
                       [2, 2, 2, 2],
                       [64, 64, 1, 8],
                       [128, 2, 128, 1]])
    b.move("right")
    assert np.all(b.grid == np.array([[1, 1, 4, 4],
                                      [1, 1, 4, 4],
                                      [1, 1, 128, 8],
                                      [1, 128, 2, 128]]))

def test_move_up():
    b = Board(GRID_SIZE, PROB_2)
    # no merges
    b.grid = np.array([[2, 4, 1, 1],
                       [1, 2, 1, 1],
                       [1, 1, 2, 8],
                       [1, 1, 1, 1]])
    b.move("up")
    assert np.all(b.grid == np.array([[2, 4, 2, 8],
                                      [1, 2, 1, 1],
                                      [1, 1, 1, 1],
                                      [1, 1, 1, 1]]))
    # 1 and 2 merges
    b.grid = np.array([[2, 2, 4, 2],
                       [2, 2, 2, 2],
                       [4, 64, 1, 2],
                       [1, 64, 128, 2]])
    b.move("up")
    assert np.all(b.grid == np.array([[4, 4, 4, 4],
                                      [4, 128, 2, 4],
                                      [1, 1, 128, 1],
                                      [1, 1, 1, 1]]))

def test_move_down():
    b = Board(GRID_SIZE, PROB_2)
    # no merges
    b.grid = np.array([[2, 4, 1, 1],
                       [1, 2, 1, 1],
                       [1, 1, 2, 8],
                       [1, 1, 1, 1]])
    b.move("down")
    assert np.all(b.grid == np.array([[1, 1, 1, 1],
                                      [1, 1, 1, 1],
                                      [1, 4, 1, 1],
                                      [2, 2, 2, 8]]))
    # 1 and 2 merges
    b.grid = np.array([[2, 2, 4, 2],
                       [2, 2, 2, 2],
                       [4, 64, 1, 2],
                       [1, 64, 128, 2]])
    b.move("down")
    assert np.all(b.grid == np.array([[1, 1, 1, 1],
                                      [1, 1, 4, 1],
                                      [4, 4, 2, 4],
                                      [4, 128, 128, 4]]))
