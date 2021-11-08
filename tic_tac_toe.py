"""
Tic Tac Toe in Python3

Written and tested in Python 3.8; to use Python 3.6+ update the code to remove the single use of the
walrus operator.

By default, we assume you have have dark background terminal. A future version will do dynamic
terminal analysis and color setting; for now, set the TTT_DISPLAY_MODE environment variable to
anything other than `dark`.

By default, we assume you want to play the computer. A future version will take a parameter to drive
the automated logic; for now, set the TTT_USE_AI to anything but `true` to get a two-player game.

TODO:
* Add parameter to drive whether the computer plays none, X, O, or both.
* Dynamically set colors; interrogate existing terminal background? (might require a dependency)
* Refactor the automated logic. It's fine for Tic Tac Toe, but investigate cleaner options around
  the data structure for storing game state.

"""
import os
import random
import sys
from collections import Counter

# TODO: Convert environment variable to option handling
# fully automated games, user choice of player to automate, etc.
USE_AI = os.getenv("TTT_USE_AI", "true").lower() == "true"

# TODO: automatically select colors based on existing terminal config? yikes, not now
# Escape codes for terminal coloring: https://stackoverflow.com/a/33206814/58371
if os.getenv("TTT_DISPLAY_MODE", "dark").lower() == "dark":
    SUBTLE = "\033[38;5;240m"  # dark gray
    NORMAL = "\033[38;5;255m"  # white
else:
    SUBTLE = "\033[38;5;250m"  # light gray
    NORMAL = "\033[38;5;235m"  # mostly black

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

    if USE_AI and game.curr_player == O:
        return game.computer_generated_choice()

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
    """Exception class for unexpected game errors.

    This will usually be some kind of programming error.
    """


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

    then we'll have the following (string quotes eliminated for visual alignment).
        1, 2, 3: [1, X, 3]
        4, 5, 6: [4, X, 5]
        7, 8, 9: [O, O, X]
        1, 4, 7: [1, 4, O]
        2, 4, 8: [X, X, O]
        3, 6, 9: [3, 6, X]
        1, 5, 9: [1, X, X]
        3, 5, 7: [3, X, O]

    After each update we simply check if we have three of the current player. So if player X passes
    in a choice of 1 we'd do the following:
        update 1, 2, 3 to [X, X, 3]
        update 1, 4, 7 to [X, 4, O]
        update 1, 5, 9 to [X, X, X]  <== winning move, end the game
    """

    def __init__(self, *args, **kwargs):
        """Initialize game board, game state."""
        super().__init__(*args, **kwargs)

        self.is_won = False

        # Convention says X starts the game
        self._curr_player = X
        self._next_player = O

        # Keep track of available slots
        self.open_slots = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # set keys 1, 9 to empty value
        for i in range(1, 10):
            self[i] = ""

        # keep track of progress in known winning combinations
        self._winning_combos = {
            (1, 2, 3): [1, 2, 3],
            (4, 5, 6): [4, 5, 6],
            (7, 8, 9): [7, 8, 9],
            (1, 4, 7): [1, 4, 7],
            (2, 5, 8): [2, 5, 8],
            (3, 6, 9): [3, 6, 9],
            (1, 5, 9): [1, 5, 9],
            (3, 5, 7): [3, 5, 7],
        }

    @property
    def is_full(self):
        """Is there an open slot for the player to choose?"""
        return len(self.open_slots) == 0

    @property
    def curr_player(self):
        return self._curr_player

    @property
    def next_player(self):
        return self._next_player

    def set_choice(self, choice):
        """Update the game with the player's choice."""

        # Bail if the input is bad or the game is over
        assert 1 <= choice <= 9, "Must be an int between 1 and 9"
        if self.is_won or self.is_full:
            raise GameError("Sorry, this game is over")
        if choice not in self.open_slots:
            raise GameError(f"Choice must be one of {self.open_slots}")

        # Update the display info
        self[choice] = self.curr_player

        # Keep track of which slots are available for play
        self.open_slots.remove(choice)

        # Update the winning_combos data and check for game-winning move
        for combo, played in self._winning_combos.items():
            if choice in combo:
                idx = played.index(choice)
                self._winning_combos[combo][idx] = self.curr_player
                if played == 3 * [self.curr_player]:
                    self.is_won = True
                    return

        # Toggle the current player
        self._curr_player, self._next_player = self._next_player, self._curr_player

    def computer_generated_choice(self):
        """Starting AI logic, looks for number frequency in most common remaining winning combos."""

        def get_defensive_move(combinations):
            """Return a choice that will block a winning move, or None"""

            # For each winning Combo, if there are two of the same player and an open slot
            # return the value of that open slot
            for combo, played in combinations:
                player_count = Counter(played)
                if player_count[self.next_player] == 2:
                    defensive_moves = [move for move in played if move not in (X, O)]
                    if defensive_moves:
                        return defensive_moves.pop()

        def generate_best_options_data():
            """Return Counter object with slots that appear in most winning combos.

            Counter object returns a list of tuples: [(slot, freq), (slot_freq), ...]
            So after playing 5, the results would be [(1, 3), (3, 3), (7, 3), (9, 3)].

            The highest frequencies will be grouped at the start of the list.
            """

            # TODO: This is fairly brutish. Just playing around for now.
            # It's possible that something more elegant will require different data structures
            available_slots = []
            for opts in self._winning_combos.values():
                for opt in opts:
                    if isinstance(opt, int):
                        available_slots.append(opt)

            most_common = Counter(available_slots).most_common()
            return most_common

        # If the next play could win, block that; otherwise, pick slot that is in most winning moves
        if defensive_move := get_defensive_move(self._winning_combos.items()):
            choice = defensive_move
        else:
            all_options = generate_best_options_data()

            # We could just grab the best option (all_options[0][0]) from most_common, but that
            # results in deterministic run. That is, if we choose 5, the algorithm will always
            # choose 1, even though 3, 7, 9 are equally good choices. Let's add some randomness.
            # If the best option has a frequency of 3, gather all other options with frequency
            # of 3 and randomly choose from them. all_options is reverse sorted by highest freq.
            last_frequency = -1
            best_options = []
            for slot, freq in all_options:
                if freq < last_frequency:
                    break  # stop looping once we leave the highest freq
                last_frequency = freq
                best_options.append(slot)
            choice = random.choice(best_options)
        return choice

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
