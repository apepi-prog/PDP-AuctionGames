from main.python.engine.Card import *
import random


class Deck:

    MAX_SIZE = 52

    def __init__(self, deck_id: int):
        self.deck_id = deck_id
        self.cards = []
        self.discarded = []
        for color in Color:
            for val in Value:
                self.cards.append(Card(color, val))

    def shuffle(self) -> None:
        """Shuffle the deck of cards"""
        random.shuffle(self.cards)

    def pop(self) -> Card:
        """Retrieve one card from the deck. If there is no card return nothing"""
        return self.cards.pop()

    def refill(self) -> None:
        """Refill a deck. Put back the discarded cards in the deck. The deck is shuffled and the end of the operation."""
        for card in self.discarded:
            self.cards.append(card)
        self.discarded.clear()
        self.shuffle()
        
    def size(self) -> int:
        """Retrieve the size of the deck. AKA the amount of remaining cards"""
        return len(self.cards)

    def is_empty(self) -> bool:
        """Determine if the deck is empty."""
        return self.size() == 0

    def discard(self, cards) -> None:
        for card in cards:
            self.discarded.append(card)

