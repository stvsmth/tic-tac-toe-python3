from tic_tac_toe import *

import pytest


def test_toggle_player():
    assert toggle_player("X") == "O"
    assert toggle_player("O") == "X"
    with pytest.raises(InvalidGameError):
        toggle_player("42")


def test_is_game_full():
    curr_player = "X"
    game = TicTacToe()

    # Fill up first 8 slots ...
    for i in range(1, 9):
        game = set_choice(game, curr_player, i)
        curr_player = toggle_player(curr_player)
        assert not game.is_full

    # Fill the last slot, check for fullness
    game = set_choice(game, curr_player, 9)
    assert game.is_full


def test_is_game_won():
    game = TicTacToe()

    # Basic across
    # X X X
    # O O -
    # - - -
    curr_player = "X"
    game = set_choice(game, curr_player, 1)
    assert not game.is_won

    curr_player = toggle_player(curr_player)
    game = set_choice(game, curr_player, 4)
    assert not game.is_won

    curr_player = toggle_player(curr_player)
    game = set_choice(game, curr_player, 2)
    assert not game.is_won

    curr_player = toggle_player(curr_player)
    game = set_choice(game, curr_player, 5)
    assert not game.is_won

    curr_player = toggle_player(curr_player)
    game = set_choice(game, curr_player, 3)
    assert game.is_won

    # Full diagonal
    # X O X
    # O X O
    # X O X
    game = TicTacToe()
    curr_player = "X"
    for i in range(1, 10):
        game = set_choice(game, curr_player, i)
        curr_player = toggle_player(curr_player)
    assert game.is_won

    # Basic down
    # X - O
    # O X O
    # X X O
    game = TicTacToe()

    curr_player = "X"
    game = set_choice(game, curr_player, 1)
    assert not game.is_won

    curr_player = toggle_player(curr_player)
    game = set_choice(game, curr_player, 4)
    assert not game.is_won

    curr_player = toggle_player(curr_player)
    game = set_choice(game, curr_player, 7)
    assert not game.is_won

    curr_player = toggle_player(curr_player)
    game = set_choice(game, curr_player, 3)
    assert not game.is_won

    curr_player = toggle_player(curr_player)
    game = set_choice(game, curr_player, 5)
    assert not game.is_won

    curr_player = toggle_player(curr_player)
    game = set_choice(game, curr_player, 9)
    assert not game.is_won

    curr_player = toggle_player(curr_player)
    game = set_choice(game, curr_player, 8)
    assert not game.is_won

    curr_player = toggle_player(curr_player)
    game = set_choice(game, curr_player, 6)
    assert game.is_won
