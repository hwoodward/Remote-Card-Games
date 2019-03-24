from common.Card import Card
import random

class ServerState():
    """This tracks the game's shared state on the server.

    This includes everything that would be 'on the table' during a game,
    as opposed to stuff that is 'in a player's hand'. Server state includes:
    -draw pile
    -discard pile
    """

    def __init__(self):
        self.draw_pile = Card.GetJokerDeck()
        random.shuffle(self.draw_pile)
        print(self.draw_pile)
        self.discard_pile = []
        self.active_game = False
        self.turn_index = 0

    def DrawCards(self, numCards):
        """Return the next numCards from the draw pile"""
        result = []
        for _ in range(numCards):
            result.append(self.draw_pile.pop())
        print("drew cards")
        print(result)
        return result

    def DiscardCards(self, discardList):
        """This adds the discarded card(s) to the discard pile in order"""
        self.discard_pile.append(discardList)

    def DiscardInfo(self):
        """Provides the top card and size of the discard pile as a tuple"""
        return (self.discard_pile[-1], len(self.discard_pile))
