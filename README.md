# Pystone

This is a quickly put together hearthstone (deck) tracker made for linux.

To use this tracker you must setup hearthstone to track your games:
follow
[these](https://www.reddit.com/r/hearthstone/comments/268fkk/simple_hearthstone_logging_see_your_complete_play)
instructions.

It is very fragile right now and I wouldn't be surprised if it didn't
work on other setups.

## Requirements

Just
[click](http://click.pocoo.org/5/).

## Usage

Running the program:

```bash
python track.py path/to/hearthstone/output_log.txt command
```

For example my path is
`~/.PlayOnLinux/wineprefix/hearthstone/drive_c/Program\
Files/Hearthstone/Hearthstone_Data/output_log.txt`.

Currently the only commands are `track` and `clear`.  `track` runs the
deck tracker and `clear` clears old log data.  More tips below.

Before every new game (before you queue) **and before the first time
you run it** you need to run the `clear` command (fix this in future).

Sometimes it seems to get stuck somehow in the middle of a game. If
this happens just Ctrl-C and restart it in `track` mode (fix this in
future). The log file contents will still be there so you will
not lose any state.

## Future Plans

I have plans.
