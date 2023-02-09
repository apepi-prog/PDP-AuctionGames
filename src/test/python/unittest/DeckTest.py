from main.python.engine.Card import *
from main.python.engine.Deck import Deck
import random
import copy
import unittest

class TestDeck(unittest.TestCase):

    def setUp(self) -> None:
        self.deck1 = Deck(1)
        self.deck2 = Deck("id1")
        self.deck3 = Deck(3.4)

        return super().setUp()

    def test_instance_of_deck(self):
        """BEHAVIOR: Success (with its comment line)"""
        #pass the test because of the nontype langage 
        #solution: put an assert to confirm the type in the __init__
        self.assertIsInstance(self.deck1, Deck)
        self.assertIsInstance(self.deck2, Deck)
        self.assertIsInstance(self.deck3, Deck) 
    
    def test_init_value_of_deck(self):
        """BEHAVIOR: Success (with its comment line)"""
        self.assertEqual(1, self.deck1.deck_id)
        self.assertListEqual([], self.deck1.discarded)
        self.assertEqual(52, len(self.deck1.cards))
        self.assertEqual(len(set(self.deck1.cards)), len(self.deck1.cards)) #check for doublon

    def test_valid_corresponding_type_of_init_argv_of_deck(self):
        """BEHAVIOR: Success"""
        self.assertIsInstance(self.deck1.deck_id, int)
    
    def test_invalid_corresponding_type_of_init_argv_of_deck(self):
        """BEHAVIOR: Fail"""
        self.assertIsInstance(self.deck2.deck_id, int)
        self.assertIsInstance(self.deck3.deck_id, int)

    def test_shuffle_deck(self):
        """BEHAVIOR: Fail"""
        deck_compare = copy.copy(self.deck1.cards)
        self.assertListEqual(deck_compare, self.deck1.cards)
        
        self.deck1.shuffle()
        self.assertListEqual(deck_compare, self.deck1.cards)
    
    def test_pop_card_in_deck(self):
        """BEHAVIOR: Success"""
        deck_compare = copy.copy(self.deck1.cards)
        self.assertListEqual(deck_compare, self.deck1.cards)

        pop_elmt = self.deck1.pop()
        self.assertNotIn(deck_compare[-1], self.deck1.cards)
        self.assertEqual(pop_elmt, deck_compare[len(deck_compare)-1])
        
    def test_discard_cards_in_deck(self):
        """BEHAVIOR: Success"""
        discard_cards = []
        discard_cards_compare = [self.deck1.cards[i] for i in range (10, 16)]
        
        #before every action on the deck
        self.assertListEqual(discard_cards, self.deck1.discarded)
        self.assertNotEqual(discard_cards_compare, discard_cards)
  
        for i in range(6):
            discard_cards.append(self.deck1.cards[i])
        self.assertNotEqual(discard_cards, self.deck1.discarded)
        self.assertNotEqual(discard_cards_compare, discard_cards)
        self.assertNotEqual(discard_cards_compare, self.deck1.discarded)

        #after the discard action
        self.deck1.discard(discard_cards)
        self.assertListEqual(discard_cards, self.deck1.discarded)
        self.assertNotEqual([], self.deck1.discarded)
        self.assertNotEqual(discard_cards_compare, self.deck1.discarded)

    def test_size_deck(self):
        """BEHAVIOR: Success"""
        full_size_deck = 52
        compare_cards = [self.deck1.cards[i] for i in range(40)]

        #before every action on the deck
        self.assertEqual(full_size_deck, self.deck1.size())

        #after poping cards from the deck
        for i in range(10):
            self.deck1.cards.pop(random.randint(0, len(self.deck1.cards)-1))
        self.assertGreater(full_size_deck, self.deck1.size())
        self.assertNotEqual(full_size_deck, self.deck1.size())
        self.assertGreater(self.deck1.size(), len(compare_cards))
        self.assertNotEqual(len(compare_cards), self.deck1.size())
        
        self.assertEqual(full_size_deck - 10, self.deck1.size())

    def test_empty_deck(self):
        """BEHAVIOR: Success"""
        #before every action on the deck
        self.assertFalse(self.deck1.is_empty())

        #after poping all the cards in deck
        for i in range(52):
            self.deck1.cards.pop()
        self.assertTrue(self.deck1.is_empty())

    def test_refill_deck(self):
        """BEHAVIOR: Success"""
        compare_cards = copy.copy(self.deck1.cards)
        
        #before every action on the deck
        self.assertEqual(compare_cards, self.deck1.cards)
        self.deck1.refill()
        self.assertNotEqual(compare_cards, self.deck1.cards) #check the shuffle
        self.assertEqual(len(set(self.deck1.cards)), len(self.deck1.cards)) #check for doublon
        self.assertEqual(len(compare_cards), len(self.deck1.cards))
        
        #after poping 10 random cards in the deck and put them in discard
        compare_cards = copy.copy(self.deck1.cards)
        for i in range(10):
            self.deck1.discarded.append(self.deck1.cards.pop(random.randint(0, len(self.deck1.cards)-1)))
        
        self.assertNotEqual(compare_cards, self.deck1.cards)
        self.assertGreater(len(self.deck1.discarded), 0) #to compare the state of discarded after the refill
        self.deck1.refill()
        self.assertNotEqual(compare_cards, self.deck1.cards) #check the shuffle
        self.assertEqual(len(set(self.deck1.cards)), len(self.deck1.cards)) #check for doublon
        self.assertEqual(len(compare_cards), len(self.deck1.cards))
        for card in compare_cards:
            self.assertIn(card, self.deck1.cards) #check if all de discarted card are back in the deck
        self.assertListEqual([], self.deck1.discarded) #check the discarded clear of the method 
        

if __name__ == '__main__':
    print("Resume should be equal = ....F..F.. | FAILED (failures=2)")
    unittest.main()
