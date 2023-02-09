# PDP Auction Games 2022

Projet de Programmation M1 Informatique
Sujet : Jeux d'enchères

Membres du groupe : Nahaki Barry,  Mathias Crema, Maxime Dumonteil,  Nicolas Hubner,  Maxime Meyrat,  Alex Pepi

---

## Présentation l'application 

L'application qui a été développée pour ce projet avait pour but de permettre à un programme informatique (joueur IA) de jouer à un jeu d'enchères à information partielle. 

Nous avons choisi le Blackjack et avons donc développé cette application qui se compose de 3 grandes parties : 
* Le moteur de jeu (Engine)
* Le lanceur de moteur de jeu (Launcher)
* Les différents type de joueurs (humain ou IA)

Plus de détails dans le mémoire...

---

## Compilation du mémoire

Le script `compile_tex.sh` compile le fichier 0-memoire.tex actuellement présent dans le répertoire `docs/report` et permet donc de générer le pdf complet du mémoire.

Afin de compiler, vous aurez besoin de ces trois packages : 
`sudo apt install flex libfxt-dev texlive-latex-extra`

---

## Les packages python nécessaires

L'application utilise les packages pip3 :
* Numpy
* Tensorflow
* Keras
* Pandas

La commande pour les installer est la suivante :
`pip3 install numpy tensorflow keras pandas`

---

## Le lancement de l'application

L'application s'exécute à l'aide du script `run-launcher.sh` présent dans le répertoire `src`.

### Quelques exemples de commandes

#### Exemple n°1

`./run-launcher.sh -j humain ia-basique -a 10 20 -v` : lance une seule partie avec un joueur humain possèdant 10\$ en argent de départ et un jouer ia-basique débutant avec 20\$. 

#### Exemple n°2

`./run-launcher.sh -j humain 2 -a 100 200 -p 5 -mn 5 -mx 1000 -d 2 -v` : lance une cinq parties avec deux joueurs humain possèdant respectivement 100\$ et 200\$ en argent de départ et avec des mises comprisent entre 5 et 1000\$ ainsi que 2 paquets de cartes. 

#### Exemple n°3

`./run-launcher.sh -j ia-basique ia-hilo ia-hilo-nocount ia-deep -a 1000 1000 1000 1000 -p 50 -mn 5 -mx 50` : lance 50 parties avec des joueurs ia de tout type possèdant tous 1000\$ en argent de départ et avec des mises comprisent entre 5 et 50\$.

### La notice d'utilisation du launcher

Plus de détails ci-dessous sur les différents arguments utilisables.

```
Un programme pour lancer des parties de blackjack.
Usage:
  -h,  --help
     Affiche cette aide.
  -j,  --joueurs {humain|ia-basique|ia-hilo|ia-hilo-nocount|ia-deep} [<nombre>] [{humain|ia-basique|ia-hilo|ia-hilo-nocount|ia-deep} [<nombre>] ...]
     Les types de joueurs à utiliser ainsi que le quantité.
  -a,  --argent <nombre> [<nombre> ...]
     L'argent de départ de chaque joueurs. L'argent est donné aux joueurs dans l'ordre de --joueurs.
  -p,  --parties <nombre>
     La quantité de parties à exécuter. Optionnel (défaut=1).
  -mn, --mise-min <nombre>
     La mise minimum durant les parties. Optionnel (défaut=5).
  -mx, --mise-max <nombre>
     La mise maximum durant les parties. Optionnel (défaut=100000).
  -d,  --paquets <nombre>
     La quantité de paquets de cartes à utiliser. Optionnel (défaut=1).
  -v,  --verbose
     Tout les textes sont affichés. Optionnel (défaut=seulement les résultats des parties sont affichés).
  -f,  --fichier <chemin/vers/fichier>
     Le fichier à utiliser pour remplir les paramètres à la places des arguments de la ligne de commande. (Optionnel).
```

Note : L'option `-f` qui correspond à la lecture des arguments depuis un fichier JSON n'a pas été implémentée.

---

## Les tests

L'ensemble des fichiers de test se trouve dans le répertoire src/test/python
Afin de les lancer se placer au préalable dans le répertoire `src`.

Les fichiers de test "manuels" sont placés à la racine de ce répertoire et permettent la vérification du bon déroulement d'un partie

### Les tests pour les joueurs IA

Le fichier "AIPlayerTest.py" permet de lancer une partie à 4 joueurs, ces joueurs sont des joueurs IA avec pour chacun une stratégie différente.
Pour lancer ce test un script exécutable est disponible &rarr; "run-test-ai.sh":
`./run-test-ai.sh` or `bash run-test-ai.sh`

### Les tests pour le moteur de jeu

Le fichiers "EngineTest.py" permet de lancer une partie avec un joueur humain.
Pour lancer ce test un script exécutable est disponible -> "run-test.sh":
`./run-test.sh` or `bash run-test.sh`

Les tests unitaires des classes sont dans le répertoire `src/test/python/unittest`

Pour lancer tous les tests des classes de engine, sans compter la classe Engine, un script exécutable est disponible -> "run-unittest.sh":
`./run-unittest.sh` or `bash run-unittest.sh`

Pour lancer les tests unitaire de la classe Engine un script exécutable est disponnible -> "run-engine-unittest.sh":
`./run-engine-unittest.sh` or `bash run-engine-unittest.sh`

Pour lancer individuellement tous les fichiers de test unitaire -> "PYTHONPATH=. python3 "file_path/name_file.py"
Card : `PYTHONPATH=. python3 test/python/unittest/CardTest.py`
Deck : `PYTHONPATH=. python3 test/python/unittest/DeckTest.py`
Enum : `PYTHONPATH=. python3 test/python/unittest/EnumTest.py`
Utils : `PYTHONPATH=. python3 test/python/unittest/UtilsTest.py`
HumanPlayer :`PYTHONPATH=. python3 test/python/unittest/HumanPlayerTest.py`
DealerPlayer : `PYTHONPATH=. python3 test/python/unittest/DealerPlayerTest.py`
Engine : `PYTHONPATH=. python3 test/python/unittest/EngineTest.py`
