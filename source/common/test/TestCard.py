from common.Card import Card
import unittest

class TestCardMethods(unittest.TestCase):

    def test_GetColor(self):
        """Confirm that card class correctly identifies colors"""
        #Jokers have no color
        test_card = Card(0, None)
        self.assertEqual(test_card.getColor(), None)
        #Spades are "Black"
        test_card = Card(2, 'Spades')
        self.assertEqual(test_card.getColor(), "Black")
        #Clubs are "Black"
        test_card = Card(3, 'Clubs')
        self.assertEqual(test_card.getColor(), 'Black')
        #Hearts are "Red"
        test_card = Card(5, 'Hearts')
        self.assertEqual(test_card.getColor(), 'Red')
        #Diamonds are "Red"
        test_card = Card(6, 'Diamonds')
        self.assertEqual(test_card.getColor(), "Red")

    def test_Serialize(self):
        """Confirm that cards serialize to a tuple properly"""
        #Confirm its number than suit
        test_card = Card(3, 'Hearts')
        self.assertEqual(test_card.serialize(), (3, 'Hearts'))
        
    def test_DeSerialize(self):
        """Confirm that cards are properly constructed from deserializing a tuple"""
        #deserialize joker
        test_tuple = (0, None)
        test_card = Card.deserialize(test_tuple)
        self.assertEqual(test_card, Card(0, None))
        #deserialize suit card
        test_tuple = (3, 'Clubs')
        test_card = Card.deserialize(test_tuple)
        self.assertEqual(test_card.suit, "Clubs")
        self.assertEqual(test_card.number, 3)
        #deserialize errors on invalid input card
        with self.assertRaises(ValueError):
            test_tuple = (66, 'Hearts')
            tesCard = Card.deserialize(test_tuple)

    def test_Equivalence(self):
        """Confirm two cards are equal based on values not instantiation"""
        test_card_A = Card(11, "Diamonds")
        test_card_B = Card(11, 'Diamonds')
        test_card_C = Card(10, 'Diamonds')
        test_card_D = Card(11, 'Clubs')
        #Confirm self-equivalence
        self.assertEqual(test_card_A, test_card_A)
        #Confirm dif cards with same values are equal
        self.assertEqual(test_card_A, test_card_B)
        #Confirm non-equivalence if only numbers differ
        self.assertNotEqual(test_card_A, test_card_C)
        #Confirm not equal if only suit differs
        self.assertNotEqual(test_card_A, test_card_D)
        
    def test_Construction(self):
        """Confirm that cards are constructed properly and error on invalid values"""
        #Can make jokers (suit None)
        test_card = Card(0, None)
        #Any number given for a joker is set to 0
        test_card = Card(9999, None)
        self.assertEqual(test_card.number, 0)
        #All suits are options, '' or "" works for strings
        test_card = Card(1, 'Spades')
        test_card = Card(2, "Hearts")
        test_card = Card(13, "Diamonds")
        test_card = Card(10, 'Clubs')
        #Non-suit strings and non-plural suitnames are invalid
        with self.assertRaises(ValueError):
            test_card = Card(1, 'fakityFake')
        with self.assertRaises(ValueError):
            test_card = Card(1, 'Spade')
        #0 and numbers over 13 are invalid for non-Joker cards
        with self.assertRaises(ValueError):
            test_card = Card(0, 'Spades')
        with self.assertRaises(ValueError):
            test_card = Card(14, 'Spades')

    def testDecks(self):
        """Confirm standard deck and joker deck aren't obviously wrong"""
        deck = Card.getStandardDeck()
        #length check
        self.assertEqual(len(deck), 52)
        #joker check
        self.assertFalse(Card(0, None) in deck)
        joker_deck = Card.getJokerDeck()
        #length check
        self.assertEqual(len(joker_deck), 54)
        #joker check
        self.assertTrue(Card(0, None) in joker_deck)
        #containsStandard check
        self.assertTrue(all(card in joker_deck for card in deck))

if __name__ == '__main__':
    unittest.main()
