#!/usr/bin/env python
import dataclasses
import sys

SUBTLE = "\033[38;5;240m"
NORMAL = "\033[38;5;255m"
WINNING_COMBOS = {
    (1, 2, 3): "",
    (4, 5, 6): "",
    (7, 8, 9): "",
    (1, 4, 7): "",
    (2, 5, 8): "",
    (3, 6, 9): "",
    (1, 5, 9): "",
    (3, 5, 7): "",
}


@dataclasses.dataclass
class Box:
    player: str
    value: int


def play_game():
    """Show board, ask for move, check for winner. Repeat."""
    curr_player = "X"
    full = False
    won = False
    game = init_game()
    while not full and not won:
        print_game(game)
        choice = get_choice(game, curr_player)
        game = set_choice(game, curr_player, choice)
        full = is_game_full(game)
        won = is_game_won(choice, curr_player)
        if not won:
            curr_player = toggle_player(curr_player)

    print_game(game)
    print(5 * "-")
    msg = f"{curr_player} wins!!!" if won else "It's a draw."
    print(msg)


def get_choice(game, curr_player):
    """Prompt player for their next move, loop until we get a valid choice."""
    err = "Need some input"
    while err:
        choice = input(f"{curr_player} turn. Choose an open spot (identified by numbers 1-9): ")
        choice, err = is_choice_allowed(game, choice)
        if err:
            print(err)
        else:
            return choice


def set_choice(game, curr_player, choice):
    """Update the game with the player's choice."""
    game[choice].player = curr_player
    return game


def is_choice_allowed(game, choice):
    """Given a player's input, is the chosen value legal?"""
    try:
        choice = int(choice)
    except ValueError:
        return None, "Choice must be an number between 1 and 9"

    if choice < 1 or choice > 10:
        return None, "Choice must be a number between 1 and 9"

    open_slots = [k for (k, box) in game.items() if box.player == "-"]
    if choice not in open_slots:
        return None, f"Choice must be one of {open_slots}"

    return choice, ""


def is_game_full(game):
    """Is the game board full?"""
    spot_available = [box.player for box in game.values() if box.player == "-"]
    return not any(spot_available)


def toggle_player(curr_player):
    """Toggle the current player"""
    return "X" if curr_player == "O" else "O"


def is_game_won(choice, curr_player):
    """Given the player's choice, did they just win?

    There are eight ways to win in tic-tac-toe. We store the combinations (combos) for each of the
    eight ways as sorted tuple (tuples being immutable, we can use them as dict keys). For each
    combo, we keep a record of each player's slot. Note that we usually update more than one combo
    for each play (i.e. we'd update four items if the player chooses 5, two items if they choose 2,
    and so forth.

    For example, if we have the following board
        1 X 3
        4 X 6
        O O X

    then we'll have the following
        1, 2, 3: "X"
        4, 5, 6: "X"
        7, 8, 9: "OOX"
        1, 4, 7: "O"
        2, 4, 8: "XXO"
        3, 6, 9: "X"
        1, 5, 9: "XX"
        3, 5, 7" "XO"

    After each update we simply check if we have three of the current player. So if player X passes
    in a choice of 1 we'd do the following:
        update 1, 2, 3 to "XX"
        update 1, 4, 7 to "OX"
        update 1, 5, 9 to "XXX" --> Exit with True
    """
    for key, played in WINNING_COMBOS.items():
        if choice in key:
            played += curr_player
            WINNING_COMBOS[key] = played
            if played == 3 * curr_player:
                return True
    return False


def init_game():
    """Initialize the board and game tracking information."""
    game = {
        1: Box("-", 3),
        2: Box("-", 2),
        3: Box("-", 3),
        4: Box("-", 2),
        5: Box("-", 4),
        6: Box("-", 2),
        7: Box("-", 3),
        8: Box("-", 2),
        9: Box("-", 3),
    }
    for key in WINNING_COMBOS:
        WINNING_COMBOS[key] = ""

    return game


def print_game(game):
    """Given a game, print it to the console.

    NOTE: Currently assumes the console is dark.
    """
    for key, box in game.items():
        if key % 3 == 1:
            print()  # start new line in table

        content = SUBTLE + str(key) if box.player == "-" else NORMAL + box.player
        print(f"{content}", end="")
        print(" ", end="")

    print(NORMAL)


if __name__ == "__main__":
    while True:
        print()  # bit-o white-space
        is_game = input("Shall we play a game (`no` or `n` to quit)? ") or "no"
        if is_game.lower() in ["n", "no"]:
            print("Phew, thermonuclear war avoided!")
            sys.exit(0)
        play_game()
