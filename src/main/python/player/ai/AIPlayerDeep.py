from typing import List
from main.python.engine.Action import Action
from main.python.engine.Card import Card
from main.python.engine.Deck import Deck
from main.python.engine.Player import Player
from main.python.engine.Utils import card_scores
from main.python.engine.Utils import compute_score
import matplotlib.pyplot as plt

import pandas as panda
import numpy as np
import os
## to remove warnings and messages by tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import logging
logging.getLogger("tensorflow").disabled = True
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import SGD 

class AIPlayerDeep(Player):

    def __init__(self, name: str):
        super().__init__(name)
        self.type = "ia-deep"
        self.full_deck = Deck(0)
        self.ai_hand_cards = []
        self.money = 0
        self.ai_min_bet = 0
        self.ai_max_bet = 0
        self.deck_is_refill = False
        self.current_deck_index = 0
        self.other_player_cards = []
        self.network = self.init_neural_network()
        self.train_neural_network(self.network)

    def __str__(self):
        return "AI Player DeepLearning"

    def get_bet(self) -> int:
        bet = self.ai_min_bet
        return int(bet) 

    def notify_game_start(self, min_bet: int, max_bet: int, deck_id: int, money: int) -> None:
        self.current_deck_index = deck_id
        self.deck_is_refill = False
        self.ai_hand_cards.clear() 
        self.money = money
        self.ai_min_bet = min_bet
        self.ai_max_bet = max_bet
        self.other_player_cards = []

    def notify_game_end(self, win_status: int, money_earned: int) -> None:
        self.other_player_cards.clear()

    def notify_new_card(self, card: Card) -> None:
        self.ai_hand_cards.append(card)

    def notify_new_bud_card(self, card: Card) -> None:
        pass

    def notify_new_dealer_card(self, card: Card, is_before_refill) -> None:
        self.other_player_cards.append(card)
            
    def notify_deck_refill(self) -> None:
        pass

    def next_action(self) -> Action:
        action = None

        ##init and training of our model 
        neural_network = self.network

        ##to predict we want a vector of size 2 with: 
        ## [SUM_OF_CARDS, DEALER_CARDS(only the one we can see)]
        sum_cards = compute_score(self.ai_hand_cards)
        sum_dealer = compute_score(self.other_player_cards)
        X_values = [sum_cards, sum_dealer]
        X_values = np.array([X_values])
        
        #prediction of our network
        predictions = neural_network.predict(X_values)
        indice = 0
        p = predictions[0][indice]
        #we found in the Y_vector the highest probability and the indice associated
        for i in range(4):
            if predictions[0][i] > p:
                p = predictions[0][i]
                indice = i

        #we deduce the correspondant action
        if indice + 1 == 1:
            action = Action.HIT
        if indice + 1 == 2:
            action = Action.STAND
        if indice + 1 == 3:
            action = Action.DOUBLE
        if indice + 1 == 4:
            action = Action.SURRENDER
        
        return action
    
    ##
    # Function to compute sum of cards (written in string and not in object Card)
    ##
    def compute_sum_cards(self, cards_list, heads):
        sum_cards = 0
        first_two_cards = 0
        for card in cards_list:
            if first_two_cards < 2:
                if card in heads:
                    if card != 'A':
                        sum_cards += 10
                    else:
                        sum_cards += 11
                else:
                    sum_cards += int(card)
                first_two_cards += 1
        return sum_cards
    
    ##
    # Function to create a training set for our AI
    ##
    def generate_training_set(self, data, start, end):
        #we got each coolumns of our data
        columns = data.columns
        
        ## cards with specific values
        heads = ['T', 'J', 'Q', 'K', 'A']

        #Establishing X dataset 
        X_train = []
        Y_train = []
        for row in range(start, end):
            x = []
            for c in columns:
                if c != "type" and c != "result":
                    if c == "cards":
                        cards = data.loc[row].at["cards"]
                        x.append(self.compute_sum_cards(cards, heads))
                    elif c == "dealer-cards":
                        cards = str(data.loc[row].at["dealer-cards"])
                        dealer_sum = 0
                        if cards[0] in heads:
                            if cards[0] == 'A':
                                dealer_sum = 11
                            else:
                                dealer_sum = 10
                            x.append(dealer_sum)
                        else:
                            x.append(int(cards[0]))
                    #reduction of dimension to 2 only
                    #else:
                    #    x.append(data.loc[row].at[c])
            X_train.append(x)
            # the format of Y are like this [0, 0, 0, 0] where each indice refer to action
            # example : [1, 0, 0, 0] means HIT
            # Now establishing Y dataset

            nb_cards = len(data.loc[row].at["cards"])
            ## case to surrender if we cant bet any money
            if data.loc[row].at["money"] == 0 or data.loc[row].at["money"] < data.loc[row].at["min-bet"]:
                Y_train.append([0, 0, 0, 1])
            ## we are able to win something
            if data.loc[row].at["result"] > 0:
                if int(data.loc[row].at["result"]) == 2*int(data.loc[row].at["bet"]):
                    if self.money >= 2*self.get_bet():
                        ## we can double our bet
                        Y_train.append([0, 0, 1, 0])
                else:
                    if nb_cards == 2:
                        Y_train.append([0, 1, 0, 0])
                    else:
                        Y_train.append([1, 0, 0, 0])
            else:
                Y_train.append([0, 0, 0, 1])
        return X_train, Y_train

    ##
    # Function to create a test set for our IA
    ##
    def generate_test_set(self, data, start, end):
        X_test, Y_test = self.generate_training_set(data, start, end)
        return X_test, Y_test

    ##
    # Function to init the neural network
    ##
    def init_neural_network(self):
        #number of actions is the number of classes so it's 4
        # Each class correspond to one action (HIT (0), STAND(1), DOUBLE(2) or SURRENDER(3))
        nb_classes = 4

        ## init the model
        model = Sequential()

        ## flattening the data
        model.add(Flatten())

        #first dense layer
        model.add(Dense(128))
        model.add(Activation('relu'))

        #dense layer
        model.add(Dense(64))
        model.add(Activation('relu'))

        model.add(Dense(32))
        model.add(Activation('relu'))
    
        #outside layer of the network
        model.add(Dense(nb_classes)) 
        model.add(Activation('softmax'))

        #compiling
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        return model
    
    ##
    # Function to read the csv file, and train our network
    ##
    def train_neural_network(self, network):
        ## reading the csv file
        actual_dir = os.getcwd()

        ## to modify with directory generated instead of resources
        ##csv_dir = actual_dir+"/main/resources/stat-exemple.csv"
        csv_dir = actual_dir + "/generated/result.csv"
        data = panda.read_csv(csv_dir)

        shuffled = data.sample(frac=1)
        shuffled.to_csv(csv_dir, index=False)
        data = panda.read_csv(csv_dir)

        ##number of rows in the csv file
        nb_rows = len(data.index)

        ## 85% for training
        X_train, Y_train = self.generate_training_set(data, 0, round(nb_rows*85/100))

        #15% for testing
        X_test, Y_test = self.generate_test_set(data, round(nb_rows*85/100), nb_rows)

        ## we need np array to fit the model 
        X_train = np.asarray(X_train)
        Y_train = np.asarray(Y_train)
        X_test = np.asarray(X_test)
        Y_test = np.asarray(Y_test)

        #training (add verbose=0 to disable on terminal each epoch during fiting)
        history = network.fit(X_train, Y_train, epochs=256, batch_size=64, verbose=0)

