from common.Card import Card
import unittest

class TestCardMethods(unittest.TestCase):

    def test_GetColor(self):
        """Confirm that card class correctly identifies colors"""
        #Jokers have no color
        testCard = Card(0, None)
        self.assertEqual(testCard.GetColor(), None)
        #Spades are "Black"
        testCard = Card(2, 'Spades')
        self.assertEqual(testCard.GetColor(), "Black")
        #Clubs are "Black"
        testCard = Card(3, 'Clubs')
        self.assertEqual(testCard.GetColor(), 'Black')
        #Hearts are "Red"
        testCard = Card(5, 'Hearts')
        self.assertEqual(testCard.GetColor(), 'Red')
        #Diamonds are "Red"
        testCard = Card(6, 'Diamonds')
        self.assertEqual(testCard.GetColor(), "Red")

    def test_Serialize(self):
        """Confirm that cards serialize to a tuple properly"""
        #Confirm its number than suit
        testCard = Card(3, 'Hearts')
        self.assertEqual(testCard.Serialize(), (3, 'Hearts'))
        
    def test_DeSerialize(self):
        """Confirm that cards are properly constructed from deserializing a tuple"""
        #deserialize joker
        testTuple = (0, None)
        testCard = Card.Deserialize(testTuple)
        self.assertEqual(testCard, Card(0, None))
        #deserialize suit card
        testTuple = (3, 'Clubs')
        testCard = Card.Deserialize(testTuple)
        self.assertEqual(testCard._suit, "Clubs")
        self.assertEqual(testCard._number, 3)
        #deserialize errors on invalid input card
        with self.assertRaises(ValueError):
            testTuple = (66, 'Hearts')
            tesCard = Card.Deserialize(testTuple)

    def test_Equivalence(self):
        """Confirm two cards are equal based on values not instantiation"""
        testCardA = Card(11, "Diamonds")
        testCardB = Card(11, 'Diamonds')
        testCardC = Card(10, 'Diamonds')
        testCardD = Card(11, 'Clubs')
        #Confirm self-equivalence
        self.assertEqual(testCardA, testCardA)
        #Confirm dif cards with same values are equal
        self.assertEqual(testCardA, testCardB)
        #Confirm non-equivalence if only numbers differ
        self.assertNotEqual(testCardA, testCardC)
        #Confirm not equal if only suit differs
        self.assertNotEqual(testCardA, testCardD)
        
    def test_Construction(self):
        """Confirm that cards are constructed properly and error on invalid values"""
        #Can make jokers (suit None)
        testCard = Card(0, None)
        #Any number given for a joker is set to 0
        testCard = Card(9999, None)
        self.assertEqual(testCard._number, 0)
        #All suits are options, '' or "" works for strings
        testCard = Card(1, 'Spades')
        testCard = Card(2, "Hearts")
        testCard = Card(13, "Diamonds")
        testCard = Card(10, 'Clubs')
        #Non-suit strings and non-plural suitnames are invalid
        with self.assertRaises(ValueError):
            testCard = Card(1, 'fakityFake')
        with self.assertRaises(ValueError):
            testCard = Card(1, 'Spade')
        #0 and numbers over 13 are invalid for non-Joker cards
        with self.assertRaises(ValueError):
            testCard = Card(0, 'Spades')
        with self.assertRaises(ValueError):
            testCard = Card(14, 'Spades')

    def testDecks(self):
        """Confirm standard deck and joker deck aren't obviously wrong"""
        deck = Card.GetStandardDeck()
        #length check
        self.assertEqual(len(deck), 52)
        #joker check
        self.assertFalse(Card(0, None) in deck)
        jokerDeck = Card.GetJokerDeck()
        #length check
        self.assertEqual(len(jokerDeck), 54)
        #joker check
        self.assertTrue(Card(0, None) in jokerDeck)
        #containsStandard check
        self.assertTrue(all(card in jokerDeck for card in deck))

if __name__ == '__main__':
    unittest.main()
