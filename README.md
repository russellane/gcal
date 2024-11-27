# gcal
```
usage: gcal [-h] [-H] [-v] [-V] [--config FILE] [--print-config] [--print-url]
            [--completion [SHELL]]
            COMMAND ...

Google `calendar` command line interface.

Specify one of:
  COMMAND
    calendars           Display calendars in the user's calendar list.
    events              Display scheduled events.

General options:
  -h, --help            Show this help message and exit.
  -H, --long-help       Show help for all commands and exit.
  -v, --verbose         `-v` for detailed output and `-vv` for more detailed.
  -V, --version         Print version number and exit.
  --config FILE         Use config `FILE` (default: `~/.pygoogle.toml`).
  --print-config        Print effective config and exit.
  --print-url           Print project url and exit.
  --completion [SHELL]  Print completion scripts for `SHELL` and exit
                        (default: `bash`).

See `gcal COMMAND --help` for help on a specific command.
```

## gcal calendars
```
usage: gcal calendars [-h] [--include-calendars [CALENDARS ...] |
                      --exclude-calendars [CALENDARS ...]] [--limit LIMIT]
                      [--pretty-print]

The `gcal calendars` program displays all calendars in the user's `calendar list`.

options:
  -h, --help            Show this help message and exit.
  --include-calendars [CALENDARS ...]
                        Only display from the given list of calendars.
  --exclude-calendars [CALENDARS ...]
                        Do not display from the given list of calendars.
  --limit LIMIT         Limit execution to `LIMIT` number of items.
  --pretty-print        Pretty-print items.
```

## gcal events
```
usage: gcal events [-h] [-s START_DATE] [-e END_DATE] [-n NUMDAYS]
                   [--include-calendars [CALENDARS ...] |
                   --exclude-calendars [CALENDARS ...]] [--limit LIMIT]
                   [--pretty-print]

The `gcal events` program displays all events scheduled in all calendars
in the user's `calendar list`.

options:
  -h, --help            Show this help message and exit.
  -s, --start START_DATE
                        List events at or after `START_DATE` (inclusive)
                        (YYYY-MM-DD). Defaults to `today`. Use `all` to not
                        filter by start-date.
  -e, --end END_DATE    List events prior to `END_DATE` (exclusive) (YYYY-MM-
                        DD). Defaults to `NUMDAYS` from `START_DATE`. Use
                        `all` to not filter by end-date.
  -n, --numdays NUMDAYS
                        List up to `NUMDAYS` days of events (default: `90`).
  --include-calendars [CALENDARS ...]
                        Only display from the given list of calendars.
  --exclude-calendars [CALENDARS ...]
                        Do not display from the given list of calendars.
  --limit LIMIT         Limit execution to `LIMIT` number of items.
  --pretty-print        Pretty-print items.
```

