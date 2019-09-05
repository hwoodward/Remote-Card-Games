from client.StateTracker import ClientState
from common.Card import Card
import unittest

class TestClientState(unittest.TestCase):

    def testSetup(self):
        """Confirm the state tracker initializes properly"""
        testState = ClientState()
        self.assertFalse(testState.interactive)
        self.assertEqual(testState.hand_cards, [])
        self.assertEqual(testState.visible_cards, [])

    def testNewCards(self):
        """Confirm newCards adds cards to hand"""
        testState = ClientState()
        wholeDeck = Card.GetStandardDeck()
        testState.newCards(wholeDeck)
        self.assertEqual(wholeDeck, testState.hand_cards)

        drawnCards = [Card(0, None), Card(0, None)]
        testState.newCards(drawnCards)
        self.assertEqual(Card.GetJokerDeck(), testState.hand_cards)
        
    def testPlayCards(self):
        """Confirm playCards transfers cards from hand to visible"""
        testState = ClientState()
        hand = [Card(1, 'Spades'), Card(2, 'Clubs'), Card(3, 'Diamonds'), Card(4, 'Hearts'), Card(0, None)]
        testState.newCards(hand)
        testState.playCards([Card(1, 'Spades')])
        self.assertEqual(testState.visible_cards, [Card(1, 'Spades')])
        hand.remove(Card(1, 'Spades'))
        self.assertEqual(testState.hand_cards, hand)

        with self.assertRaises(ValueError):
            testState.playCards([Card(1, 'Spades')])

        testState.playCards([Card(2, 'Clubs'), Card(0, None)])
        self.assertEqual(testState.visible_cards, [Card(1, 'Spades'), Card(2, 'Clubs'), Card(0, None)])
        self.assertEqual(testState.hand_cards, [Card(3, 'Diamonds'), Card(4, 'Hearts')])

        
    def testDiscardCards(self):
        """Confirm discardCards removes cards without playing them"""
        testState = ClientState()
        hand = [Card(1, 'Spades'), Card(2, 'Clubs'), Card(3, 'Diamonds'), Card(4, 'Hearts'), Card(0, None)]
        testState.newCards(hand)
        testState.discardCards([Card(1, 'Spades')])
        self.assertEqual(testState.visible_cards, [])
        hand.remove(Card(1, 'Spades'))
        self.assertEqual(testState.hand_cards, hand)

        with self.assertRaises(ValueError):
            testState.playCards([Card(1, 'Spades')])

        testState.discardCards([Card(2, 'Clubs'), Card(0, None)])
        self.assertEqual(testState.visible_cards, [])
        self.assertEqual(testState.hand_cards, [Card(3, 'Diamonds'), Card(4, 'Hearts')])


if __name__ == '__main__':
    unittest.main()
