from typing import List
from main.python.engine.Action import Action
from main.python.engine.Card import Card
from main.python.engine.Deck import Deck
from main.python.engine.Player import Player
from main.python.engine.Utils import card_scores
from main.python.engine.Utils import compute_score

class AIPlayerHilo(Player):
    
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "ia-hilo"
        self.full_deck = Deck(0)
        self.money = 0
        self.min_bet = 0
        self.max_bet = 0
        self.ai_my_bet = 0
        self.current_deck_index = 0
        self.cards_in_hand = []
        self.cards_in_play_quantity = 0
        self.cards_in_play_values = 0
        self.counted_cards_quantity = [0 for i in range(7)]
        self.counted_cards_values = [0 for i in range(7)]

    def __str__(self):
        return "AI Player Hi-Lo"

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
        bet = self.min_bet
        if self.counted_cards_quantity[self.current_deck_index] > 0:
            bet = (self.counted_cards_quantity[self.current_deck_index] * self.money) / len(self.full_deck.cards)
            if bet < self.min_bet:
                bet = self.min_bet
            elif bet > self.max_bet:
                bet = self.max_bet
        self.ai_my_bet = int(bet)
        return int(bet) 

    def notify_game_start(self, min_bet: int, max_bet: int, deck_id: int, money: int) -> None:
        self.current_deck_index = deck_id
        self.money = money
        self.min_bet = min_bet
        self.max_bet = max_bet

    def notify_game_end(self, win_status: int, money_earned: int) -> None:
        self.counted_cards_quantity[self.current_deck_index] += self.cards_in_play_quantity
        self.counted_cards_values[self.current_deck_index] += self.cards_in_play_values
        self.cards_in_play_quantity = 0
        self.cards_in_play_values = 0
        self.cards_in_hand.clear()

    def notify_new_card(self, card: Card) -> None:
        self.cards_in_hand.append(card)
        self.cards_in_play_quantity += 1
        self.cards_in_play_values += self.compute_hilo_score(card)

    def notify_new_bud_card(self, card: Card) -> None:
        self.cards_in_play_quantity += 1
        self.cards_in_play_values += self.compute_hilo_score(card)

    def notify_new_dealer_card(self, card: Card, is_before_refill) -> None:
        self.cards_in_play_quantity += 1
        self.cards_in_play_values += self.compute_hilo_score(card)
            
    def notify_deck_refill(self) -> None:
        self.counted_cards_quantity[self.current_deck_index] = 0
        self.counted_cards_values[self.current_deck_index] = 0

    def next_action(self) -> Action:
        threshold_positive = 0.5
        threshold_negative = -0.5
        hand_value = 0

        for current_card in self.cards_in_hand:
            hand_value += self.compute_hilo_score(current_card)

        hand_value_norm = hand_value / len(self.cards_in_hand)

        if hand_value_norm > threshold_positive:
            return Action.HIT

        if hand_value_norm < threshold_negative:
            return Action.STAND
        
        counted_cards_value_norm = (self.counted_cards_values[self.current_deck_index] + self.cards_in_play_values) / (self.counted_cards_quantity[self.current_deck_index] + self.cards_in_play_quantity)

        if (hand_value_norm >= threshold_negative and hand_value_norm < 0 and counted_cards_value_norm > threshold_positive) or (hand_value_norm <= threshold_positive and hand_value_norm > 0 and counted_cards_value_norm < threshold_negative):
            if self.ai_my_bet * 2 >= self.money: # if double is not possible 
                return Action.HIT
            else:
                return Action.DOUBLE
        
        return Action.STAND
