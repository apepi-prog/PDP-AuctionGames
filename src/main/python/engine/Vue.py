from main.python.engine.Card import Card
from main.python.engine.Player import Player
from main.python.engine.PlayerData import PlayerData


class Vue:

    def show_player_cards(self, name: str, cards: [Card]) -> None:
        """
        Show the cards of the player
        @param name: the name of the player
        @param cards: the cards of the player
        """
        pass

    def show_dealer_cards(self, cards: [Card]) -> None:
        """
        Show the cards of the dealer
        @param cards: the cards of the dealer
        """
        pass

    def show_in_game_board(self, players: [Player], player_datas: [PlayerData], dealer_card: Card) -> None:
        """
        Show the board during the game
        @param players: the list of players in the game
        @param player_datas: the list of data of the players in the game
        @param dealer_card: the visible card of the dealer
        """
        pass

    def show_player_result(self, player: Player, player_data: PlayerData, win_status: int, money_earned: int) -> None:
        """
        Show the result of the game for a player
        @param player: the player to show the result
        @param player_data: the data of the player
        @param win_status: the win status of the player (<0=lose, 0=draw, >0=win)
        @param money_earned: the amount of money earned at the end of the game
        """
        pass

    def show_end_stats(self, players: [Player], player_datas: [PlayerData]) -> None:
        """
        Show the stats at the end of all the games
        @param players: the list of players
        @param player_datas: the list of data of the players
        """
        pass
