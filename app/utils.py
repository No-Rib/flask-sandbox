"""Various utils for the app."""


TIMESTAMP_WEB_FORMAT = "%-d %b %Y %H:%M"
"""Default format fof datetime for web representation.

    Format: "1 Jan 1970 00:00"
"""


def format_datetime(timestamp):
    """Formats datetime object for web representation."""

    return timestamp.strftime(TIMESTAMP_WEB_FORMAT)
