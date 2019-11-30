from client.ClientState import ClientState
from common.Card import Card
import unittest

class TestClientState(unittest.TestCase):

    def testSetup(self):
        """Confirm the state tracker initializes properly"""
        test_state = ClientState()
        self.assertEqual(test_state.turn_phase, 'inactive')
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
        hand = [Card(1, 'Spades'), Card(2, 'Clubs'), Card(3, 'Diamonds'), Card(4, 'Hearts'), Card(4, 'Spades'), Card(0, None)]
        test_state.newCards(hand)
        self.assertEqual(test_state.hand_cards, hand)

        #Confirm can't play cards we don't have (even if we have some)
        with self.assertRaises(Exception):
            test_state.playCards({1:[Card(1, 'Spades'), Card(1, 'Spades'), Card(0, None)]})
        #Confirm failed play didn't edit hand
        self.assertEqual(test_state.hand_cards, hand)

        #Confirm can't play illegal move
        with self.assertRaises(Exception):
            test_state.playCards({1:[Card(1, 'Spades')]})
        #Confirm failed play didn't edit hand
        self.assertEqual(test_state.hand_cards, hand)

        #Confirm legal play is allowed and edits played cards and hand properly
        test_state.newCards([Card(1, 'Spades'), Card(0, None)])
        test_state.playCards({1:[Card(1, 'Spades'), Card(1, 'Spades'), Card(0, None)]})
        self.assertEqual(test_state.played_cards, {1: [Card(1, 'Spades'), Card(1, 'Spades'), Card(0, None)]})
        hand.remove(Card(1, 'Spades'))
        self.assertEqual(test_state.hand_cards, hand)
        
        #Confirm second play adds to the played cards properly
        test_state.playCards({4:[Card(4, 'Hearts'), Card(4, 'Spades'), Card(2, 'Clubs')]})
        self.assertEqual(test_state.played_cards, {1: [Card(1, 'Spades'), Card(1, 'Spades'), Card(0, None)], 4:[Card(4, 'Hearts'), Card(4, 'Spades'), Card(2, 'Clubs')]})
        hand.remove(Card(4, 'Hearts'))
        hand.remove(Card(4, 'Spades'))
        hand.remove(Card(2, 'Clubs'))
        self.assertEqual(test_state.hand_cards, [Card(3, 'Diamonds'), Card(0, None)])

    def testPickupRulesCheck(self):
        """Confirm we check the discard pile size for pickups"""
        test_state = ClientState(ruleset=None)
        test_state.played_cards[1] = [Card(1, 'Clubs'), Card(1, 'Clubs'), Card(1, 'Clubs')]
        test_state.played_cards[4] = [Card(4, 'Clubs'), Card(4, 'Clubs'), Card(0, None)]
        
        prepared_cards = {}
        prepared_cards[5] = [Card(5, 'Clubs'), Card(5, 'Clubs')]

        #confirm too small pile disallowed
        test_state.discard_info = (Card(5, 'Hearts'), 6)
        with self.assertRaises(Exception):
            test_state.pickupPileRuleCheck( prepared_cards)

    def testDiscardCards(self):
        """Confirm discardCards removes cards without playing them"""
        test_state = ClientState(ruleset=None)
        hand = [Card(1, 'Spades'), Card(1, 'Spades'), Card(2, 'Clubs'), Card(3, 'Diamonds'), Card(4, 'Hearts'), Card(0, None)]
        test_state.newCards(hand)
        test_state.discardCards([Card(1, 'Spades')])
        self.assertEqual(test_state.played_cards, {})
        hand.remove(Card(1, 'Spades'))
        self.assertEqual(test_state.hand_cards, hand)
        
        #Confirm can only discard cards actually in your hand
        with self.assertRaises(Exception):
            test_state.discardCards([Card(1, 'Spades')])
        
        #Confirm can only discard correct number of cards
        with self.assertRaises(Exception):
            test_state.discardCards([Card(2, 'Clubs'), Card(3, 'Diamonds')])

    def testHandStatus(self):
        """Confirm that hand status information is ordered correctly"""
        test_state = ClientState(ruleset=None)
        #set turn phase
        test_state.turn_phase = 'TestPhase'
        #setup so that hand has 5 cards and there is a foot left to play
        hand = [Card(1, 'Spades'), Card(2, 'Clubs'), Card(3, 'Diamonds'), Card(4, 'Hearts'), Card(0, None)]
        test_state.dealtHands([hand, hand])
        self.assertEqual(test_state.getHandStatus(), ['TestPhase', 5, 1])

if __name__ == '__main__':
    unittest.main()
