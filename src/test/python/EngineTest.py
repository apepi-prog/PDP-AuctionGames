from main.python.engine.Engine import Engine
from main.python.engine.DealerPlayer import DealerPlayer
from main.python.player.HumanPlayer import HumanPlayer
from main.python.vue.TerminalVue import TerminalVue

# initialize player(s)

human = HumanPlayer("JoueurTest")

# initialize engine
engine = Engine(TerminalVue(), True, True)
engine.set_deck_amount(2)
engine.set_game_amount(3)

# Set bet interval
engine.set_min_bet(10)
engine.set_max_bet(100)

# Set the dealer of the game
engine.set_dealer(DealerPlayer("dealer"))

# Add players to the engine
engine.add_player(human, 200, 5)

# Start the game
engine.run()
