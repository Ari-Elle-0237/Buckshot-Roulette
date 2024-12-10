import unittest
from BuckshotRoulette import *

SAMPLE_SIZE = 100
class MyTestCase(unittest.TestCase):
    def test_help_message(self):
        """Verify that every move has a help message"""
        print(BSRoulette.MOVE_LIST)
        for move in BSRoulette.MOVE_LIST:
            print(BSRoulette.help(f"{move}"))
            self.assertIsNotNone(BSRoulette.help(f"{move}"))

    def test_magazine_generation(self):
        for _ in range(SAMPLE_SIZE):
            magazine = BSRoulette.generate_magazine()
            # Verify There is at least one live and one Blank
            self.assertIn(True, magazine)
            self.assertIn(False, magazine)
            # Verify the magazine is the right size
            self.assertGreaterEqual(len(magazine), 2)
            self.assertLessEqual(len(magazine), 6)

if __name__ == '__main__':
    unittest.main()
