from enum import IntEnum


class AnixartComment(IntEnum):
    DISLIKE = 1
    LIKE = 2


class AnixartProfileVotedSort(IntEnum):
    LAST_FIRST = 1
    OLD_FIRST = 2
    STAR_5 = 3
    STAR_4 = 4
    STAR_3 = 5
    STAR_2 = 6
    STAR_1 = 7


class AnixartLists(IntEnum):
    WATCHING = 1
    IN_PLANS = 2
    WATCHED = 3
    POSTPONED = 4
    DROPPED = 5
