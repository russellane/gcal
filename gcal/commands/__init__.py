"""Google Calendar Commands."""

from argparse import ArgumentParser, _ArgumentGroup
from typing import Any, TypeVar

from libcli import BaseCmd
from loguru import logger
from rich.pretty import pprint as rich_pretty_print

from gcal.cli import GoogleCalendarCLI

Parser = TypeVar("Parser", ArgumentParser, _ArgumentGroup)

__all__ = ["GoogleCalendarCmd"]


class GoogleCalendarCmd(BaseCmd):
    """Base class of google calendar commands."""

    cli: GoogleCalendarCLI

    def add_limit_option(self, parser: Parser) -> None:
        """Add `--limit` to the given `parser`."""

        parser.add_argument(
            "--limit",
            type=int,
            help="limit execution to `LIMIT` number of items",
        )

    def check_limit(self) -> bool:
        """Call at top of loop before performing work."""

        if self.options.limit is None:
            logger.trace("No limit")
            return False

        self.options.limit -= 1
        logger.trace("limit {!r}", self.options.limit)
        assert isinstance(self.options.limit, int)
        return self.options.limit < 0

    def add_pretty_print_option(self, parser: Parser) -> None:
        """Add `--pretty-print` to the given `parser`."""

        parser.add_argument(
            "--pretty-print",
            action="store_true",
            help="pretty-print items",
        )

    @staticmethod
    def pprint(obj: Any, **kwargs: Any) -> None:
        """Make `pprint` convenient."""

        rich_pretty_print(obj, **kwargs)

    @staticmethod
    def add_includes_excludes_options(parser: Parser) -> None:
        """Add `--include-calendars` and `--exclude-calendars` to the given `parser`."""

        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            "--include-calendars",
            dest="includes",
            metavar="CALENDARS",
            nargs="*",
            help="Only display from the given list of calendars.",
        )

        group.add_argument(
            "--exclude-calendars",
            dest="excludes",
            metavar="CALENDARS",
            nargs="*",
            help="Do not display from the given list of calendars.",
        )
