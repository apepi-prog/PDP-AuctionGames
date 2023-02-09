from main.python.engine.Player import Player
from main.python.engine.Action import IntEnum, Action
from main.python.engine.Card import Card


class HumanPlayer(Player):

    def __init__(self, name: str):
        super().__init__(name)
        self.type = "humain"
        self.money = 0
        self.min_bet = 0
        self.max_bet = 0
        self.bet = 0
        self.cards = []

    def __str__(self):
        return f"Human Player \"{self.name}\""

    def next_action(self) -> Action:
        double_is_possible = len(self.cards) == 2 and self.money >= self.bet*2
        message = f"""
{self.name}
Veuillez entrer le code de l'action que vous souhaitez faire :
c - Tirer une carte
r - S'arrêter (rester)"""
        if double_is_possible:
            message += "\nd - Doubler sa mise (et recevoir une dernière carte)"
        message += "\na - Abandonner"
        print(message)
        code = input()
        if code == 'c':
            return Action.HIT
        elif code == 'r':
            return Action.STAND
        elif code == 'd' and double_is_possible:
            return Action.DOUBLE
        elif code == 'a':
            return Action.SURRENDER
        return Action.EMPTY

    def get_bet(self) -> int:
        if self.money < self.min_bet:
            print("Vous n'avez malheureusement pas la mise minimale requise...")
            return -1
        message = f"""
{self.name}
La mise minimale est : {self.min_bet}
La mise maximale est : {self.max_bet}
Vous avez : {self.money}
Veuillez entrer la mise que vous souhaitez mettre :"""
        print(message)
        try:
            bet = int(input())
            return bet
        except ValueError:
            return -1

    def notify_game_start(self, min_bet: int, max_bet: int, deck_id: int, money: int) -> None:
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.money = money
        self.bet = 0
        self.cards = []

    def notify_new_card(self, card: Card) -> None:
        self.cards.append(card)
