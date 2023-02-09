from typing import List
from main.python.engine.Action import Action
from main.python.engine.Card import Card
from main.python.engine.Deck import Deck
from main.python.engine.Player import Player
from main.python.engine.Utils import card_scores
from main.python.engine.Utils import compute_score

class AIPlayerHiloNoCount(Player):
    
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "ia-hilo-nocount"
        self.full_deck = Deck(0)
        self.money = 0
        self.min_bet = 0
        self.max_bet = 0
        self.cards_in_hand = []

    def __str__(self):
        return "AI Player Hi-Lo NoCount"

    def compute_hilo_score(self, card: Card) -> int:
        score = 0
        card_array = [card]
        value = compute_score(card_array)
        if value >= 1 and value <= 6:
            score += 1
        if value == 10 or value == 11:
            score -= 1
        return score

    def get_bet(self) -> int:
        bet = (self.min_bet * self.money) / self.max_bet
        if bet > self.max_bet:
            bet = self.max_bet
        if bet < self.min_bet:
            bet = self.min_bet
        return int(bet)

    def notify_game_start(self, min_bet: int, max_bet: int, deck_id: int, money: int) -> None:
        self.money = money
        self.min_bet = min_bet
        self.max_bet = max_bet

    def notify_game_end(self, win_status: int, money_earned: int) -> None:
        self.cards_in_hand.clear()

    def notify_new_card(self, card: Card) -> None:
        self.cards_in_hand.append(card)

    def notify_new_bud_card(self, card: Card) -> None:
        pass

    def notify_new_dealer_card(self, card: Card, is_before_refill) -> None:
        pass
            
    def notify_deck_refill(self) -> None:
        pass

    def next_action(self) -> Action:
        threshold = 0.5
        hand_value = 0

        for current_card in self.cards_in_hand:
            hand_value += self.compute_hilo_score(current_card)

        hand_value_norm = hand_value / len(self.cards_in_hand)

        if hand_value_norm > threshold:
            return Action.HIT

        return Action.STAND
