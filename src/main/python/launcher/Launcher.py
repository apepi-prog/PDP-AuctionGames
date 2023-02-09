import sys
from textwrap import dedent
from typing import Dict, List, Union

from main.python.engine.DealerPlayer import DealerPlayer
from main.python.engine.Engine import Engine
from main.python.engine.Utils import eprint
from main.python.player.HumanPlayer import HumanPlayer
from main.python.player.ai.AIPlayerDeep import AIPlayerDeep
from main.python.player.ai.AIPlayerBasic import AIPlayerBasic
from main.python.player.ai.AIPlayerHilo import AIPlayerHilo
from main.python.player.ai.AIPlayerHiloNoCount import AIPlayerHiloNoCount
from main.python.vue.TerminalVue import TerminalVue


def player_from_type(ptype: str):
    if ptype == "humain":
        return HumanPlayer, 60
    elif ptype == "ia-basique":
        return AIPlayerBasic, 10
    elif ptype == "ia-hilo":
        return AIPlayerHilo, 10
    elif ptype == "ia-hilo-nocount":
        return AIPlayerHiloNoCount, 10
    elif ptype == "ia-deep":
        return AIPlayerDeep, 20
    else:
        return None, 0


ARG_PLAYER = "--joueurs"
ARG_PLAYER_SHORT = "-j"
ARG_MONEY = "--argent"
ARG_MONEY_SHORT = "-a"
ARG_GAME_AMOUNT = "--parties"
ARG_GAME_AMOUNT_SHORT = "-p"
ARG_BET_MIN = "--mise-min"
ARG_BET_MIN_SHORT = "-mn"
ARG_BET_MAX = "--mise-max"
ARG_BET_MAX_SHORT = "-mx"
ARG_DECK_AMOUNT = "--paquets"
ARG_DECK_AMOUNT_SHORT = "-d"
ARG_VERBOSE = "--verbose"
ARG_VERBOSE_SHORT = "-v"
ARG_FILE = "--fichier"
ARG_FILE_SHORT = "-f"
ARG_HELP = "--help"
ARG_HELP_SHORT = "-h"

valid_arg_names: List[str] = [ARG_PLAYER, ARG_MONEY, ARG_GAME_AMOUNT, ARG_BET_MIN, ARG_BET_MAX, ARG_DECK_AMOUNT,
                              ARG_VERBOSE, ARG_FILE, ARG_HELP, ARG_PLAYER_SHORT, ARG_MONEY_SHORT,
                              ARG_GAME_AMOUNT_SHORT, ARG_BET_MIN_SHORT, ARG_BET_MAX_SHORT, ARG_DECK_AMOUNT_SHORT,
                              ARG_VERBOSE_SHORT, ARG_FILE_SHORT, ARG_HELP_SHORT]

user_args = sys.argv[1:]

valid_args: Dict[str, List[str]] = {}
invalid_args: Dict[str, List[str]] = {}

# Store arguments in a dictionary
name = "invalid"
valid_args[name] = []
for arg in user_args:
    if arg.startswith("-"):
        name = arg
        valid_args[name] = []
    else:
        valid_args[name].append(arg)

# Remove invalid arguments
invalid_keys = []
for key in valid_args.keys():
    if key not in valid_arg_names:
        invalid_keys.append(key)
for element in invalid_keys:
    invalid_args[element] = valid_args[element]
    del valid_args[element]

if (ARG_HELP in valid_args) or (ARG_HELP_SHORT in valid_args) or len(user_args) == 0:
    print(dedent(
        f"""\
        Un programme pour lancer des parties de blackjack.
        Usage:
          {ARG_HELP_SHORT},  {ARG_HELP}
             Affiche cette aide.
          {ARG_PLAYER_SHORT},  {ARG_PLAYER} {{humain|ia-basique|ia-hilo|ia-hilo-nocount|ia-deep}} [<nombre>] [{{humain|ia-basique|ia-hilo|ia-hilo-nocount|ia-deep}} [<nombre>] ...]
             Les types de joueurs à utiliser ainsi que le quantité.
          {ARG_MONEY_SHORT},  {ARG_MONEY} <nombre> [<nombre> ...]
             L'argent de départ de chaque joueurs. L'argent est donné aux joueurs dans l'ordre de {ARG_PLAYER}.
          {ARG_GAME_AMOUNT_SHORT},  {ARG_GAME_AMOUNT} <nombre>
             La quantité de parties à exécuter. Optionnel (défaut=1).
          {ARG_BET_MIN_SHORT}, {ARG_BET_MIN} <nombre>
             La mise minimum durant les parties. Optionnel (défaut=5).
          {ARG_BET_MAX_SHORT}, {ARG_BET_MAX} <nombre>
             La mise maximum durant les parties. Optionnel (défaut=100000).
          {ARG_DECK_AMOUNT_SHORT},  {ARG_DECK_AMOUNT} <nombre>
             La quantité de paquets de cartes à utiliser. Optionnel (défaut=1).
          {ARG_VERBOSE_SHORT},  {ARG_VERBOSE}
             Tout les textes sont affichés. Optionnel (défaut=seulement les résultats des parties sont affichés).
          {ARG_FILE_SHORT},  {ARG_FILE} <chemin/vers/fichier>
             Le fichier à utiliser pour remplir les paramètres à la places des arguments de la ligne de commande. (Optionnel).
        """))
    exit()

