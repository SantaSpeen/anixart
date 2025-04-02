from enum import IntEnum


class AnixartAuthErrors(IntEnum):
    """ Error codes for AnixartApi authentication."""
    INCORRECT_LOGIN = 1
    INCORRECT_PASSWORD = 2


def errors_handler(error):
    """Handle errors and return a JSON response."""
    pass
