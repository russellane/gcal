"""Command Line Interface to Google Calendar."""

from pathlib import Path

from libcli import BaseCLI

from gcal.api import GoogleCalendarAPI

__all__ = ["GoogleCalendarCLI"]


class GoogleCalendarCLI(BaseCLI):
    """Command Line Interface to Google Calendar."""

    config = {
        # name of config file.
        "config-file": Path("~/.pygoogle.toml"),
        # toml [section-name].
        "config-name": "gcal",
        # distribution name, not importable package name
        "dist-name": "rlane-gcal",
    }

    api: GoogleCalendarAPI  # connection to google service

    def init_parser(self) -> None:
        """Initialize argument parser."""

        self.ArgumentParser(
            prog=__package__,
            description="Google `calendar` command line interface.",
            epilog="See `%(prog)s COMMAND --help` for help on a specific command.",
        )

    def add_arguments(self) -> None:
        """Add arguments to parser."""

        self.add_subcommand_modules("gcal.commands", prefix="Calendar", suffix="Cmd")

    def main(self) -> None:
        """Command line interface entry point (method)."""

        if not self.options.cmd:
            self.parser.print_help()
            self.parser.exit(2, "error: Missing COMMAND\n")

        self.api = GoogleCalendarAPI(self.options)
        self.options.cmd()


def main(args: list[str] | None = None) -> None:
    """Command line interface entry point (function)."""
    GoogleCalendarCLI(args).main()
