from typing import List
from main.python.engine.Action import Action
from main.python.engine.Card import Card
from main.python.engine.Deck import Deck
from main.python.engine.Player import Player
from main.python.engine.Utils import card_scores
from main.python.engine.Utils import compute_score

class AIPlayerBasic(Player):

    """
    Dictionnary which store played cards to count it, for each deck
    deck index is the line index and each line is an array of the played cards for this deck
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "ai-basique"
        self.counted_cards_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        self.full_deck = Deck(0)
        self.money = 0
        self.ai_min_bet = 0
        self.ai_max_bet = 0
        self.ai_my_bet = 0
        self.deck_is_refill = False
        self.current_deck_index = 0
        self.other_player_cards = []
        self.ai_hand_cards = []

    def __str__(self) -> str:
        return "AI Player basique"

    def get_bet(self) -> int:
        bet = self.ai_min_bet
        if len(self.counted_cards_dict[self.current_deck_index]) > 0:
            bet = (len(self.counted_cards_dict[self.current_deck_index]) * self.money) / len(self.full_deck.cards)
            if bet < self.ai_min_bet:
                bet = self.ai_min_bet
            elif bet > self.ai_max_bet:
                bet = self.ai_max_bet
        self.ai_my_bet = int(bet)
        return int(bet) 

    def notify_game_start(self, min_bet: int, max_bet: int, deck_id: int, money: int) -> None:
        self.current_deck_index = deck_id
        self.deck_is_refill = False
        self.money = money
        self.ai_min_bet = min_bet
        self.ai_max_bet = max_bet
        

    def notify_game_end(self, win_status: int, money_earned: int) -> None:
        self.ai_hand_cards.clear() 
        self.other_player_cards.clear() 

    def notify_new_card(self, card: Card) -> None:
        self.ai_hand_cards.append(card)
        self.counted_cards_dict[self.current_deck_index].append(card)

    def notify_new_bud_card(self, card: Card) -> None:
        self.other_player_cards.append(card)
        self.counted_cards_dict[self.current_deck_index].append(card)

    def notify_new_dealer_card(self, card: Card, is_before_refill) -> None:
        self.other_player_cards.append(card)
        self.counted_cards_dict[self.current_deck_index].append(card)
            
    def notify_deck_refill(self) -> None:
        self.counted_cards_dict[self.current_deck_index].clear()

        for c in self.ai_hand_cards:
            self.counted_cards_dict[self.current_deck_index].append(c)
        for c in self.other_player_cards:
            self.counted_cards_dict[self.current_deck_index].append(c)

        self.deck_is_refill = True

    def next_action(self) -> Action:
        threshold_high = 0.5
        threshold_low = 0.08

        card_group_counter = [0, 0, 0, 0]
        
        # Compute player hand value
        value_sum = compute_score(self.ai_hand_cards)

        if value_sum <= 17:
            wanted_card_value = 21 - value_sum

            for current_card in self.full_deck.cards:
                is_in = False
                for c in self.counted_cards_dict[self.current_deck_index]:
                    if(c.color == current_card.color and c.value == current_card.value):
                        is_in = True

                # Count number of card with the same value 
                if not is_in:
                    for i in range(0, 4):
                        if card_scores[current_card.value.symbol] == wanted_card_value - i:
                            card_group_counter[i] += 1

            maximum_card_group_counter = max(card_group_counter)

            # Compute the maximum probability
            card_hit_probability = maximum_card_group_counter / (len(self.full_deck.cards) - len(self.counted_cards_dict[self.current_deck_index]))

            # Decide the correct action according to probability
            if card_hit_probability >= threshold_high:
                if self.ai_my_bet * 2 >= self.money: # if double is not possible 
                    return Action.HIT
                else:
                    return Action.DOUBLE

            elif card_hit_probability >= threshold_low:
                return Action.HIT

        return Action.STAND
