#!/usr/bin/env python
import sys

SUBTLE = "\033[38;5;240m"
NORMAL = "\033[38;5;255m"
X = "X"
O = "O"


class InvalidGameError(Exception):
    pass


class TicTacToe(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.curr_player = X
        
        self.is_won = False

        # Keep track of # of turns taken, for fullness check
        self.slots_left = 9

        # set keys 1, 9 to empty value
        for i in range(1, 10):
            self[i] = ""

        # keep track of progress in known winning combinations
        self.winning_combos = {
            (1, 2, 3): "",
            (4, 5, 6): "",
            (7, 8, 9): "",
            (1, 4, 7): "",
            (2, 5, 8): "",
            (3, 6, 9): "",
            (1, 5, 9): "",
            (3, 5, 7): "",
        }

    @property
    def is_full(self):
        return self.slots_left == 0

    def __repr__(self):
        """Generate string representation of Tic Tac Toe game.

        NOTE: Currently assumes the console is dark.
        """
        content = ""
        for key, player in self.items():
            if key % 3 == 1:
                content += "\n"  # start new line in table
            else:
                content += " "  # space between boxes
            content += NORMAL + player if player else SUBTLE + str(key)
        return content + NORMAL


def play_game():
    """Show board, ask for move, check for winner. Repeat."""
    game = TicTacToe()
    while not game.is_full and not game.is_won:
        print(game)
        choice = get_choice(game)
        game = set_choice(game, choice)

    # Game ended, show results
    print(game)
    game_status = f"{game.curr_player} wins!!!" if game.is_won else "It's a draw."
    print(game_status)


def get_choice(game):
    """Prompt player for their next move, loop until we get a valid choice."""
    err = "Need some input"
    while err:
        choice = input(f"{game.curr_player} turn. Choose a spot (identified by numbers 1-9): ")
        choice, err = is_choice_allowed(game, choice)
        if err:
            print(err)
        else:
            return choice


def set_choice(game, choice):
    """Update the game with the player's choice."""
    # Maybe we'll override set and handle this in the class later
    assert 1 <= choice <= 9, "Must be an int between 1 and 9"

    # Update the display info
    game[choice] = game.curr_player

    # Update # of slots open
    game.slots_left -= 1

    # Update the winner matrix, possibly game won state
    for combo, played in game.winning_combos.items():
        if choice in combo:
            played += game.curr_player
            game.winning_combos[combo] = played
            if played == 3 * game.curr_player:
                game.is_won = True
                return game

    game.curr_player = X if game.curr_player == O else O
    return game


def is_choice_allowed(game, choice):
    """Given a player's input, is the chosen value legal?"""
    try:
        choice = int(choice)
    except ValueError:
        return None, "Choice must be an number between 1 and 9"

    if choice < 1 or choice > 10:
        return None, "Choice must be a number between 1 and 9"

    open_slots = [k for (k, player) in game.items() if not player]
    if choice not in open_slots:
        return None, f"Choice must be one of {open_slots}"

    return choice, ""


if __name__ == "__main__":
    while True:
        wants_to_play = input("\nShall we play a game (`no` or `n` to quit)? ") or "no"
        if wants_to_play.lower() in ["n", "no", "q", "quit"]:
            print("Phew, thermonuclear war avoided!")
            sys.exit(0)
        play_game()
