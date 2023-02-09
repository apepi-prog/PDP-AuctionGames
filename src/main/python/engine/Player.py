from main.python.engine.Action import Action
from main.python.engine.Card import Card


class Player:

    def __init__(self, name: str):
        self.name = name
        self.type = None

    def notify_game_start(self, min_bet: int, max_bet: int, deck_id: int, money: int) -> None:
        """
        Called at the start of each game to notify the player of multiple parameters.
        @param min_bet: the minimum bet possible during this game
        @param max_bet: the maximum bet possible during this game
        @param deck_id: the deck id used
        @param money: the curent money of the player
        """
        pass

    def get_bet(self) -> int:
        """
        Returns the amounts of money the player bets for this game.
        """
        pass

    def notify_new_card(self, card: Card) -> None:
        """
        Called when a new card is given to the player (at the start of the game, or after an action).
        @param card: the new card
        """
        pass

    def notify_new_bud_card(self, card: Card) -> None:
        """
        Called when a new card is given to another player (at the start of the game, or after an action of another player).
        @param card: the new card
        """
        pass

    def notify_new_dealer_card(self, card: Card, is_before_refill) -> None:
        """
        Called when a new card is given to the dealer (at the start of the game, and at the end of the game).
        @param card: the new card
        @param is_before_refill: determine if the card was effectively given to the dealer before the deck was refilled
        """
        pass

    def notify_deck_refill(self) -> None:
        """
        Called when the deck is refiled (the discarded card are put back in the deck). The refill appends only when the deck is empty before taking a card from it.
        """
        pass

    def next_action(self) -> Action:
        """
        Return the next action of the player
        """
        pass

    def notify_game_end(self, win_status: int, money_earned: int) -> None:
        """
        Called at the end of the game to notify the player of the final board.
        @param win_status: the win status of the player at the end of the game (<0=lose, 0=draw, >0=win)
        @param money_earned: the money earned by the player at the end of the game
        """
        pass
