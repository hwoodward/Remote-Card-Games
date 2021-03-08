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
        if ruleset is not None:
            rule_module = "common." + ruleset
        else:
            # This is the unit test case - we may want to put a dummy ruleset in
            print("In unittest mode - using HandAndFoot rules")
            rule_module = "common.HandAndFoot"

        self.rules = importlib.import_module(rule_module)
        self.draw_pile = []
        self.round = -1  # Start at negative so first nextRound call increments to 0
        self.discard_pile = []
        self.turn_index = 0
        self.num_decks_in_play = 0
        self.Draw_Size_original = self.rules.Draw_Size # At start of new round may need to reset Draw_Size in some games


    def prepareRound(self, numPlayers):
        """Reset the state for a round
        
        Constructs the shuffled draw pile
        Clears out the discard pile
        """
        deck = []
        num_decks = self.rules.numDecks(numPlayers)
        for deck_number in range(0, num_decks):
            for card in self.rules.singleDeck(deck_number):
                deck.append(card)
        random.shuffle(deck)
        self.draw_pile = deck
        self.discard_pile = []
        self.num_decks_in_play = num_decks
        self.rules.Draw_Size = self.Draw_Size_original # Draw_Size may be reset during a round if draw pile runs out.

    def drawCards(self):
        """Return the next Draw_Size cards from the draw pile"""
        if len(self.draw_pile) < self.rules.Draw_Size:
            note = self.refreshDrawPile()
            print(note)
            #todo: want to broadcast this note.
        result = []
        for _ in range(self.rules.Draw_Size):
            result.append(self.draw_pile.pop())
        return result
    
    def pickUpPile(self):
        """Return the top Pickup_Size cards from the discard pile"""
        result = []
        for _ in range(self.rules.Pickup_Size):
            result.append(self.discard_pile.pop())
        return result

    def discardCards(self, discard_list):
        """This adds the discarded card(s) to the discard pile in order"""
        for card in discard_list:
            self.discard_pile.append(card)

    def getDiscardInfo(self):
        """Provides the top card and size of the discard pile as a tuple"""
        top_card = Card(0, None, 0)  # If pile is empty we still need a default card since None doesn't serialize
        if len(self.discard_pile) > 0:
            top_card = self.discard_pile[-1]
        return [top_card, len(self.discard_pile)]

    def dealHands(self):
        """Return all hands to deal to a single player at the start of a round"""
        all_hands = []
        for _ in range(self.rules.Hands_Per_Player):
            hand = []
            for _ in range(self.rules.Deal_Size):
                hand.append(self.draw_pile.pop())
            all_hands.append(hand)
        return all_hands

    def refreshDrawPile(self):
        """ if draw pile doesn't have enough cards for draw, then refresh it-- method depends on ruleset."""
        if self.rules.Refresh_Draw_Pile == 'shuffle_discards':
            top_discard = self.discard_pile.pop(0)
            draw_pile_new = self.discard_pile
            self.discard_pile = [top_discard]
            random.shuffle(draw_pile_new)
            self.draw_pile = self.draw_pile + draw_pile_new
            note = 'Discards have been shuffled and put in draw pile.'
            if len(self.draw_pile)< self.rules.Draw_Size:
                self.rules.Draw_Size = len(self.draw_pile)
                note =  note + 'Pile still too small, draw size now smaller...'
        elif self.rules.Refresh_Draw_Pile == 'fresh_decks':
            deck = []
            num_decks = self.rules.numDecks(1)        # add number of decks that you would use for 1 player.
            for newdeck in range(0, num_decks):
                for card in self.rules.singleDeck(newdeck + self.num_decks_in_play):
                    deck.append(card)
            random.shuffle(deck)
            self.draw_pile = self.draw_pile + deck
            self.num_decks_in_play = self.num_decks_in_play + num_decks
            note = str(num_decks) + ' fresh decks have been added to draw pile.'
        else:
            self.rules.Draw_Size = len(self.draw_pile)
            note = 'Pile is empty -- no more drawing this round.'
        return note

