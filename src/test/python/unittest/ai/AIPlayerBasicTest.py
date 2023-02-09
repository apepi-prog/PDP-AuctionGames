from audioop import add
from xmlrpc.client import Boolean
from main.python.engine.Engine import Engine
from main.python.player.ai.AIPlayerBasic import AIPlayerBasic
from main.python.engine.Card import Color
from main.python.engine.Card import Value
from main.python.engine.Card import Card
from main.python.engine.Action import Action


import unittest
import sys
import io

class TestAIPlayerBasic(unittest.TestCase):

    def test_next_action_hit(self):
        """BEHAVIOR: Success"""
        player = AIPlayerBasic("AIBasic_test")
        
        # Set the correct scenario
        player.notify_new_dealer_card(Card(Color.HEART, Value.SIX), False) # 6♥
        player.notify_new_card(Card(Color.DIAMOND, Value.TEN)) #  10♦ 
        player.notify_new_card(Card(Color.HEART, Value.FOUR)) # 4♥

        returned_action = player.next_action()
        
        self.assertEqual(returned_action, Action.HIT)

    def test_next_action_double(self):
        """BEHAVIOR: Success"""
        player = AIPlayerBasic("AIBasic_test")
        
        # Set the correct scenario
        # Set the play before ...
        player.notify_new_dealer_card(Card(Color.HEART, Value.NINE), False) # 9♥
        player.notify_new_card(Card(Color.DIAMOND, Value.THREE)) #  3♦ 
        player.notify_new_card(Card(Color.HEART, Value.KING)) # K♥

        returned_action = player.next_action()
        
        self.assertEqual(returned_action, Action.DOUBLE)

    def test_next_action_stand(self):
        """BEHAVIOR: Success"""
        player = AIPlayerBasic("AIBasic_test")
        
        # Set the correct scenario
        player.notify_new_dealer_card(Card(Color.DIAMOND, Value.EIGHT), False) # 8♦
        player.notify_new_card(Card(Color.DIAMOND, Value.NINE)) #  9♦
        player.notify_new_card(Card(Color.CLUB, Value.QUEEN)) # Q♣

        returned_action = player.next_action()
        
        self.assertEqual(returned_action, Action.STAND)
    

if __name__ == '__main__':
    unittest.main()