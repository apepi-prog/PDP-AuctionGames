from shutil import register_unpack_format
from main.python.engine.Player import Player
from main.python.engine.Action import IntEnum, Action
from main.python.engine.Card import *
from main.python.player.HumanPlayer import HumanPlayer

import sys
import io
import unittest

class TestHuman(unittest.TestCase):

    def setUp(self) -> None:
        self.player = HumanPlayer("test_player")

        return super().setUp()

    def test_instance_of_human_player(self):
        """BEHAVIOR: Success"""
        self.assertIsInstance(self.player, HumanPlayer)
    
    def test_valid_corresponding_type_of_init_argv_of_human_player(self):
        """BEHAVIOR: Success"""
        self.assertIsInstance(self.player.name, str)
    
    def test_invalid_corresponding_type_of_init_argv_of_human_player(self):
        """BEHAVIOR: Fail"""
        self.assertIsInstance(HumanPlayer(666).name, str) 
        self.assertIsInstance(HumanPlayer(6.6).name, str) 

    def test_init_value_of_human_player(self):
        """BEHAVIOR: Success"""
        self.assertMultiLineEqual("humain", self.player.type)
        self.assertEqual(0, self.player.money)
        self.assertEqual(0, self.player.min_bet)
        self.assertEqual(0, self.player.max_bet)
        self.assertEqual(0, self.player.bet)
        self.assertListEqual([], self.player.cards)

    def test_string_cast_of_human_player(self):
        """BEHAVIOR: Success"""
        self.assertMultiLineEqual('Human Player "test_player"', str(self.player))


    """Testing the next_action() function need to be made manualy for the input"""


    def test_notify_game_start_to_human_player(self):
        """BEHAVIOR: Success"""
        min_bet_val = 8
        max_bet_val = 50
        money_val = 100
        
        self.player.notify_game_start(min_bet_val, max_bet_val, 1, money_val)
        self.assertEqual(min_bet_val, self.player.min_bet)
        self.assertEqual(max_bet_val, self.player.max_bet)
        self.assertEqual(money_val, self.player.money)
        self.assertEqual(0, self.player.bet)
        self.assertListEqual([], self.player.cards)

    def test_notify_new_card(self):
        """BEHAVIOR: Success"""
        self.assertListEqual([], self.player.cards)
        card1 = Card(Color.CLUB, Value.ACE)
        self.assertNotIn(card1, self.player.cards)
        
        self.player.notify_new_card(card1)
        self.assertIn(card1, self.player.cards)
        self.assertEqual(1, len(self.player.cards))
    
    def test_get_bet_human_player_without_enough_money(self):
        """BEHAVIOR: Success"""
        self.player.money = 5
        self.player.min_bet = 10
        
        suppress_text = io.StringIO()   
        sys.stdout = suppress_text #to suppress the print output of the get_bet()
        self.assertEqual(-1, self.player.get_bet())
        sys.stdout = sys.__stdout__ #restor the output

if __name__ == '__main__':
    print("Resume should be equal = ...F.... | FAILED (failures=1)")
    unittest.main()