from client.ClientState import ClientState
from common.Card import Card
import unittest

class TestClientState(unittest.TestCase):

    def testSetup(self):
        """Confirm the state tracker initializes properly"""
        test_state = ClientState()
        self.assertFalse(test_state.turn_phase)
        self.assertEqual(test_state.hand_cards, [])
        self.assertEqual(test_state.hand_list, [])
        self.assertEqual(test_state.played_cards, {})

    def testDealtHands(self):
        """Confirm that extraHands are added to the test_state hand_list"""
        test_state = ClientState()
        hand = [Card(1, 'Spades'), Card(2, 'Clubs'), Card(3, 'Diamonds'), Card(4, 'Hearts'), Card(0, None)]
        test_state.dealtHands([hand, hand])
        self.assertEqual(test_state.hand_list, [hand])
        self.assertEqual(test_state.hand_cards, hand)
        
    def testNewCards(self):
        """Confirm newCards adds cards to hand"""
        test_state = ClientState(ruleset=None)
        wholeDeck = Card.getStandardDeck()
        test_state.newCards(wholeDeck)
        self.assertEqual(wholeDeck, test_state.hand_cards)

        drawn_cards = [Card(0, None), Card(0, None)]
        test_state.newCards(drawn_cards)
        self.assertEqual(Card.getJokerDeck(), test_state.hand_cards)
        
    def testPlayCards(self):
        """Confirm playCards transfers cards from hand to visible"""
        test_state = ClientState(ruleset=None)
        hand = [Card(1, 'Spades'), Card(2, 'Clubs'), Card(3, 'Diamonds'), Card(4, 'Hearts'), Card(0, None)]
        test_state.newCards(hand)
        test_state.playCards({1:[Card(1, 'Spades')]})
        self.assertEqual(test_state.played_cards, {1: [Card(1, 'Spades')]})
        hand.remove(Card(1, 'Spades'))
        self.assertEqual(test_state.hand_cards, hand)

        with self.assertRaises(ValueError):
            test_state.playCards({1:[Card(1, 'Spades')]})

        test_state.playCards({1:[Card(2, 'Clubs'), Card(0, None)]})
        self.assertEqual(test_state.played_cards, {1:[Card(1, 'Spades'), Card(2, 'Clubs'), Card(0, None)]})
        self.assertEqual(test_state.hand_cards, [Card(3, 'Diamonds'), Card(4, 'Hearts')])

        
    def testDiscardCards(self):
        """Confirm discardCards removes cards without playing them"""
        test_state = ClientState(ruleset=None)
        hand = [Card(1, 'Spades'), Card(2, 'Clubs'), Card(3, 'Diamonds'), Card(4, 'Hearts'), Card(0, None)]
        test_state.newCards(hand)
        test_state.discardCards([Card(1, 'Spades')])
        self.assertEqual(test_state.played_cards, {})
        hand.remove(Card(1, 'Spades'))
        self.assertEqual(test_state.hand_cards, hand)

        with self.assertRaises(ValueError):
            test_state.playCards({1:[Card(1, 'Spades')]})

        test_state.discardCards([Card(2, 'Clubs'), Card(0, None)])
        self.assertEqual(test_state.played_cards, {})
        self.assertEqual(test_state.hand_cards, [Card(3, 'Diamonds'), Card(4, 'Hearts')])


if __name__ == '__main__':
    unittest.main()
