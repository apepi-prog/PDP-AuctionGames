import csv
import os
from pathlib import Path
from random import shuffle

from main.python.engine.Action import Action
from main.python.engine.Card import Card
from main.python.engine.Deck import Deck
from main.python.engine.Player import Player
from main.python.engine.PlayerData import PlayerData
from main.python.engine.Utils import Optional, compute_score, eprint, limited_call
from main.python.engine.Vue import Vue


class Engine:
    """
    The engine of blackjack
    """

    def __init__(self, vue: Vue, has_limited_try: bool, has_limited_time: bool):
        self.players = []
        self.players_data = {}
        self.min_bet = Optional()
        self.max_bet = Optional()
        self.dealer = None
        self.game_amount = 1
        self.deck_amount = 1
        self.vue = vue
        self.verbose = True
        self.has_limited_try = has_limited_try
        self.LIMITED_TRY_NB = 7
        self.has_limited_time = has_limited_time

    def add_player(self, player: Player, money: int, time_limit: int) -> None:
        """Add a player to this game"""
        if len(self.players) < 6:
            if player not in self.players:
                self.players.append(player)
                self.players_data[player] = PlayerData(money, time_limit)
        else:
            print("Nombre de joueurs déjà maximal")

    def set_dealer(self, dealer: Player) -> None:
        self.dealer = dealer

    def set_min_bet(self, minimum: int) -> None:
        if minimum > 0 and (not self.max_bet.is_present() or minimum <= self.max_bet.get_value()):
            self.min_bet.set_value(minimum)

    def set_max_bet(self, maximum: int) -> None:
        if maximum > 0 and (not self.min_bet.is_present() or maximum >= self.min_bet.get_value()):
            self.max_bet.set_value(maximum)

    def set_game_amount(self, amount: int) -> None:
        if 1 < amount <= 500:
            self.game_amount = amount

    def set_deck_amount(self, amount: int) -> None:
        if 1 < amount <= 7:
            self.deck_amount = amount

    def set_verbose(self, verbose: bool) -> None:
        self.verbose = verbose

    def run(self) -> None:
        """run the game"""
        if not self.min_bet.is_present() or not self.max_bet.is_present():
            raise RuntimeError("Min bet or max bet is not set.")
        if self.dealer is None:
            raise RuntimeError("The dealer for the game has not been set.")
        if self.min_bet.get_value() > self.max_bet.get_value():
            raise RuntimeError("Max bet can't be less than min bet")
        if len(self.players) < 1:
            print("Pas assez de joueur pour la partie.")
        # initialize the engine
        decks = [Deck(i) for i in range(self.deck_amount)]
        shuffle(decks)
        used_deck = []
        removed_players = []
        for game_number in range(self.game_amount):
            # initialize the game
            for player in self.players:
                self.players_data[player].surrender = False
                if self.players_data[player].money < self.min_bet.get_value():
                    removed_players.append(player)
                    self.players.remove(player)
            if len(self.players) < 1:
                print("Pas assez de joueur pour la partie.")
                break
            if not decks:
                decks += used_deck
                shuffle(decks)
                used_deck.clear()
            deck = decks.pop()
            used_deck.append(deck)
            deck.shuffle()
            dealer_cards = []
            # notify players of the start of the game
            for player in self.players:
                player.notify_game_start(self.min_bet.get_value(), self.max_bet.get_value(), deck.deck_id, self.players_data[player].money)
            self.dealer.notify_game_start(0, 0, deck.deck_id, 0)
            # take the bets of each player
            for player in self.players:
                remove_player = False
                if self.players_data[player].money >= self.min_bet.get_value():
                    ask_remaining = self.LIMITED_TRY_NB
                    while ask_remaining > 0:
                        if self.has_limited_time:
                            if ask_remaining < 7:
                                eprint(f"Essais restants {ask_remaining}")
                            stopped, bet = limited_call(self.players_data[player].time_limit, player.get_bet)
                            if stopped:
                                bet = -1
                                eprint("Temps écoulé pour la demande de la mise")
                            ask_remaining -= 1
                        else:
                            bet = player.get_bet()
                        if self.min_bet.get_value() <= bet <= self.max_bet.get_value() and bet <= self.players_data[player].money:
                            self.players_data[player].bet = bet
                            ask_remaining = 0
                        elif ask_remaining == 0:  # the player returns a bet value which is not in the interval [min_bet,max_bet]
                            remove_player = True
                else:  # the player does not have the minimum bet required
                    remove_player = True
                if remove_player:
                    self.players.remove(player)
                    removed_players.append(player)
            # deal cards for each player
            for player in self.players:
                card, _ = self.pop_card(deck)
                self.players_data[player].cards.append(card)
                self.notify_new_card(player, card)
            dcard, refilled = self.pop_card(deck)
            dealer_cards.append(dcard)
            self.dealer.notify_new_card(dcard)
            for player in self.players:
                player.notify_new_dealer_card(dcard, not refilled)
            for player in self.players:
                card, _ = self.pop_card(deck)
                self.players_data[player].cards.append(card)
                self.notify_new_card(player, card)
            dcard, refilled = self.pop_card(deck)
            second_card_before_refill = not refilled
            dealer_cards.append(dcard)
            self.dealer.notify_new_card(dcard)
            # play for each player
            for player in self.players:
                is_playing = True
                while is_playing:
                    ask_remaining = self.LIMITED_TRY_NB
                    while ask_remaining > 0:
                        if self.verbose:
                            self.vue.show_in_game_board(self.players, self.players_data, dealer_cards[0])
                        if self.has_limited_time:
                            stopped, action = limited_call(self.players_data[player].time_limit, player.next_action)
                            if stopped:
                                action = Action.EMPTY
                                eprint("Temps écoulé pour la demande d'action")
                        else:
                            action = player.next_action()
                        if self.has_limited_try and ask_remaining < 7:
                            eprint(f"Essais restants {ask_remaining - 1}")
                        is_playing, ask_remaining = self.compute_action_result(action, player, deck, ask_remaining)
            for player in self.players:
                player.notify_new_dealer_card(dealer_cards[1], second_card_before_refill)
            is_playing = True
            while is_playing:
                action = self.dealer.next_action()
                if action == Action.HIT:
                    dcard, refilled = self.pop_card(deck)
                    dealer_cards.append(dcard)
                    self.dealer.notify_new_card(dcard)
                    for player in self.players:
                        player.notify_new_dealer_card(dcard, not refilled)
                else:
                    is_playing = False
            # compute game result
            for player in self.players:
                win_status, money_earned = self.compute_game_result(player, dealer_cards)
                self.save_result(player, money_earned, dealer_cards)
                self.players_data[player].money += money_earned
                player.notify_game_end(win_status, money_earned)
                if self.verbose:
                    self.vue.show_player_result(player, self.players_data[player], win_status, money_earned)
            if self.verbose:
                self.vue.show_dealer_cards(dealer_cards)
            # end of the game
            self.discard_cards(dealer_cards, deck)
        # end of the engine
        self.vue.show_end_stats(self.players + removed_players, self.players_data)

    def compute_action_result(self, action: Action, player: Player, deck: Deck, ask_remaining: int) -> (bool, int):
        """
        Return if the player can continue playing after this action
        As a side effect, it applies the action to the game and changes some attributes
        """
        if action == Action.HIT:
            card, _ = self.pop_card(deck)
            self.players_data[player].cards.append(card)
            self.notify_new_card(player, card)
            if compute_score(self.players_data[player].cards) > 21:
                return False, 0
            else:
                return True, 0
        elif action == Action.STAND:
            return False, 0
        elif action == Action.DOUBLE:
            if len(self.players_data[player].cards) == 2 and self.players_data[player].money >= 2 * self.players_data[player].bet:
                card, _ = self.pop_card(deck)
                self.players_data[player].cards.append(card)
                self.notify_new_card(player, card)
                self.players_data[player].bet += self.players_data[player].bet
                return False, 0
            elif ask_remaining - 1 if self.has_limited_try else ask_remaining > 0:
                return True, (ask_remaining - 1 if self.has_limited_try else ask_remaining)
            else:
                self.players_data[player].eliminated = True
                return False, 0
        elif action == Action.SURRENDER:
            self.players_data[player].surrender = True
            return False, 0
        else:
            if ask_remaining - 1 if self.has_limited_try else ask_remaining > 0:
                return True, (ask_remaining - 1 if self.has_limited_try else ask_remaining)
            else:
                self.players_data[player].eliminated = True
                return False, 0

    def other_player_cards(self, player):
        cards = []
        for other_player in self.players:
            if other_player is not player:
                cards += self.players_data[other_player].cards.copy()
        return cards

    def compute_game_result(self, player, dealer_cards) -> (int, int):
        """Compute the result of the game for a player. Return the win status of the player (<0=lose, 0=draw, >0=win) and the money earned."""
        dealer_score = compute_score(dealer_cards)

        # Player surrendered
        if self.players_data[player].surrender:
            return -1, -self.players_data[player].bet / 2

        score = self.compute_player_score(player)
        # Player burned or eliminated
        if score > 21 or self.players_data[player].eliminated:
            return -1, -self.players_data[player].bet

        player_blackjack = score == 21 and len(self.players_data[player].cards) == 2

        # Dealer has blackjack
        if dealer_score == 21 and len(dealer_cards) == 2:
            if player_blackjack:
                return 0, 0
            else:
                return -1, -self.players_data[player].bet

        # Dealer lost
        if dealer_score > 21:
            if player_blackjack:
                return 1, 1.5 * self.players_data[player].bet
            else:
                return 1, self.players_data[player].bet

        # Dealer didn't lose and doesn't have blackjack
        if score < dealer_score:
            return -1, -self.players_data[player].bet
        elif score == dealer_score:
            return 0, 0
        else:
            if player_blackjack:
                return 1, 1.5 * self.players_data[player].bet
            else:
                return 1, self.players_data[player].bet

    def compute_player_score(self, player: Player) -> int:
        return compute_score(self.players_data[player].cards)

    def discard_cards(self, dealer_cards, deck: Deck) -> None:
        deck.discard(dealer_cards)
        dealer_cards.clear()
        for player in self.players:
            deck.discard(self.players_data[player].cards)
            self.players_data[player].cards.clear()

    def pop_card(self, deck: Deck):
        refilled = False
        if deck.is_empty():
            deck.refill()
            refilled = True
            for player in self.players:
                player.notify_deck_refill()
        return deck.pop(), refilled

    def notify_new_card(self, current_player: Player, card: Card):
        current_player.notify_new_card(card)
        for player in self.players:
            if player is not current_player:
                player.notify_new_bud_card(card)

    def save_result(self, player: Player, money_earned: int, dealer_cards) -> None:
        def tostring(cards):
            val = ""
            for card in cards:
                if card.value.symbol == "10":
                    val += "T"
                else:
                    val += card.value.symbol
            return val

        Path("./generated").mkdir(exist_ok=True)
        with open("./generated/result.csv", "a+") as file:
            writer = csv.writer(file)
            if os.stat("./generated/result.csv").st_size == 0:
                writer.writerow(["type", "money", "bet", "cards", "result", "min-bet", "max-bet", "dealer-cards"])
            writer.writerow([player.type, self.players_data[player].money, self.players_data[player].bet,
                             tostring(self.players_data[player].cards), money_earned, self.min_bet.get_value(),
                             self.max_bet.get_value(), tostring(dealer_cards)])
