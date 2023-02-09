from main.python.engine.Card import Color
from main.python.engine.Card import Value
from main.python.engine.Card import Card
import unittest

class TestCard(unittest.TestCase):

    def setUp(self) -> None:
        self.cards = []
        for color in Color:
            for value in Value:
                self.cards.append(Card(color, value))
                    
        self.cardA = []
        for color in Color:
            self.cardA.append(Card(color, Value.ACE)) 

        return super().setUp()

    def test_instance_of_card(self):
        """BEHAVIOR: Success"""
        for card in self.cards:
            self.assertIsInstance(card, Card)

    def test_valid_corresponding_type_of_init_argv_of_card(self):
        """BEHAVIOR: Success"""
        for card in self.cards:
            self.assertIsInstance(card.color, Color)
            self.assertIsInstance(card.value, Value)
    
    def test_invalid_corresponding_type_of_init_argv_of_card(self):
        """BEHAVIOR: Fail"""
        invalid_card1 = Card(666, 999)
        invalid_card2 = Card("HEART", "ACE")

        #pass the assert because of the non type langage
        #solution: put an assert to confirm the type in the __init__
        self.assertIsInstance(invalid_card1, Card)
        self.assertIsInstance(invalid_card2, Card)

        self.assertIsInstance(invalid_card1.color, Color)
        self.assertIsInstance(invalid_card1.value, Value)
        self.assertIsInstance(invalid_card2.color, Color)
        self.assertIsInstance(invalid_card2.value, Value)

    def test_str_string_value(self):
        """BEHAVIOR: Success"""
        #valid return tests
        self.assertMultiLineEqual(self.cardA[0].string_value(True, False, False), "ace♡") 
        self.assertMultiLineEqual(self.cardA[0].string_value(True, True, True), "A♥") 
        self.assertMultiLineEqual(self.cardA[0].string_value(True, True, False), "ace♥") 
        self.assertMultiLineEqual(self.cardA[0].string_value(True, False, True), "A♡") 
        self.assertMultiLineEqual(self.cardA[0].string_value(True, False, True, "_"), "A_♡")
        self.assertMultiLineEqual(self.cardA[0].string_value(True, False, True, "_"), "A_♡")
        #missing arguments(good care of defaults values)
        self.assertMultiLineEqual(self.cardA[0].string_value(), "A♥")

        #invalid return tests 
        self.assertNotEqual(self.cardA[0].string_value(True, False, False), "")
        #missing arguments(good care of defaults values)
        self.assertNotEqual(self.cardA[0].string_value(True), "")
        self.assertNotEqual(self.cardA[0].string_value(True, True), "")
        self.assertNotEqual(self.cardA[0].string_value(True), "A")
        self.assertNotEqual(self.cardA[0].string_value(False, True), "♥")
 
    def test_str_verbose_of_card(self):
        """BEHAVIOR: Success"""
        #valid return tests
        self.assertMultiLineEqual(self.cardA[0].verbose_string(), "ace of heart")
        self.assertMultiLineEqual(self.cardA[1].verbose_string(), "ace of diamond")
        self.assertMultiLineEqual(self.cardA[2].verbose_string(), "ace of club")
        self.assertMultiLineEqual(self.cardA[3].verbose_string(), "ace of spade")

        #invalid return tests
        self.assertNotEqual(self.cardA[0].verbose_string(), "queen of heart")
        self.assertNotEqual(self.cardA[0].verbose_string(), "ace of club")
        self.assertNotEqual(self.cardA[0].verbose_string(), "ace de heart")
        self.assertNotEqual(self.cardA[0].verbose_string(), "as de coeur")
        self.assertNotEqual(self.cardA[0].verbose_string(), "")



if __name__ == '__main__':
    print("Resume should be equal = .F... | FAILED (failures=1)")
    unittest.main()