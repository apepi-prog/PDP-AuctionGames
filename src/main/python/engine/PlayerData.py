from main.python.engine.Utils import Optional


class PlayerData:

    def __init__(self, money: int, time_limit: int):
        self.cards = []
        self.bet = Optional()
        self.money = money
        self.surrender = False
        self.eliminated = False
        self.time_limit = time_limit
        