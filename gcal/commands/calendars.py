"""Calendar `calendars` command module."""

import rich
from libcli import BaseCmd
from rich.box import ROUNDED
from rich.table import Table

from gcal.cli import GoogleCalendarCLI

__all__ = ["CalendarListCalendarsCmd"]


class CalendarListCalendarsCmd(BaseCmd):
    """Calendar `calendars` command class."""

    def init_command(self) -> None:
        """Initialize Calandar `calendars` command."""

        self.add_subcommand_parser(
            "calendars",
            help="Display calendars in the user's calendar list",
            description=self.cli.dedent(
                """
    The `%(prog)s` program displays all calendars in the user's `calendar list`.
                """,
            ),
        )

    def run(self) -> None:
        """Run Calendar `calendars` command."""

        table = Table(
            "Summary",
            "Description",
            "Time Zone",
            "Access Role",
            "Color",
            box=ROUNDED,
            show_lines=True,
            style="#d06b64",
            title="User's Calendar List",
            title_style="#d06b64 italic",
            header_style="#d06b64 italic",
        )

        assert isinstance(self.cli, GoogleCalendarCLI)

        for entry in self.cli.api.get_users_calendar_list():

            table.add_row(
                entry["summary"],
                entry.get("description", ""),
                entry["timeZone"],
                entry["accessRole"],
                entry["backgroundColor"],
                style=f"{entry['backgroundColor']} on {entry['foregroundColor']}",
            )

        rich.print(table)
