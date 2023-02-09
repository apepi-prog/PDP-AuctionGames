from audioop import add
from xmlrpc.client import Boolean
from main.python.engine.Engine import Engine
from main.python.engine.DealerPlayer import DealerPlayer
from main.python.player.HumanPlayer import HumanPlayer
from main.python.player.ai.AIPlayerBasic import AIPlayerBasic
from main.python.player.ai.AIPlayerDeep import AIPlayerDeep
from main.python.player.ai.AIPlayerHilo import AIPlayerHilo
from main.python.player.ai.AIPlayerHiloNoCount import AIPlayerHiloNoCount
from main.python.engine.PlayerData import PlayerData
from main.python.engine.Card import *
from main.python.vue.TerminalVue import TerminalVue

import unittest
import sys
import io

class TestEngine(unittest.TestCase):

    def setUp(self) -> None:
        self.engine = Engine(TerminalVue(), True, True)
        
        self.engine_set = Engine(TerminalVue(), True, True)
        self.engine_set.deck_amount = 2
        self.engine_set.game_amount = 30
        self.engine_set.min_bet.value = 10
        self.engine_set.min_bet.present = True
        self.engine_set.max_bet.value = 100
        self.engine_set.max_bet.present = True
        self.human = HumanPlayer("human_player")
        self.basic = AIPlayerBasic("JoueurAI-Basique-Test")
        self.hilo = AIPlayerHilo("JoueurAI-HiLo-Test")
        self.hilo_nc = AIPlayerHiloNoCount("JoueurAI-HiLoNoCount-Test")
        self.engine_set.dealer = DealerPlayer("dealer")
        self.engine_set.players.append(self.human)
        self.engine_set.players.append(self.basic)        
        self.engine_set.players.append(self.hilo)
        self.engine_set.players.append(self.hilo_nc)
        self.engine_set.players_data[self.human] = PlayerData(200, 5)
        self.engine_set.players_data[self.basic] = PlayerData(200, 5)
        self.engine_set.players_data[self.hilo] = PlayerData(200, 5)
        self.engine_set.players_data[self.hilo_nc] = PlayerData(200, 5)

        return super().setUp()

    def test_instance_of_engine(self):
        """BEHAVIOR: Success"""
        self.assertIsInstance(self.engine, Engine)
    
    def test_init_value_of_engine(self):
        """BEHAVIOR: Success"""
        vue_test = TerminalVue()
        engine_test1 = Engine(vue_test, False, False)
        engine_test2 = Engine(vue_test, True, False)
        engine_test3 = Engine(vue_test, False, True)

        self.assertListEqual([], self.engine.players)
        self.assertEqual({}, self.engine.players_data)
        self.assertEqual(None, self.engine.dealer)
        self.assertEqual(1, self.engine.game_amount)
        self.assertEqual(1, self.engine.deck_amount)
        self.assertTrue(self.engine.verbose)
        self.assertEqual(7, self.engine.LIMITED_TRY_NB)
        self.assertTrue(self.engine.has_limited_try)
        self.assertTrue(self.engine.has_limited_time)
        self.assertEqual(self.engine.min_bet.value, None)
        self.assertEqual(self.engine.max_bet.value, None)
        self.assertIsInstance(engine_test1.vue, TerminalVue)

        self.assertFalse(engine_test1.has_limited_try)
        self.assertFalse(engine_test1.has_limited_time)
        self.assertTrue(engine_test2.has_limited_try)
        self.assertFalse(engine_test2.has_limited_time)
        self.assertFalse(engine_test3.has_limited_try)
        self.assertTrue(engine_test3.has_limited_time)
    
    def test_add_player_in_engine(self):
        """BEHAVIOR: Success"""

        added_player = HumanPlayer("added_player")
        self.assertNotIn(added_player, self.engine.players)
        self.engine.add_player(added_player, 10, 5)
        self.assertIn(added_player, self.engine.players)

        #test try to add doublon player
        self.engine.add_player(added_player, 30, 5)
        self.assertEqual(1, len(self.engine.players))

    def test_add_player_in_engine_above_capacity(self):
        """BEHAVIOR: Failed"""

        added_player = HumanPlayer("added_player")
        for i in range(6):
            self.engine.players.append(HumanPlayer("player"+str(i)))     
        self.assertNotIn(added_player, self.engine.players)
        suppress_text = io.StringIO()   
        sys.stdout = suppress_text #to suppress the print output of the add_player()
        self.engine.add_player(added_player, 10, 5)
        sys.stdout = sys.__stdout__ #restor the output
        self.assertIn(added_player, self.engine.players)
    
    def test_set_dealer_in_engine(self):
        """BEHAVIOR: Success"""
        added_dealer = DealerPlayer("dealer")
        self.engine.set_dealer(added_dealer)
        self.assertEqual(self.engine.dealer, added_dealer)
    
    def test_set_valid_min_bet_in_engine(self):
        """BEHAVIOR: Success"""
        val = 1000
        
        #without max bet value
        self.engine.set_min_bet(val)
        self.assertEqual(self.engine.min_bet.value, val)
    
    def test_set_incoherent_min_bet_in_engine(self):
        """BEHAVIOR: Failed"""
        val = -5
        
        #respecting the positive value of min_bet
        self.engine.set_min_bet(val)
        self.assertEqual(self.engine.min_bet.value, val)
    
    def test_set_to_high_min_bet_in_engine(self):
        """BEHAVIOR: Failed""" 
        max_val = 100
        val = 300
        
        #ensure coherence with max_bet
        self.engine.max_bet.value = max_val
        self.engine.max_bet.present = True
        self.assertNotEqual(self.engine.max_bet.value, None)
        self.assertTrue(self.engine.max_bet.present)
        self.engine.set_min_bet(val)
        self.assertEqual(self.engine.min_bet.value, val)
    
    def test_set_valid_max_bet_in_engine(self):
        """BEHAVIOR: Success"""
        val = 1000
        
        #without min bet value
        self.engine.set_max_bet(val)
        self.assertEqual(self.engine.max_bet.value, val)
    
    def test_set_incoherent_max_bet_in_engine(self):
        """BEHAVIOR: Failed"""
        val = -5
        
        #respecting the positive value of max_bet
        self.engine.set_max_bet(val)
        self.assertEqual(self.engine.max_bet.value, val)
    
    def test_set_to_low_max_bet_in_engine(self):
        """BEHAVIOR: Failed""" 
        min_val = 100
        val = 50
        
        #ensure coherence with max_bet
        self.engine.min_bet.value = min_val
        self.engine.min_bet.present = True
        self.assertNotEqual(self.engine.min_bet.value, None)
        self.assertTrue(self.engine.min_bet.present)
        self.engine.set_max_bet(val)
        self.assertEqual(self.engine.max_bet.value, val)
    
    def test_set_valid_amout_of_deck_in_engine(self):
        """BEHAVIOR: Success"""
        
        for i in range(1,8):
            self.engine.set_deck_amount(i)
            self.assertEqual(self.engine.deck_amount, i)
    
    def test_set_to_high_amout_of_deck_in_engine(self):
        """BEHAVIOR: Failed"""

        val = 8
        self.engine.set_deck_amount(val)
        self.assertEqual(self.engine.deck_amount, val)
    
    def test_set_to_low_amout_of_deck_in_engine(self):
        """BEHAVIOR: Failed"""

        val = 0
        self.engine.set_deck_amount(val)
        self.assertEqual(self.engine.deck_amount, val)

    def test_set_valid_amout_of_game_in_engine(self):
        """BEHAVIOR: Success"""
        
        for i in range(1,500):
            self.engine.set_game_amount(i)
            self.assertEqual(self.engine.game_amount, i)
    
    def test_set_to_high_amout_of_game_in_engine(self):
        """BEHAVIOR: Failed"""

        val = 501
        self.engine.set_game_amount(val)
        self.assertEqual(self.engine.game_amount, val)
    
    def test_set_to_low_amout_of_game_in_engine(self):
        """BEHAVIOR: Failed"""

        val = 0
        self.engine.set_game_amount(val)
        self.assertEqual(self.engine.game_amount, val)

    def test_set_verbose_in_engine(self):
        """BEHAVIOR: Success"""

        self.engine.set_verbose(False) 
        self.assertFalse(self.engine.verbose)       
        self.engine.set_verbose(True) 
        self.assertTrue(self.engine.verbose) 

    def test_recover_other_player_cards(self):
        """BEHAVIOR: Success"""
        ref_cards = [Card(Color.HEART, Value.ACE), Card(Color.DIAMOND, Value.KING), Card(Color.CLUB, Value.TWO), Card(Color.DIAMOND, Value.QUEEN), Card(Color.HEART, Value.TEN), Card(Color.DIAMOND, Value.EIGHT), Card(Color.SPADE, Value.SIX), Card(Color.CLUB, Value.JACK)]      
        self.engine_set.players[0].cards.append(ref_cards[0])
        self.engine_set.players[0].cards.append(ref_cards[1])
        self.engine_set.players_data[self.human].cards.append(ref_cards[0])
        self.engine_set.players_data[self.human].cards.append(ref_cards[1])
        self.engine_set.players[1].ai_hand_cards.append(ref_cards[2])
        self.engine_set.players[1].ai_hand_cards.append(ref_cards[3])
        self.engine_set.players_data[self.basic].cards.append(ref_cards[2])
        self.engine_set.players_data[self.basic].cards.append(ref_cards[3])
        self.engine_set.players[2].cards_in_hand.append(ref_cards[4])
        self.engine_set.players[2].cards_in_hand.append(ref_cards[5])
        self.engine_set.players_data[self.hilo].cards.append(ref_cards[4])
        self.engine_set.players_data[self.hilo].cards.append(ref_cards[5])
        self.engine_set.players[3].cards_in_hand.append(ref_cards[6])
        self.engine_set.players[3].cards_in_hand.append(ref_cards[7])
        self.engine_set.players_data[self.hilo_nc].cards.append(ref_cards[6])
        self.engine_set.players_data[self.hilo_nc].cards.append(ref_cards[7])

        compare_card_human = [ref_cards[i] for i in range(2, 8)]
        compare_card_basic = [ref_cards[i] for i in range(0, 2)]+[ref_cards[j] for j in range(4, 8)]
        compare_card_hilo = [ref_cards[i] for i in range(0, 4)]+[ref_cards[j] for j in range(6, 8)]
        compare_card_hilo_nc = [ref_cards[i] for i in range(6)]

        self.assertListEqual(compare_card_human, self.engine_set.other_player_cards(self.human))
        self.assertEqual(len(set(compare_card_human)), len(set(self.engine_set.other_player_cards(self.human))))
        self.assertListEqual(compare_card_basic, self.engine_set.other_player_cards(self.basic))
        self.assertEqual(len(set(compare_card_basic)), len(set(self.engine_set.other_player_cards(self.basic))))
        self.assertListEqual(compare_card_hilo, self.engine_set.other_player_cards(self.hilo))
        self.assertEqual(len(set(compare_card_hilo)), len(set(self.engine_set.other_player_cards(self.hilo))))
        self.assertListEqual(compare_card_hilo_nc, self.engine_set.other_player_cards(self.hilo_nc))
        self.assertEqual(len(set(compare_card_hilo_nc)), len(set(self.engine_set.other_player_cards(self.hilo_nc))))


if __name__ == '__main__':
    print("Resume should be equal = .F....FFFFFFFF..... | FAILED (failures=9)")
    unittest.main()