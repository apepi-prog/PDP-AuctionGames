from main.python.engine.Utils import *
from main.python.engine.Card import *
import unittest

class TestCard(unittest.TestCase):

    def setUp(self) -> None:
        self.void_opt = Optional()
        self.opt = Optional(10)

        return super().setUp()
    
    def test_is_instance_of_optional(self):
        """BEHAVIOR: Success"""
        self.assertIsInstance(self.opt, Optional)
        self.assertIsInstance(self.void_opt, Optional)
    
    def test_init_value_of_optional(self):
        """BEHAVIOR: Success"""
        self.assertEqual(self.opt.value, 10)
        self.assertEqual(self.void_opt.value, None)
        self.assertTrue(self.opt.present)
        self.assertFalse(self.void_opt.present)
    
    def test_string_cast_of_optional(self):
        """BEHAVIOR: Success"""
        self.assertMultiLineEqual(str(self.opt), "value: 10, present: True")
        self.assertMultiLineEqual(str(self.void_opt), "value: None, present: False")

    def test_get_value_of_optional(self):
        """BEHAVIOR: Success"""
        self.assertEqual(self.opt.get_value(), 10)
    
    def test_raise_exception_on_get_non_set_optional(self):
        """BEHAVIOR: Failed"""
        self.void_opt.get_value()

    def test_set_value_of_optional(self):
        """BEHAVIOR: Success"""
        val = 23
        self.void_opt.set_value(val)
        self.assertEqual(self.void_opt.value, val)
        self.assertTrue(self.void_opt.present)
    
    def test_is_present_optional(self):
        """BEHAVIOR: Success"""
        self.assertTrue(self.opt.is_present())
        self.assertFalse(self.void_opt.is_present())

    def test_compute_score_without_cards(self):
        """BEHAVIOR: Success"""
        cards = []
        self.assertEqual(compute_score(cards), 0)
    
    def test_compute_score_with_many_ace(self):
        """BEHAVIOR: Success"""
        cards1 = [Card(Color.HEART, Value.ACE), Card(Color.CLUB, Value.ACE),Card(Color.DIAMOND, Value.ACE), Card(Color.SPADE, Value.ACE)]
        cards2 = [Card(Color.CLUB, Value.ACE), Card(Color.DIAMOND, Value.ACE), Card(Color.SPADE, Value.ACE)]
        cards3 = [Card(Color.DIAMOND, Value.ACE), Card(Color.SPADE, Value.ACE)]
        cards4 = [Card(Color.SPADE, Value.ACE)]

        self.assertEqual(compute_score(cards1), 14)
        self.assertEqual(compute_score(cards2), 13)
        self.assertEqual(compute_score(cards3), 12)
        self.assertEqual(compute_score(cards4), 11)

    def test_compute_score(self):
        """BEHAVIOR: Success"""
        #the correct value of single card
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.ACE)]), 11)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.TWO)]), 2)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.THREE)]), 3)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.FOUR)]), 4)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.FIVE)]), 5)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.SIX)]), 6)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.SEVEN)]), 7)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.EIGHT)]), 8)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.NINE)]), 9)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.TEN)]), 10)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.JACK)]), 10)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.QUEEN)]), 10)
        self.assertEqual(compute_score([Card(Color.DIAMOND, Value.KING)]), 10)
        
        #blackjack
        self.assertEqual(compute_score([Card(Color.SPADE, Value.ACE), Card(Color.HEART, Value.KING)]), 21)
        self.assertEqual(compute_score([Card(Color.SPADE, Value.ACE), Card(Color.HEART, Value.QUEEN)]), 21)
        self.assertEqual(compute_score([Card(Color.SPADE, Value.ACE), Card(Color.HEART, Value.JACK)]), 21)
        self.assertEqual(compute_score([Card(Color.SPADE, Value.ACE), Card(Color.HEART, Value.TEN)]), 21)

        #combination cards
        self.assertEqual(compute_score([Card(Color.SPADE, Value.ACE), Card(Color.SPADE, Value.TWO), Card(Color.SPADE, Value.THREE)]), 16)
        self.assertEqual(compute_score([Card(Color.SPADE, Value.TWO), Card(Color.SPADE, Value.THREE)]), 5)
        self.assertEqual(compute_score([Card(Color.SPADE, Value.FOUR), Card(Color.SPADE, Value.FIVE), Card(Color.SPADE, Value.SIX)]), 15)
        self.assertEqual(compute_score([Card(Color.SPADE, Value.EIGHT), Card(Color.SPADE, Value.NINE), Card(Color.SPADE, Value.TEN)]), 27)
        self.assertEqual(compute_score([Card(Color.SPADE, Value.JACK), Card(Color.SPADE, Value.THREE), Card(Color.SPADE, Value.KING)]), 23)

if __name__ == '__main__':
    print("Resume should be equal = .......E.. | FAILED (errors=1)")
    unittest.main()