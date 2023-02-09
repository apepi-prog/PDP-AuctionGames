import sys
import signal
from main.python.engine.Card import Value, Card


class Optional:
    def __init__(self, value=None):
        self.value = value
        self.present = False
        if self.value is not None:
            self.present = True

    def __str__(self):
        return f"value: {self.value}, present: {self.present}"

    def get_value(self):
        if self.present:
            return self.value
        else:
            raise RuntimeError("value is not set")

    def set_value(self, value):
        self.value = value
        self.present = True

    def is_present(self):
        return self.present


card_scores = {
    Value.ACE.symbol: [1, 11],
    Value.TWO.symbol: 2,
    Value.THREE.symbol: 3,
    Value.FOUR.symbol: 4,
    Value.FIVE.symbol: 5,
    Value.SIX.symbol: 6,
    Value.SEVEN.symbol: 7,
    Value.EIGHT.symbol: 8,
    Value.NINE.symbol: 9,
    Value.TEN.symbol: 10,
    Value.JACK.symbol: 10,
    Value.QUEEN.symbol: 10,
    Value.KING.symbol: 10,
}


def compute_score(cards: [Card]) -> int:
    score = 0
    aces = 0
    for card in cards:
        if card.value.symbol == Value.ACE.symbol:
            aces += 1
        else:
            score += card_scores[card.value.symbol]
    if aces > 0:
        if score + aces <= 11:  # score + 11 + (aces - 1) <= 21
            score += 10 + aces  # score += 11 + (aces - 1)
        else:
            score += aces
    return score


# from https://stackoverflow.com/questions/5574702
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# Code which permits to limit the execution time of a function call
# adapted from https://stackoverflow.com/questions/366682 (last access : 04/06/22)
def limited_call(seconds, function, *args):
    class TimeoutException(Exception):
        pass
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        result = function(*args)
        return False, result
    except TimeoutException:
        return True, None

