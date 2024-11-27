"""Interface to Google Calendar."""

from argparse import Namespace
from typing import Any, Iterator

from gcal.google import connect_to_google

__all__ = ["GoogleCalendarAPI"]


class GoogleCalendarAPI:
    """Interface to Google Calendar.

    See https://developers.google.com/calendar/api/v3/reference
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, options: Namespace) -> None:
        """Connect to Google Calendar."""

        self.options = options
        self.service = connect_to_google("calendar.readonly", "v3")

    def get_users_calendar_list(self) -> Iterator[dict[str, Any]]:
        """Yield each calendar in user's calendar list."""

        page_token = None
        while True:
            calendar_list = (
                self.service.calendarList().list(pageToken=page_token).execute()  # noqa: PLE101
            )
            for calendar in calendar_list["items"]:
                if self.options.includes and calendar["summary"] not in self.options.includes:
                    continue
                if self.options.excludes and calendar["summary"] in self.options.excludes:
                    continue
                yield calendar
            page_token = calendar_list.get("nextPageToken")
            if not page_token:
                break
