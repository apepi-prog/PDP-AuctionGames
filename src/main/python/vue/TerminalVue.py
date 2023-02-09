from textwrap import dedent

from main.python.engine.Card import Card
from main.python.engine.Player import Player
from main.python.engine.PlayerData import PlayerData
from main.python.engine.Utils import compute_score
from main.python.engine.Vue import Vue


class TerminalVue(Vue):

    def cards_to_string(self, cards: [Card]) -> str:
        string = ""
        for card in cards:
            string += f"{str(card)} "
        return string[:-1]

    def show_player_cards(self, name: str, cards: [Card]) -> None:
        print(f"Joueur \"{name}\" :\n  {self.cards_to_string(cards)} ({compute_score(cards)})")

    def show_dealer_cards(self, cards: [Card]) -> None:
        print(f"Croupier :\n  {self.cards_to_string(cards)} ({compute_score(cards)})")

    def show_in_game_board(self, players: [Player], player_datas: [PlayerData], dealer_card: Card) -> None:
        print("\n--------------- Table de jeu ---------------")
        for player in players:
            self.show_player_cards(player.name, player_datas[player].cards)
            print(f"  Mise: {player_datas[player].bet}$")
        print(f"Croupier :\n   {str(dealer_card)} ? ({compute_score([dealer_card])})")

    def show_player_result(self, player: Player, player_data: PlayerData, win_status: int, money_earned: int) -> None:
        print(dedent(
            f"""
            Résultat pour \"{player.name}\" :
              {self.cards_to_string(player_data.cards)} ({compute_score(player_data.cards)})
              {
            f"{player.name} a perdu {-money_earned}$" if win_status < 0 else
            f"{player.name} a fait une égalité" if win_status == 0 else
            f"{player.name} a gagné {money_earned}$"
            }
              {player.name} a {player_data.money}$
            """))

    def show_end_stats(self, players: [Player], player_datas: [PlayerData]) -> None:
        print("\nRésultat des parties :")
        for player in players:
            print(f"  {player.name} a {player_datas[player].money}$")
