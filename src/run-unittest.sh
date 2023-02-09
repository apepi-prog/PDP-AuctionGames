#!/bin/sh

#test on all Enum class
PYTHONPATH=. python3 test/python/unittest/EnumTest.py

#test on Card class
PYTHONPATH=. python3 test/python/unittest/CardTest.py

#test on Deck class
PYTHONPATH=. python3 test/python/unittest/DeckTest.py

#test on Player class
PYTHONPATH=. python3 test/python/unittest/DealerPlayerTest.py
PYTHONPATH=. python3 test/python/unittest/HumanPlayerTest.py

#test on AI Class
PYTHONPATH=. python3 test/python/unittest/ai/AIPlayerBasicTest.py
PYTHONPATH=. python3 test/python/unittest/ai/AIPlayerHiloTest.py
PYTHONPATH=. python3 test/python/unittest/ai/AIPlayerHiloNoCountTest.py
#test on Utils file methods
PYTHONPATH=. python3 test/python/unittest/UtilsTest.py 
