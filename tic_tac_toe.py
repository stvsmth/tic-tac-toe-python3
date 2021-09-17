#!/usr/bin/env python3
import sys

# Escape codes for terminal coloring
# https://stackoverflow.com/a/33206814/58371
# TODO: We assume a dark console!!! (because we are not monsters)
# ...   we should check terminal background and choose appropriately
# ...   but for now we can just toggle the DARK_MODE option
DARK_MODE = True

if DARK_MODE:
    SUBTLE = "\033[38;5;240m"   # mostly black
    NORMAL = "\033[38;5;255m"   # dark gray
else:
    SUBTLE = "\033[38;5;250m"   # light gray
    NORMAL = "\033[38;5;235m"   # white

X = "X"
O = "O"


def play_game():
    """Show board, ask for move, check for winner. Repeat."""
    game = TicTacToe()
    while not game.is_full and not game.is_won:
        print(game)
        choice = get_choice(game)
        game.set_choice(choice)

    # Game ended, show results
    print(game)
    game_status = f"{game.curr_player} wins!!!" if game.is_won else "It's a draw."
    print(game_status)


def get_choice(game):
    """Prompt player for their next move, loop until we get a valid choice."""
    err = "Need some input"
    while err:
        choice = input(f"{game.curr_player} turn. Choose a spot (identified by numbers 1-9): ")
        choice, err = is_choice_valid(game.open_slots, choice)
        if err:
            print(err)
        else:
            return choice


def is_choice_valid(open_slots, choice):
    """Given a player's input, is the chosen value legal?"""
    try:
        choice = int(choice)
    except ValueError:
        return None, "Choice must be a number between 1 and 9"

    if choice < 1 or choice > 10:
        return None, "Choice must be a number between 1 and 9"

    if choice not in open_slots:
        return None, f"Choice must be one of {open_slots}"

    return choice, ""


class GameError(Exception):
    pass


class TicTacToe(dict):
    """Simple dict with some game tracking and helper methods.

    How we track a win
    ==================
    There are eight ways to win in tic-tac-toe. We store the combinations (combos) for each of the
    eight ways as a tuple (tuples, being immutable, are valid dict keys). For each combo, we keep
    a record of each player's slot. Note that we usually update more than one combo for each play
    (i.e. we'd update four items if the player chooses 5, two items if they choose 2, and so forth.

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
        update 1, 5, 9 to "XXX"
    """

    def __init__(self, *args, **kwargs):
        """Initialize game board, game state."""
        super().__init__(*args, **kwargs)

        self.is_won = False

        # Convention says X starts the game
        self.curr_player = X

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

    def set_choice(self, choice):
        """Update the game with the player's choice."""
        assert 1 <= choice <= 9, "Must be an int between 1 and 9"

        # Don't move forward if the game is over
        if self.is_won or self.is_full:
            raise GameError("Sorry, this game is over")

        if choice not in self.open_slots:
            raise GameError(f"Choice must be one of {self.open_slots}")

        # Update the display info
        self[choice] = self.curr_player

        # Update # of slots open
        self.slots_left -= 1

        # Update the winner matrix, possibly game won state
        for combo, played in self.winning_combos.items():
            if choice in combo:
                played += self.curr_player
                self.winning_combos[combo] = played
                if played == 3 * self.curr_player:
                    self.is_won = True
                    return

        self.curr_player = X if self.curr_player == O else O

    @property
    def open_slots(self):
        """Get a list of which choices are still available."""
        return [k for (k, player) in self.items() if not player]

    def __repr__(self):
        """Generate string representation of Tic Tac Toe game."""
        content = ""
        for key, player in self.items():
            # Put a space (between boxes) or new-line (after 3, 6, 9) to create a 3 x 3 table
            eol = "\n" if key % 3 == 1 else " "
            content += eol
            content += NORMAL + player if player else SUBTLE + str(key)
        return content + NORMAL


if __name__ == "__main__":
    while True:
        wants_to_play = input("\nShall we play a game (`no` or `n` to quit)? ") or "no"
        if wants_to_play.lower() in ["n", "no", "q", "quit"]:
            print("Phew, thermonuclear war avoided!")
            sys.exit(0)
        play_game()
