from common import Card
import random

class ServerState():
    """This tracks the game's shared state on the server.

    This includes everything that would be 'on the table' during a game,
    as opposed to stuff that is 'in a player's hand'. Server state includes:
    -draw pile
    -discard pile
    """

    def __init__(self):
        self.draw_pile = random.shuffle(Card.Joker_Deck)
        self.discard_pile = []

    def drawCards(self, numCards):
        """Return the next numCards from the draw pile"""
        result = []
        for _ in range(numCards):
            result.append(self.draw_pile.pop())
        return result

    def discardCards(self, discardList):
        """This adds the discarded card(s) to the discard pile in order"""
        #TODO: we should probably check the discarded items are really cards
        self.discard_pile.append(discardList)
