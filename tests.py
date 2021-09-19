import pytest

from tic_tac_toe import *

# X X O
# O X X
# X O O
FULL_GAME_DRAW_SEQUENCE = [2, 4, 6, 8, 1, 3, 5, 9, 7]


def test_is_game_full():
    game = TicTacToe()

    # Fill up first 8 slots ...
    almost_full = FULL_GAME_DRAW_SEQUENCE.copy()
    almost_full.pop()
    for i in almost_full:
        game.set_choice(i)
        assert not game.is_full

    game.set_choice(7)
    assert game.is_full


def test_open_slots():
    game = TicTacToe()
    expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert expected == game.open_slots

    for i in FULL_GAME_DRAW_SEQUENCE:
        game.set_choice(i)
        expected.remove(i)
        assert expected == game.open_slots


def test_game_play_stops():
    game = TicTacToe()
    for i in FULL_GAME_DRAW_SEQUENCE:
        game.set_choice(i)
    assert game.is_full

    with pytest.raises(GameError):
        game.set_choice(5)


def test_is_choice_valid():
    game = TicTacToe()

    choice, err = is_choice_valid(game.open_slots, "5")
    assert not err
    assert choice == 5

    choice, err = is_choice_valid(game.open_slots, " 5 ")
    assert not err
    assert choice == 5

    game.set_choice(5)
    choice, err = is_choice_valid(game.open_slots, "5")
    assert not choice
    assert err == "Choice must be one of [1, 2, 3, 4, 6, 7, 8, 9]"

    choice, err = is_choice_valid(game.open_slots, "x")
    assert not choice
    assert "Choice must be a number between 1 and 9" == err

    choice, err = is_choice_valid(game.open_slots, "0")
    assert not choice
    assert "Choice must be a number between 1 and 9" == err

    choice, err = is_choice_valid(game.open_slots, "-2")
    assert not choice
    assert "Choice must be a number between 1 and 9" == err

    choice, err = is_choice_valid(game.open_slots, "42")
    assert not choice
    assert "Choice must be a number between 1 and 9" == err

    choice, err = is_choice_valid(game.open_slots, "")
    assert not choice
    assert "Choice must be a number between 1 and 9" == err


def test_is_game_won():
    game = TicTacToe()

    # Basic across
    # X X X
    # O O -
    # - - -
    for i in [1, 4, 2, 5]:
        game.set_choice(i)
        assert not game.is_won

    game.set_choice(3)
    assert game.is_won

    # Full diagonal
    # X O X
    # O X O
    # X - -
    game = TicTacToe()
    for i in range(1, 8):
        game.set_choice(i)
    assert game.is_won

    # Basic down
    # X - O
    # O X O
    # X X O
    game = TicTacToe()

    for i in [1, 4, 7, 3, 5, 9, 8]:
        game.set_choice(i)
        assert not game.is_won

    game.set_choice(6)
    assert game.is_won
