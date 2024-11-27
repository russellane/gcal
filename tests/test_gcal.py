import os
import sys

import pytest

from gcal.cli import main

slow = pytest.mark.skipif(not os.environ.get("SLOW"), reason="slow")


def run_cli(options: list[str]) -> None:
    """Test calling the cli directly."""

    sys.argv = ["gcal"]
    if options:
        sys.argv += options
    print(f"\nRunning {sys.argv!r}", flush=True)
    main()


def test_gcal_no_args() -> None:
    with pytest.raises(SystemExit) as err:
        run_cli([])
    assert err.value.code == 2


# -------------------------------------------------------------------------------


def test_gcal_calendars() -> None:
    run_cli(["calendars"])


def test_gcal_calendars_limit_2() -> None:
    run_cli(["calendars", "--limit", "2"])


def test_gcal_calendars_pretty_print() -> None:
    run_cli(["calendars", "--pretty-print"])


def test_gcal_calendars_limit_2_pretty_print() -> None:
    run_cli(["calendars", "--limit", "2", "--pretty-print"])


# -------------------------------------------------------------------------------


def test_gcal_events() -> None:
    run_cli(["events"])


def test_gcal_events_limit_2() -> None:
    run_cli(["events", "--limit", "2"])


def test_gcal_events_pretty_print() -> None:
    run_cli(["events", "--pretty-print"])


def test_gcal_events_limit_2_pretty_print() -> None:
    run_cli(["events", "--limit", "2", "--pretty-print"])


# -------------------------------------------------------------------------------


@slow
@pytest.mark.parametrize(
    ("start", "end"),
    [
        ("all", "all"),
        ("all", "in 30 days"),
        ("all", None),
        #
        ("today", "all"),
        ("today", "in 30 days"),
        ("today", None),
        #
        (None, "all"),
        (None, "in 30 days"),
        (None, None),
    ],
)
def test_gcal_events_bounded(start: str | None, end: str | None) -> None:
    args = ["events"]
    if start:
        args += ["--start", start]
    if end:
        args += ["--end", end]
    run_cli(args)


# -------------------------------------------------------------------------------


def test_gcal_includes_events() -> None:
    run_cli(["events", "--include-calendars", "Holidays in United States"])


def test_gcal_includes_events2() -> None:
    run_cli(["events", "--include-calendars", "Holidays in United States", "Phases of the Moon"])


def test_gcal_excludes_events() -> None:
    run_cli(["events", "--exclude-calendars", "Holidays in United States"])


def test_gcal_excludes_events2() -> None:
    run_cli(["events", "--exclude-calendars", "Holidays in United States", "Phases of the Moon"])
