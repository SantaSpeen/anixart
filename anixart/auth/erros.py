from enum import IntEnum


class AnixartAuthError(IntEnum):
    """ Error codes for AnixartApi authentication."""
    INCORRECT_LOGIN = 1
    INCORRECT_PASSWORD = 2
