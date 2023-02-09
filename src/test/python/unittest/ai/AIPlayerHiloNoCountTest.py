from audioop import add
from xmlrpc.client import Boolean
from main.python.engine.Engine import Engine
from main.python.player.ai.AIPlayerHiloNoCount import AIPlayerHiloNoCount
from main.python.engine.Card import Color
from main.python.engine.Card import Value
from main.python.engine.Card import Card
from main.python.engine.Action import Action

import unittest
import sys
import io

class TestAIPlayerHiloNoCount(unittest.TestCase):

    def test_next_action_hit(self):
        """BEHAVIOR: Success"""
        player = AIPlayerHiloNoCount("AIHilo_test")
        
        # Set the correct scenario
        player.notify_new_dealer_card(Card(Color.DIAMOND, Value.TEN), False) # 10♦
        player.notify_new_card(Card(Color.CLUB, Value.FOUR)) #  4♣
        player.notify_new_card(Card(Color.SPADE, Value.TWO)) # 2♠

        returned_action = player.next_action()
        
        self.assertEqual(returned_action, Action.HIT)

    def test_next_action_stand(self):
        """BEHAVIOR: Success"""
        player = AIPlayerHiloNoCount("AIHilo_test")
        
        # Set the correct scenario
        player.notify_new_dealer_card(Card(Color.SPADE, Value.THREE), False) # 3♠
        player.notify_new_card(Card(Color.HEART, Value.JACK)) # J♥
        player.notify_new_card(Card(Color.CLUB, Value.KING)) # K♣

        returned_action = player.next_action()
        
        self.assertEqual(returned_action, Action.STAND)
    

if __name__ == '__main__':
    unittest.main()