from enum import IntEnum


class AnixartProfileErrors(IntEnum):
    """ Error codes for AnixartApi authentication."""
    PROFILE_NOT_FOUND = 2


def errors_handler(error):
    """Handle errors and return a JSON response."""
    pass
