from enum import IntEnum, unique


@unique
class Action(IntEnum):
    EMPTY = 0
    HIT = 1
    STAND = 2
    DOUBLE = 3
    SURRENDER = 4
