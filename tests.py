from tic_tac_toe import *


def test_is_game_full():
    game = TicTacToe()

    # Fill up first 8 slots ...
    for i in range(1, 9):
        game.set_choice(i)
        assert not game.is_full

    # Fill the last slot, check for fullness
    game.set_choice(9)
    assert game.is_full


def test_is_game_won():
    game = TicTacToe()

    # Basic across
    # X X X
    # O O -
    # - - -
    game.set_choice(1)
    assert not game.is_won

    game.set_choice(4)
    assert not game.is_won

    game.set_choice(2)
    assert not game.is_won

    game.set_choice(5)
    assert not game.is_won

    game.set_choice(3)
    assert game.is_won

    # Full diagonal
    # X O X
    # O X O
    # X O X
    game = TicTacToe()
    for i in range(1, 10):
        game.set_choice(i)
    assert game.is_won

    # Basic down
    # X - O
    # O X O
    # X X O
    game = TicTacToe()

    game.set_choice(1)
    assert not game.is_won

    game.set_choice(4)
    assert not game.is_won

    game.set_choice(7)
    assert not game.is_won

    game.set_choice(3)
    assert not game.is_won

    game.set_choice(5)
    assert not game.is_won

    game.set_choice(9)
    assert not game.is_won

    game.set_choice(8)
    assert not game.is_won

    game.set_choice(6)
    assert game.is_won
