"""Calendar `events` command module."""

import datetime
from typing import Any, Iterator

import dateparser
import rich
from rich.box import ROUNDED
from rich.table import Table

from gcal.commands import GoogleCalendarCmd

__all__ = ["CalendarListEventsCmd"]


class CalendarListEventsCmd(GoogleCalendarCmd):
    """Calendar `events` command class."""

    start_date: datetime.datetime | None
    end_date: datetime.datetime | None

    def init_command(self) -> None:
        """Initialize Calendar `events` command."""

        parser = self.add_subcommand_parser(
            "events",
            help="Display scheduled events",
            description=self.cli.dedent(
                """
    The `%(prog)s` program displays all events scheduled in all calendars
    in the user's `calendar list`.
                """,
            ),
        )

        parser.add_argument(
            "-s",
            "--start",
            dest="start_date",
            help=self.cli.dedent(
                """
    List events at or after `START_DATE` (inclusive) (YYYY-MM-DD).
    Defaults to `today`. Use `all` to not filter by start-date.
                """
            ),
        )

        parser.add_argument(
            "-e",
            "--end",
            dest="end_date",
            help=self.cli.dedent(
                """
    List events prior to `END_DATE` (exclusive) (YYYY-MM-DD).
    Defaults to `NUMDAYS` from `START_DATE`. Use `all` to not filter by end-date.
                """
            ),
        )

        arg = parser.add_argument(
            "-n",
            "--numdays",
            dest="numdays",
            type=int,
            default=90,
            help=self.cli.dedent(
                """
    List up to `NUMDAYS` days of events.
                """
            ),
        )
        self.cli.add_default_to_help(arg, parser)

        self.add_includes_excludes_options(parser)
        self.add_limit_option(parser)
        self.add_pretty_print_option(parser)

    def run(self) -> None:
        """Run Calendar `events` command."""

        # START_DATE
        if self.cli.options.start_date == "all":
            self.start_date = None  # Don't filter on start-date.
        elif self.cli.options.start_date:
            # Use what's given,
            self.start_date = dateparser.parse(self.cli.options.start_date)
        else:
            # or default to `today`.
            self.start_date = dateparser.parse("today")

        # END_DATE
        self.end_date = None  # Don't filter on end-date.
        if self.cli.options.end_date != "all" and self.cli.options.end_date:
            # Use what's given,
            self.end_date = dateparser.parse(self.cli.options.end_date)
        elif self.start_date:
            # or default to `NUMDAYS` from `START_DATE` (if given).
            self.end_date = self.start_date + datetime.timedelta(days=self.cli.options.numdays)

        table = Table(
            "Calendar",
            "Date",
            "Time",
            "Event",
            box=ROUNDED,
            style="#d06b64",
            title="Calendar Events",
            title_style="#d06b64 italic",
            header_style="#d06b64 italic",
        )

        last_month = None

        for event in sorted(self._get_users_events(), key=lambda x: x["_start_date"]):

            if self.check_limit():
                break

            if _date_time := event["start"].get("dateTime"):
                _dt = dateparser.parse(_date_time)
                assert _dt
                date = _dt.strftime("%Y %a %b %e")
                time = _dt.strftime("%H:%M")

            elif _date := event["start"].get("date"):
                _dt = dateparser.parse(_date)
                assert _dt
                date = _dt.strftime("%Y %a %b %e")
                time = ""

            else:
                raise RuntimeError(
                    "event['start'] missing `dateTime` and `date`."
                )  # pragma: no cover

            if not self.cli.options.pretty_print and last_month and last_month != _dt.month:
                table.add_section()
            last_month = _dt.month

            calendar = event["_calendar"]

            if self.cli.options.pretty_print:
                self.pprint(calendar)
                continue

            table.add_row(
                calendar["summary"],
                date,
                time,
                event["summary"],
                style=f"{calendar['backgroundColor']} on {calendar['foregroundColor']}",
            )

        if not self.cli.options.pretty_print:
            rich.print(table)

    def _get_users_events(self) -> Iterator[dict[str, Any]]:
        """Yield events from all calendars in user's calendar list."""

        for calendar in self.cli.api.get_users_calendar_list():

            for event in self._get_calendar_events(calendar):

                event["_start_date"] = event["start"].get("dateTime", event["start"].get("date"))
                event["_calendar"] = calendar
                yield event

    def _get_calendar_events(self, calendar: dict[str, Any]) -> Iterator[dict[str, Any]]:
        """Yield events from the given `calendar`."""

        args = {
            "calendarId": calendar["id"],
            "singleEvents": True,
        }

        if self.start_date:
            args["timeMin"] = self.start_date.isoformat() + "Z"  # `Z` indicates `UTC`.

        if self.end_date:
            args["timeMax"] = self.end_date.isoformat() + "Z"  # `Z` indicates `UTC`.

        result = self.cli.api.service.events().list(**args).execute()
        yield from result.get("items", [])
