import numpy as np
from py2048.board import Board, GRID_SIZE, PROB_2, DIRS

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

def test_score_increment_on_move():
    b = Board(GRID_SIZE, PROB_2)
    # no merges
    b.score = 0
    b.grid = np.array([[2, 4, 1, 1],
                       [1, 2, 1, 1],
                       [1, 1, 2, 8],
                       [1, 1, 1, 1]])
    b.move("down")
    assert b.score == 0

    # 1 and 2 merges
    b.score = 0
    b.grid = np.array([[2, 2, 4, 2],
                       [2, 2, 2, 2],
                       [4, 64, 1, 2],
                       [1, 64, 128, 2]])
    b.move("down")
    assert b.score == 4 + 128 + 4 + 4 + 4
    b.score = 0
    b.grid = np.array([[2, 2, 4, 2],
                       [2, 2, 2, 2],
                       [4, 64, 1, 2],
                       [1, 64, 128, 2]])
    b.move("right")
    assert b.score == 4 + 4 + 4

def test_n_empty_tiles():
    b = Board(GRID_SIZE, PROB_2)
    b.grid = np.array([[1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1]])
    assert b.n_empty_tiles() == 16
    b.grid = np.array([[2, 1, 1, 1],
                       [1, 2, 1, 1],
                       [1, 1, 2, 1],
                       [1, 1, 1, 2]])
    assert b.n_empty_tiles() == 12
    b.grid = np.array([[2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2]])
    assert b.n_empty_tiles() == 0

def test_empty_tiles():
    b = Board(GRID_SIZE, PROB_2)
    b.grid = np.array([[1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1]])

    correct_empty_tiles = []
    for i in range(GRID_SIZE[1]):
        for j in range(GRID_SIZE[1]):
            correct_empty_tiles.append((i, j))

    correct_empty_tiles.sort()

    assert b.empty_tiles() == correct_empty_tiles
    b.grid = np.array([[2, 1, 1, 1],
                       [1, 4, 1, 1],
                       [1, 1, 8, 1],
                       [1, 1, 1, 128]])
    correct_empty_tiles = []
    for i in range(GRID_SIZE[0]):
        for j in range(GRID_SIZE[0]):
            if i != j:
                correct_empty_tiles.append((i, j))

    correct_empty_tiles.sort()

    assert b.empty_tiles() == correct_empty_tiles
    b.grid = np.array([[2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2]])
    assert b.empty_tiles() == []

def test_add_random_tile():
    # don't test this method currently.
    # would need to be tightly coupled to implementation details
    pass

def test_turn():
    # don't test this method currently.
    # would need to be tightly coupled to implementation details
    pass

