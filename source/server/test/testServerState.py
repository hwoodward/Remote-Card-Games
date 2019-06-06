from server.ServerState import ServerState
from common.Card import Card
import unittest

class TestServerState(unittest.TestCase):

    def testSetup(self):
        """Confirm that state tracker initializes properly"""
        testState = ServerState()
        self.assertEqual(testState.turn_index, 0)
        self.assertEqual(len(testState.draw_pile), 54)
        self.assertEqual(len(testState.discard_pile), 0)
        #Not sure how to confirm that the deck is shuffled
        
    def testDraw(self):
        """Confirm that drawing works as it should.

            Returns specified number of cards
            Returns top cards in the pile
            Removes those cards from the pile"""
        testState = ServerState()
        topCard = testState.draw_pile[-1]
        secondCard = testState.draw_pile[-2]
        drawResult = testState.DrawCards(2)
        self.assertEqual(len(testState.draw_pile), 52)
        self.assertEqual(len(drawResult), 2)
        self.assertEqual(topCard, drawResult[0])
        self.assertEqual(secondCard, drawResult[1])

    def testDiscard(self):
        """Confirm that discarCards adds all cards to discard pile in order"""
        testState = ServerState()
        discardList = [Card(0,None), Card(3,'Spades'), Card(2, 'Clubs')]
        testState.DiscardCards(discardList)
        self.assertEqual(len(testState.discard_pile), 3)
        self.assertEqual(testState.discard_pile, discardList)

        discardList = [Card(12, 'Hearts')]
        testState.DiscardCards(discardList)
        self.assertEqual(len(testState.discard_pile), 4)
        self.assertEqual(testState.discard_pile[-1], discardList[0])

    def testDiscardInfo(self):
        """Confirm that DiscardInfo accurately reporst discard_pile status"""
        testState = ServerState()
        discardList = [Card(0,None), Card(3,'Spades'), Card(2, 'Clubs')]
        testState.DiscardCards(discardList)
        info = testState.DiscardInfo()
        self.assertEqual((Card(2, 'Clubs'), 3), info)

if __name__ == '__main__':
    unittest.main()
