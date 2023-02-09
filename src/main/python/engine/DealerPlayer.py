from main.python.engine.Player import Player
from main.python.engine.Action import Action
from main.python.engine.Card import *
from main.python.engine.Engine import compute_score


class DealerPlayer(Player):

    def __init__(self, name: str):
        super().__init__(name)
        self.cards = []

    def notify_game_start(self, min_bet: int, max_bet: int, deck_id: int, money: int) -> None:
        self.cards = []

    def notify_new_card(self, card: Card) -> None:
        self.cards.append(card)

    def next_action(self) -> Action:
        """The action of the dealer is always HIT if its score is below 17, else the action is STAND."""
        # dealer plays (dealer must HIT if its score < 16 and STAND if its score >= 17)
        score = compute_score(self.cards)
        if score <= 16:
            return Action.HIT
        else:
            return Action.STAND

    def get_bet(self) -> int:
        """"The dealer don't have a bet."""
        return 0

