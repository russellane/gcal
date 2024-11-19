import os
import sys

import pytest

from gcal.cli import GoogleCalendarCLI

slow = pytest.mark.skipif(not os.environ.get("SLOW"), reason="slow")


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


@slow
@pytest.mark.parametrize(
    ("start", "end"),
    [
        ("all", "all"),
        ("all", "today + 30 days"),
        ("all", None),
        #
        ("today", "all"),
        ("today", "today + 30 days"),
        ("today", None),
        #
        (None, "all"),
        (None, "today + 30 days"),
        (None, None),
    ],
)
def test_gcal_events2(start: str | None, end: str | None) -> None:

    args = ["events"]
    if start:
        args += ["--start", start]
    if end:
        args += ["--end", end]

    run_cli(args)
