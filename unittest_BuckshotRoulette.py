import unittest
from BuckshotRoulette import *

class MyTestCase(unittest.TestCase):
    def test_help_message(self):
        """Verify that every move has a help message"""
        print(BSRoulette.MOVE_LIST)
        for move in BSRoulette.MOVE_LIST:
            self.assertIsNotNone(BSRoulette.help(f"{move}"))
if __name__ == '__main__':
    unittest.main()
