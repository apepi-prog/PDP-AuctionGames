from main.python.engine.Player import Player
from main.python.engine.Action import Action
from main.python.engine.Card import *
from main.python.engine.Engine import compute_score
from main.python.engine.DealerPlayer import DealerPlayer

import random
import unittest

class TestDealer(unittest.TestCase):

    def setUp(self) -> None:
        self.dealer1 = DealerPlayer(Player("Dealer"))

        return super().setUp()

    def test_instance_of_dealer_player(self):
        """BEHAVIOR: Success"""
        self.assertIsInstance(self.dealer1, DealerPlayer)
        #pass the second assert test because of the non type langage
        #solution put an assert to confirm the type in the __init__
        self.assertIsInstance(DealerPlayer(Player(987)), DealerPlayer)
        self.assertIsInstance(DealerPlayer("Player"), DealerPlayer)
    
    def test_valid_corresponding_type_of_init_argv_of_dealer(self):
        """BEHAVIOR: Success"""
        self.assertIsInstance(self.dealer1.name, Player)
    
    def test_invalid_corresponding_type_of_init_argv_of_dealer(self):
        """BEHAVIOR: Fail"""
        self.assertIsInstance(DealerPlayer("Player").name, Player) 

    def test_init_value_of_dealer_player(self):
        """BEHAVIOR: Success"""
        self.assertListEqual([], self.dealer1.cards)

    def test_notify_game_start(self):
        """BEHAVIOR: Success"""
        self.assertListEqual([], self.dealer1.cards)

        self.dealer1.cards.append(Card(Color.HEART, Value.KING))
        self.dealer1.cards.append(Card(Color.SPADE, Value.ACE))
        self.assertNotEqual([], self.dealer1.cards)
        self.dealer1.notify_game_start(0, 0, random.randint(0, 6) , 0)
        self.assertListEqual([], self.dealer1.cards)
    
    def test_notify_new_card(self):
        """BEHAVIOR: Success"""
        self.assertListEqual([], self.dealer1.cards)
        card1 = Card(Color.SPADE, Value.ACE)
        self.assertNotIn(card1, self.dealer1.cards)
        
        self.dealer1.notify_new_card(card1)
        self.assertIn(card1, self.dealer1.cards)
        self.assertEqual(1, len(self.dealer1.cards))

    def test_next_action_dealer(self):
        """BEHAVIOR: Success"""

        #this test also inderectly test the compute_score function
        #test hit
        self.assertEqual(Action.HIT, self.dealer1.next_action()) #the dealer havec no cards yet
        self.dealer1.cards = [Card(Color.HEART, Value.ACE), Card(Color.SPADE, Value.ACE), Card(Color.DIAMOND, Value.ACE), Card(Color.CLUB, Value.ACE)] #test the good value choice of Ace
        self.assertEqual(Action.HIT, self.dealer1.next_action())
        self.dealer1.cards = [Card(Color.HEART, Value.KING), Card(Color.HEART, Value.SIX)]
        self.assertEqual(Action.HIT, self.dealer1.next_action())
        self.dealer1.cards = [Card(Color.HEART, Value.EIGHT), Card(Color.CLUB, Value.EIGHT)]
        self.assertEqual(Action.HIT, self.dealer1.next_action())
        self.dealer1.cards = [Card(Color.HEART, Value.EIGHT), Card(Color.CLUB, Value.FIVE)]
        self.assertEqual(Action.HIT, self.dealer1.next_action())
        self.dealer1.cards = [Card(Color.HEART, Value.TWO), Card(Color.CLUB, Value.THREE), Card(Color.CLUB, Value.FOUR), Card(Color.CLUB, Value.SEVEN)]
        self.assertEqual(Action.HIT, self.dealer1.next_action())
        
        #test stand
        self.dealer1.cards = [Card(Color.HEART, Value.KING), Card(Color.HEART, Value.ACE)] #blackjack hand
        self.assertEqual(Action.STAND, self.dealer1.next_action())
        self.dealer1.cards = [Card(Color.HEART, Value.TEN), Card(Color.HEART, Value.ACE)]   #blackjack hand  
        self.assertEqual(Action.STAND, self.dealer1.next_action())
        self.dealer1.cards = [Card(Color.HEART, Value.EIGHT), Card(Color.SPADE, Value.NINE)]
        self.assertEqual(Action.STAND, self.dealer1.next_action())
        self.dealer1.cards = [Card(Color.HEART, Value.JACK), Card(Color.HEART, Value.FIVE), Card(Color.CLUB, Value.THREE)]
        self.assertEqual(Action.STAND, self.dealer1.next_action())
        self.dealer1.cards = [Card(Color.HEART, Value.TEN), Card(Color.HEART, Value.SIX), Card(Color.CLUB, Value.QUEEN)]
        self.assertEqual(Action.STAND, self.dealer1.next_action())

if __name__ == '__main__':
    print("Resume should be equal = ..F.... | FAILED (failures=1)")
    unittest.main()