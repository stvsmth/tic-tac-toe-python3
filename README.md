# Tic Tac Toe in Python 3

Implements a command-line Tic Tac Toe game in Python 3, with some automated game play.

Default play mode is human (X) vs computer(O) you play the computer, but it provides an option for
taking out the automated game play.

This is the first in what I hope will be several implementations of the game. However, as I know
Python best, and I'm fond of the command-line, this will likely be the reference implementation that
I fiddle with the most.

This code grew out of the [programming task](https://www.recurse.com/pairing-tasks) I chose for
the [Recurse Center](https://www.recurse.com/about). That task asked to upload a single file, and I
will keep that constraint for now. Therefore, I will keep most discussion of the code choices in the
file itself. The code is commented for this use case.

## Usage

```shell
python3 tic_tac_toe.py
```

### Display contrast

This is a command-line game, and we assume a dark terminal background. You can change the display to
accommodate lighter backgrounds by setting an OS environment variable: ```TTT_DISPLAY_MODE```.
Probably the best way to do this is to use the command prefix option:

```shell
TTT_DISPLAY_MODE=light ./python3 tic_tac_toe.py
```

Any value other than `dark` (case-insensitive) will enable light-mode.

### Human vs. Human or Human vs. Computer

By default, we assume you want to play the computer. If you'd like to play another human or yourself
set the ```TTT_USE_AI``` environment variable.

```shell
TTT_USE_AI=false ./python3 tic_tac_toe.py
```

Any value other than `true` (case-insensitive) will enable two-player mode.

