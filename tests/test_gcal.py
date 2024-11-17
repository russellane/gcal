import sys

import pytest

from gcal.cli import GoogleCalendarCLI


def run_cli(options: list[str]) -> None:
    """Test calling the cli directly."""

    sys.argv = ["gcal"]
    if options:
        sys.argv += options
    print(f"\nRunning {sys.argv!r}", flush=True)
    GoogleCalendarCLI().main()


def test_gcal_no_args() -> None:
    with pytest.raises(SystemExit) as err:
        run_cli([])
    assert err.value.code == 2


def test_gcal_calendars() -> None:
    run_cli(["calendars"])


def test_gcal_events() -> None:
    run_cli(["events"])
