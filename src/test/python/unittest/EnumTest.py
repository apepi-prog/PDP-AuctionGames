from main.python.engine.Card import Color
from main.python.engine.Card import Value
from main.python.engine.Action import Action
import unittest

class TestEnum(unittest.TestCase):
    
    def setUp(self) -> None:
        #ACTION
        self.action1 = Action.DOUBLE
        self.action2 = Action.EMPTY
        self.action3 = Action.HIT
        self.action4 = Action.SURRENDER
        self.action5 = Action.STAND
        
        #COLOR
        self.color1 = Color.CLUB
        self.color2 = Color.HEART
        self.color3 = Color.SPADE
        self.color4 = Color.DIAMOND

        #VALUE
        self.value1 = Value.TWO
        self.value2 = Value.THREE
        self.value3 = Value.FOUR
        self.value4 = Value.FIVE
        self.value5 = Value.SIX
        self.value6 = Value.SEVEN
        self.value7 = Value.EIGHT
        self.value8 = Value.NINE
        self.value9 = Value.TEN
        self.value10 = Value.JACK
        self.value11 = Value.QUEEN
        self.value12 = Value.KING
        self.value13 = Value.ACE
        
        return super().setUp()

    #normaly no reason to cause an error because of the Enum status of Action class
    def test_instance_of_action(self):
        """BEHAVIOR: Success"""
        self.assertIsInstance(self.action1, Action)
        self.assertIsInstance(self.action2, Action)
        self.assertIsInstance(self.action3, Action)
        self.assertIsInstance(self.action4, Action)
        self.assertIsInstance(self.action5, Action)

    def test_value_of_action(self):
        """BEHAVIOR: Success"""
        self.assertEqual(0, self.action2)
        self.assertEqual(1, self.action3)
        self.assertEqual(2, self.action5)
        self.assertEqual(3, self.action1) 
        self.assertEqual(4, self.action4)

    #normaly no reason to cause an error because of the Enum status of Color class
    def test_instance_of_color(self):
        """BEHAVIOR: Success"""
        self.assertIsInstance(self.color1, Color)
        self.assertIsInstance(self.color2, Color)
        self.assertIsInstance(self.color3, Color)
        self.assertIsInstance(self.color4, Color)

    def test_str_value_of_full_name_color(self):
        """BEHAVIOR: Success"""
        self.assertMultiLineEqual("♣", self.color1.string_value(True, True))
        self.assertMultiLineEqual("♧", self.color1.string_value(True, False))
        self.assertMultiLineEqual("club", self.color1.string_value(False, True))
        self.assertMultiLineEqual("club", self.color1.string_value(False, False))

        self.assertMultiLineEqual("♥", self.color2.string_value(True, True))
        self.assertMultiLineEqual("♡", self.color2.string_value(True, False))
        self.assertMultiLineEqual("heart", self.color2.string_value(False, True))
        self.assertMultiLineEqual("heart", self.color2.string_value(False, False))

        self.assertMultiLineEqual("♠", self.color3.string_value(True, True))
        self.assertMultiLineEqual("♤", self.color3.string_value(True, False))
        self.assertMultiLineEqual("spade", self.color3.string_value(False, True))
        self.assertMultiLineEqual("spade", self.color3.string_value(False, False))

        self.assertMultiLineEqual("♦", self.color4.string_value(True, True))
        self.assertMultiLineEqual("♢", self.color4.string_value(True, False))
        self.assertMultiLineEqual("diamond", self.color4.string_value(False, True))
        self.assertMultiLineEqual("diamond", self.color4.string_value(False, False))
    
    #normaly no reason to cause an error because of the Enum status of Value class
    def test_instance_of_Value(self):
        """BEHAVIOR: Success"""
        self.assertIsInstance(self.value1, Value)
        self.assertIsInstance(self.value2, Value)
        self.assertIsInstance(self.value3, Value)
        self.assertIsInstance(self.value4, Value)
        self.assertIsInstance(self.value5, Value)
        self.assertIsInstance(self.value6, Value)
        self.assertIsInstance(self.value7, Value)
        self.assertIsInstance(self.value8, Value)
        self.assertIsInstance(self.value9, Value)
        self.assertIsInstance(self.value10, Value)
        self.assertIsInstance(self.value11, Value)
        self.assertIsInstance(self.value12, Value)
        self.assertIsInstance(self.value13, Value)
    
    def test_str_value_of_symbol_color(self):
        """BEHAVIOR: Success"""
        #test the symbol
        self.assertMultiLineEqual("2", self.value1.string_value(True))
        self.assertMultiLineEqual("3", self.value2.string_value(True))
        self.assertMultiLineEqual("4", self.value3.string_value(True))
        self.assertMultiLineEqual("5", self.value4.string_value(True))
        self.assertMultiLineEqual("6", self.value5.string_value(True))
        self.assertMultiLineEqual("7", self.value6.string_value(True))
        self.assertMultiLineEqual("8", self.value7.string_value(True))
        self.assertMultiLineEqual("9", self.value8.string_value(True))
        self.assertMultiLineEqual("10", self.value9.string_value(True))
        self.assertMultiLineEqual("J", self.value10.string_value(True))
        self.assertMultiLineEqual("Q", self.value11.string_value(True))
        self.assertMultiLineEqual("K", self.value12.string_value(True))
        self.assertMultiLineEqual("A", self.value13.string_value(True))
        
        #test full name
        self.assertMultiLineEqual("two", self.value1.string_value(False))
        self.assertMultiLineEqual("three", self.value2.string_value(False))
        self.assertMultiLineEqual("four", self.value3.string_value(False))
        self.assertMultiLineEqual("five", self.value4.string_value(False))
        self.assertMultiLineEqual("six", self.value5.string_value(False))
        self.assertMultiLineEqual("seven", self.value6.string_value(False))
        self.assertMultiLineEqual("eight", self.value7.string_value(False))
        self.assertMultiLineEqual("nine", self.value8.string_value(False))
        self.assertMultiLineEqual("ten", self.value9.string_value(False))
        self.assertMultiLineEqual("jack", self.value10.string_value(False))
        self.assertMultiLineEqual("queen", self.value11.string_value(False))
        self.assertMultiLineEqual("king", self.value12.string_value(False))
        self.assertMultiLineEqual("ace", self.value13.string_value(False))


if __name__ == '__main__':
    print("Resume should be equal = ...... | OK")
    unittest.main()

