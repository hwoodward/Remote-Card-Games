from common.Card import Card
import unittest

class TestCardMethods(unittest.TestCase):

    def test_GetColor(self):
        self.fail()

    def test_Serialize(self):
        self.assertTrue(False) #Not implemented

    def test_DeSerialize(self):
        self.assertTrue(False) #Not implemented

    def test_Equivalence(self):
        self.assertTrue(False) #Not implemented

    def test_Construction(self):
        testCard = Card(0, None)
        testCard = Card(9999, None)
        self.assertEquals(testCard._number, 0)
        testCard = Card(1, 'Spades')
        testCard = Card(2, "Hearts")
        testCard = Card(13, "Diamonds")
        testCard = Card(10, 'Clubs')
        with self.assertRaises(ValueError):
            testCard = Card(1, 'fakityFake')
        with self.assertRaises(ValueError):
            testCard = Card(1, 'Spade')
        with self.assertRaises(ValueError):
            testCard = Card(0, 'Spades')
        with self.assertRaises(ValueError):
            testCard = Card(14, 'Spades')

if __name__ == '__main__':
    unittest.main()
