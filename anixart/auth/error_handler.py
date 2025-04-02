from enum import IntEnum


class AnixartAuthErrors(IntEnum):
    INCORRECT_LOGIN = 2
    INCORRECT_PASSWORD = 3


def errors_handler(error):
    """Handle errors and return a JSON response."""
    pass
