from enum import Enum


class Value(Enum):
    def __init__(self, full_name, symbol):
        self.full_name = full_name
        self.symbol = symbol

    def __str__(self):
        return self.string_value()

    def string_value(self, only_symbol: bool = True) -> str:
        return self.symbol if only_symbol else self.full_name

    ACE = ("ace", "A")
    TWO = ("two", "2")
    THREE = ("three", "3")
    FOUR = ("four", "4")
    FIVE = ("five", "5")
    SIX = ("six", "6")
    SEVEN = ("seven", "7")
    EIGHT = ("eight", "8")
    NINE = ("nine", "9")
    TEN = ("ten", "10")
    JACK = ("jack", "J")
    QUEEN = ("queen", "Q")
    KING = ("king", "K")


class Color(Enum):
    def __init__(self, full_name, black_symbol, white_symbol):
        self.full_name = full_name
        self.black_symbol = black_symbol
        self.white_symbol = white_symbol

    def __str__(self, only_icon: bool = True, use_black: bool = True):
        return self.string_value()

    def string_value(self, only_icon: bool = True, use_black: bool = True) -> str:
        if only_icon:
            return self.black_symbol if use_black else self.white_symbol
        else:
            return self.full_name

    HEART = ("heart", "\u2665", "\u2661")
    DIAMOND = ("diamond", "\u2666", "\u2662")
    CLUB = ("club", "\u2663", "\u2667")
    SPADE = ("spade", "\u2660", "\u2664")


class Card:
    def __init__(self, color: Color, value: Value):
        self.color = color
        self.value = value

    def __str__(self):
        return self.string_value()

    def string_value(self, only_icon: bool = True, use_black: bool = True, only_symbol: bool = True,
                     sep: str = '') -> str:
        return self.value.string_value(only_symbol) + sep + self.color.string_value(only_icon, use_black)

    def verbose_string(self) -> str:
        return self.string_value(False, False, False, " of ")