# TODO: should we print invalid arguments to the user

# Replace arg with their short version if present
if ARG_PLAYER_SHORT in valid_args:
    ARG_PLAYER = ARG_PLAYER_SHORT
if ARG_MONEY_SHORT in valid_args:
    ARG_MONEY = ARG_MONEY_SHORT
if ARG_GAME_AMOUNT_SHORT in valid_args:
    ARG_GAME_AMOUNT = ARG_GAME_AMOUNT_SHORT
if ARG_BET_MIN_SHORT in valid_args:
    ARG_BET_MIN = ARG_BET_MIN_SHORT
if ARG_BET_MAX_SHORT in valid_args:
    ARG_BET_MAX = ARG_BET_MAX_SHORT
if ARG_DECK_AMOUNT_SHORT in valid_args:
    ARG_DECK_AMOUNT = ARG_DECK_AMOUNT_SHORT
if ARG_VERBOSE_SHORT in valid_args:
    ARG_VERBOSE = ARG_VERBOSE_SHORT
if ARG_FILE_SHORT in valid_args:
    ARG_FILE = ARG_FILE_SHORT

# Define parameters
players = []  # [[Player, int]]
game_amount = 1
min_bet = 5
max_bet = 100000
deck_amount = 1
verbose = False

if ARG_FILE in valid_args:
    # Compute file
    # TODO : read args from file
    pass
else:
    # No player in parameters
    if ARG_PLAYER not in valid_args:
        eprint("No player given.")
        exit(1)
    # No money in parameters
    if ARG_MONEY not in valid_args:
        eprint("No money given.")
        exit(1)
    # Compute players (<type> <amount>?)+
    size = len(valid_args[ARG_PLAYER])
    i = 0
    while i < size:
        player_type = valid_args[ARG_PLAYER][i]
        if player_type in ("humain", "ia-basique", "ia-hilo", "ia-hilo-nocount", "ia-deep"):
            next_element = valid_args[ARG_PLAYER][i + 1] if i + 1 < size else ""
            creator, time_limit = player_from_type(player_type)
            amount = 1
            if next_element.isdigit():
                amount = int(next_element)
                i += 1
            for j in range(amount):
                players.append([creator(player_type), 0, time_limit])
        else:
            eprint("invalid type: " + player_type)
        i += 1
    # Compute money <amount>+
    size = len(valid_args[ARG_MONEY])
    i = 0
    player_index = 0
    while i < size and player_index < len(players):
        value = valid_args[ARG_MONEY][i]
        if value.isdigit():
            amount = int(value)
            if 0 <= amount <= 100000:
                players[player_index][1] = int(value)
                player_index += 1
        i += 1
    if i != len(players):
        eprint(f"Not enough valid money amount: {i} valid for {len(players)} players")
        exit(1)
    # TODO : what about user giving too much money args ?
    # Compute games <amount>?
    if ARG_GAME_AMOUNT in valid_args and len(valid_args[ARG_GAME_AMOUNT]) > 0:
        value = valid_args[ARG_GAME_AMOUNT][0]
        if value.isdigit():
            amount = int(value)
            if 1 <= amount <= 500:
                game_amount = amount
    # Compute min/max bets <amount>?
    if ARG_BET_MIN in valid_args and len(valid_args[ARG_BET_MIN]) > 0:
        value = valid_args[ARG_BET_MIN][0]
        if value.isdigit():
            amount = int(value)
            if 5 <= amount <= 100000:
                min_bet = amount
    if ARG_BET_MAX in valid_args and len(valid_args[ARG_BET_MAX]) > 0:
        value = valid_args[ARG_BET_MAX][0]
        if value.isdigit():
            amount = int(value)
            if min_bet <= amount <= 100000:
                max_bet = amount
    # Compute decks <amount>?
    if ARG_DECK_AMOUNT in valid_args and len(valid_args[ARG_DECK_AMOUNT]) > 0:
        value = valid_args[ARG_DECK_AMOUNT][0]
        if value.isdigit():
            amount = int(value)
            if 1 <= amount <= 7:
                deck_amount = amount
    # Compute fast run
    if ARG_VERBOSE in valid_args:
        verbose = True

# Remove players with money < min_bet
players_to_remove = []
size = len(players)
i = 0
while i < size:
    if players[i][1] < min_bet:
        players_to_remove.append(i)
    i += 1
players_to_remove.reverse()
for index in players_to_remove:
    del players[index]

# Identify players
for i, element in enumerate(players):
    element[0].name = f"{element[0].name} {i+1}"

# Print params used
print(f"""
Paramètres de lancement:
  Joueurs : {[f"{str(elem[0])}:{str(elem[1])}" for elem in players]}
  Nombre de paquets : {deck_amount}
  Mises : [{min_bet}, {max_bet}]
  Nombre de parties : {game_amount}
  Verbeux : {"Oui" if verbose else "Non"}
""")

# Launch the engine

engine = Engine(TerminalVue(), True, True)

engine.set_min_bet(min_bet)
if max_bet is not None:
    engine.set_max_bet(max_bet)

for element in players:
    engine.add_player(element[0], element[1], element[2])

engine.set_dealer(DealerPlayer("Dealer"))

engine.set_game_amount(game_amount)
engine.set_deck_amount(deck_amount)
engine.set_verbose(verbose)

engine.run()
