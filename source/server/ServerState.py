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

    def __init__(self, ruleset = None):
        if ruleset != None:
            rule_module = "common." + ruleset
        else:
            #This is the unit test case - we may want to put a dummy ruleset in
            print("In unittest mode - using HandAndFoot rules")
            rule_module = "common.HandAndFoot"

        self.rules = importlib.import_module(rule_module)
        self.draw_pile = []
        self.round = -1 #Start at negative so first nextRound call increments to 0
        self.discard_pile = []
        self.turn_index = 0

    def constructDeck(self, numPlayers):
        """Build up and shuffle the draw_pile deck based on rules"""
        deck = []
        for _ in range(0, self.rules.numDecks(numPlayers)):
            for card in self.rules.singleDeck():
                deck.append(card)
        random.shuffle(deck)
        self.draw_pile = deck

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

    def getDiscardInfo(self):
        """Provides the top card and size of the discard pile as a tuple"""
        return [self.discard_pile[-1], len(self.discard_pile)]

    def dealHands(self):
        """Return all hands to deal to a single player at the start of a round"""
        all_hands = []
        for _ in range(self.rules.Hands_Per_Player):
            hand = []
            for _ in range(self.rules.Deal_Size):
                hand.append(self.draw_pile.pop())
            all_hands.append(hand)
        return all_hands