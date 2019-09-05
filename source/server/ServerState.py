from common.Card import Card

import random
import importlib

class ServerState():
    """This tracks the game's shared state on the server.

    This includes everything that would be 'on the table' during a game,
    as opposed to stuff that is 'in a player's hand'. Server state includes:
    -draw pile
    -discard pile
    """

    def __init__(self, ruleset):
        rule_module = "common." + ruleset
        self.rules = importlib.import_module(rule_module)
        self.draw_pile = Card.getJokerDeck()
        random.shuffle(self.draw_pile)
        self.discard_pile = []
        self.active_game = False
        self.turn_index = 0

    def drawCards(self):
        """Return the next numCards from the draw pile"""
        result = []
        for _ in range(self.rules.Draw_Size):
            result.append(self.draw_pile.pop())
        return result

    def discardCards(self, discard_list):
        """This adds the discarded card(s) to the discard pile in order"""
        for card in discard_list:
            self.discard_pile.append(card)

    def discardInfo(self):
        """Provides the top card and size of the discard pile as a tuple"""
        return (self.discard_pile[-1], len(self.discard_pile))
