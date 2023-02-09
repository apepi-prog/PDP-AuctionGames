#!/bin/sh

# no args
PYTHONPATH=. python3 main/python/launcher/Launcher.py

# test --joueurs
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs mauvaistype
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs mauvaistype humain --argent 10 20 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain ia-basique --argent 10 20 # ok

# test --argent
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent -100
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 0 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 10000000000000000000
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent pasunnombre

# test --parties
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties -5
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 0
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 1 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 1000
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties pasunnombre

# test --mise-min
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min -5
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 0 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 2 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 100000000000000
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min pasunnombre

# test --mise-max
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max -5
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 0
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 2
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 1000 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 100000000000000
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max pasunnombre

# test --paquets
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 1000 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 1000 --paquets
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 1000 --paquets -5
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 1000 --paquets 0
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 1000 --paquets 2 # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 1000 --paquets 1000000000000
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 1000 --paquets pasunnombre

# test --verbose
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 1000 --paquets 2
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 1000 --paquets 2 --verbose # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --parties 2 --mise-min 10 --mise-max 1000 --paquets 2 --verbose witharg


# test --fichier

# test unrecognized arg
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --invalidarg # ok
PYTHONPATH=. python3 main/python/launcher/Launcher.py --joueurs humain --argent 100 --invalidarg witharg # ok

