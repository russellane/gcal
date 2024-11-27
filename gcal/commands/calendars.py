"""Calendar `calendars` command module."""

import rich
from rich.box import ROUNDED
from rich.table import Table

from gcal.commands import GoogleCalendarCmd

__all__ = ["CalendarListCalendarsCmd"]


class CalendarListCalendarsCmd(GoogleCalendarCmd):
    """Calendar `calendars` command class."""

    def init_command(self) -> None:
        """Initialize Calendar `calendars` command."""

        parser = self.add_subcommand_parser(
            "calendars",
            help="Display calendars in the user's calendar list",
            description=self.cli.dedent(
                """
    The `%(prog)s` program displays all calendars in the user's `calendar list`.
                """,
            ),
        )

        self.add_includes_excludes_options(parser)
        self.add_limit_option(parser)
        self.add_pretty_print_option(parser)

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

        for entry in self.cli.api.get_users_calendar_list():

            if self.check_limit():
                break

            if self.cli.options.pretty_print:
                self.pprint(entry)
                continue

            table.add_row(
                entry["summary"],
                entry.get("description", ""),
                entry["timeZone"],
                entry["accessRole"],
                entry["backgroundColor"],
                style=f"{entry['backgroundColor']} on {entry['foregroundColor']}",
            )

        if not self.cli.options.pretty_print:
            rich.print(table)
