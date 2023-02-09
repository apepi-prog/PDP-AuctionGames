from audioop import add
from xmlrpc.client import Boolean
from main.python.engine.Engine import Engine
from main.python.player.ai.AIPlayerHilo import AIPlayerHilo
from main.python.engine.Card import Color
from main.python.engine.Card import Value
from main.python.engine.Card import Card
from main.python.engine.Action import Action


import unittest
import sys
import io

class TestAIPlayerHilo(unittest.TestCase):

    def test_next_action_hit(self):
        """BEHAVIOR: Success"""
        player = AIPlayerHilo("AIHilo_test")
        
        # Set the correct scenario
        player.notify_new_dealer_card(Card(Color.SPADE, Value.QUEEN), False) # Q♠
        player.notify_new_card(Card(Color.CLUB, Value.THREE)) #  3♣
        player.notify_new_card(Card(Color.DIAMOND, Value.FIVE)) # 5♦

        returned_action = player.next_action()
        
        self.assertEqual(returned_action, Action.HIT)

    def test_next_action_stand(self):
        """BEHAVIOR: Success"""
        player = AIPlayerHilo("AIHilo_test")
        
        # Set the correct scenario
        player.notify_new_dealer_card(Card(Color.HEART, Value.TWO), False) # 8♦
        player.notify_new_card(Card(Color.CLUB, Value.JACK)) # J♣
        player.notify_new_card(Card(Color.CLUB, Value.TEN)) # 10♣

        returned_action = player.next_action()
        
        self.assertEqual(returned_action, Action.STAND)
    

if __name__ == '__main__':
    unittest.main()