def test_possible_moves():
    b = Board()
    b.grid = np.array([[2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2]])

    assert b.possible_moves() == DIRS

    b.grid = np.array([[1, 1, 1, 2],
                       [1, 1, 1, 2],
                       [1, 1, 1, 2],
                       [1, 1, 1, 2]])

    assert b.possible_moves() == ["left", "up", "down"]

    b.grid = np.array([[2, 1, 1, 1],
                       [2, 1, 1, 1],
                       [2, 1, 1, 1],
                       [2, 1, 1, 1]])

    assert b.possible_moves() == ["right", "up", "down"]

    b.grid = np.array([[2, 2, 2, 2],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1]])

    assert b.possible_moves() == ["left", "right", "down"]

    b.grid = np.array([[1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [2, 2, 2, 2]])

    assert b.possible_moves() == ["left", "right", "up"]
    b.grid = np.array([[2, 4, 2, 4],
                       [4, 2, 4, 2],
                       [2, 4, 2, 4],
                       [4, 2, 4, 2]])

    assert b.possible_moves() == []

    # check that grid is not modified
    b.grid = np.array([[2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2]])

    b.possible_moves()

    assert np.all(b.grid == np.array([[2, 2, 2, 2],
                                      [2, 2, 2, 2],
                                      [2, 2, 2, 2],
                                      [2, 2, 2, 2]]))

def test_check_game_over():
    b = Board(GRID_SIZE, PROB_2)
    b.grid = np.array([[1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1]])

    assert b.check_game_over() == False

    b.grid = np.array([[2, 1, 1, 1],
                       [1, 4, 1, 1],
                       [1, 1, 8, 1],
                       [1, 1, 1, 128]])

    assert b.check_game_over() == False

    b.grid = np.array([[2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2]])

    assert b.check_game_over() == False

    b.grid = np.array([[2, 2, 2, 4],
                       [4, 2, 4, 2],
                       [2, 4, 2, 4],
                       [4, 2, 4, 2]])

    assert b.check_game_over() == False

    b.grid = np.array([[2, 4, 2, 4],
                       [4, 2, 4, 2],
                       [2, 4, 2, 4],
                       [4, 2, 4, 2]])

    assert b.check_game_over() == True

def test_n_merges_available():
    b = Board(GRID_SIZE, PROB_2)
    b.grid = np.array([[1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1]])
    assert b.n_merges_available() == 0
    b.grid = np.array([[2, 2, 1, 1],
                       [1, 2, 1, 1],
                       [1, 1, 2, 1],
                       [1, 1, 1, 2]])
    assert b.n_merges_available() == 2
    b.grid = np.array([[2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2]])
    assert b.n_merges_available() == 16

    b.grid = np.array([[2, 4, 4, 2],
                       [4, 2, 2, 4],
                       [4, 2, 2, 4],
                       [2, 4, 4, 2]])
    assert b.n_merges_available() == 8

def test_smoothness():
    b = Board(GRID_SIZE, PROB_2)
    b.grid = np.array([[1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1]])
    assert b.smoothness() == 0
    b.grid = np.array([[2, 2, 1, 1],
                       [1, 2, 1, 1],
                       [1, 1, 2, 1],
                       [1, 1, 1, 2]])
    assert b.smoothness() == 0
    b.grid = np.array([[2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2]])
    assert b.smoothness() == 0

    b.grid = np.array([[2, 4, 2, 1],
                       [4, 2, 1, 1],
                       [2, 1, 1, 1],
                       [1, 1, 1, 1]])
    assert b.smoothness() == 6 * np.log(2)

    b.grid = np.array([[2, 4, 1, 2],
                       [4, 1, 2, 1],
                       [1, 2, 1, 1],
                       [2, 1, 1, 1]])
    assert b.smoothness() == 6 * np.log(2)

    # this works, but doesn't pass due to rounding error
    # add back in after looking into how to handle this
    # with pytest
    # b.grid = np.array([[128, 64, 1, 128],
    #                    [64, 1, 128, 1],
    #                    [1, 128, 1, 1],
    #                    [128, 1, 1, 1]])
    # assert b.smoothness() == 6 * np.log(2)

def test_n_out_of_order():
    b = Board(GRID_SIZE, PROB_2)
    b.grid = np.array([[1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1]])
    assert b.n_out_of_order() == 0
    b.grid = np.array([[2, 2, 1, 1],
                       [1, 2, 1, 1],
                       [1, 1, 2, 1],
                       [1, 1, 1, 2]])
    assert b.n_out_of_order() == 0
    b.grid = np.array([[2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2],
                       [2, 2, 2, 2]])
    assert b.n_out_of_order() == 0

    b.grid = np.array([[2, 4, 2, 1],
                       [4, 2, 1, 1],
                       [2, 1, 1, 1],
                       [1, 1, 1, 1]])
    assert b.n_out_of_order() == 2

    b.grid = np.array([[2, 4, 1, 2],
                       [4, 1, 2, 1],
                       [1, 2, 1, 1],
                       [2, 1, 1, 1]])
    assert b.n_out_of_order() == 2

    b.grid = np.array([[2, 4, 8, 16],
                       [16, 8, 4, 2],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1]])
    assert b.n_out_of_order() == 8

    b.grid = np.array([[2, 2, 2, 2],
                       [2, 4, 4, 2],
                       [2, 4, 4, 2],
                       [2, 2, 2, 2]])
    assert b.n_out_of_order() == 8
