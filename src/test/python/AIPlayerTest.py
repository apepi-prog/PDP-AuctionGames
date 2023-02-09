from main.python.engine.Engine import Engine
from main.python.engine.DealerPlayer import DealerPlayer
from main.python.player.ai.AIPlayerBasic import AIPlayerBasic
from main.python.player.ai.AIPlayerHilo import AIPlayerHilo
from main.python.player.ai.AIPlayerHiloNoCount import AIPlayerHiloNoCount
from main.python.player.ai.AIPlayerDeep import AIPlayerDeep
from main.python.vue.TerminalVue import TerminalVue

# initialize player(s)

basic = AIPlayerBasic("JoueurAI-Basique-Test")
hilo = AIPlayerHilo("JoueurAI-HiLo-Test")
hilonc = AIPlayerHiloNoCount("JoueurAI-HiLoNoCount-Test")
deep = AIPlayerDeep("JoueurAI-DeepLearning-Test")

# initialize engine
engine = Engine(TerminalVue(), True, True)
engine.set_deck_amount(2)
engine.set_game_amount(500)

# Set bet interval
engine.set_min_bet(10)
engine.set_max_bet(100)

# Set the dealer of the game
engine.set_dealer(DealerPlayer("dealer"))

# Add players to the engine
engine.add_player(basic, 200, 5)
engine.add_player(hilo, 200, 5)
engine.add_player(hilonc, 200, 5)
engine.add_player(deep, 200, 5)

# Start the game
engine.run()
