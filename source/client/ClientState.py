import importlib
from common.Card import Card


class ClientState:
    """ This class store client state for access by different listeners

    It tracks things like 'interactivity', a player's hand, discard state, etc.
    It stores what is needed to compute scores and decide on move legality
    """

    def __init__(self, ruleset = None):
        """Initialize a state tracker for a given client"""
        self.ruleset = ruleset
        if ruleset is not None:
            rule_module = "common." + ruleset
        else:
            #This is the unit test case - we may want to put a dummy ruleset in
            print("In unittest mode - using HandAndFoot rules")
            rule_module = "common.HandAndFoot"

        self.rules = importlib.import_module(rule_module)
        # Turn phase handled by controller
        self.turn_phase = 'inactive'  # hard coded start phase as 'not my turn'
        self.round = -1  # Start with the 'no current round value'
        self.name = "guest"
        self.player_index = 0 # needed for Liverpool.
        self.reset()  # Start with state cleared for a fresh round
        # Will need to know player index in Liverpool because prepare cards buttons shared.

    def getPlayerIndex(self, player_names):
        """Store the extra hands dealt to player for use after first hand is cleared"""
        self.player_index = player_names.index(self.name)

    def dealtHands(self, hands):
        """Store the extra hands dealt to player for use after first hand is cleared"""
        self.newCards(hands[0])
        self.hand_list = hands[1:]
        
    def nextHand(self):
        """Transition to the next hand in the hand_list"""
        if len(self.hand_cards) > 0:
            raise Exception("You can't pick up your foot while you have cards left in your hand.")
        self.hand_cards = self.hand_list.pop()
        
    def checkGoneOut(self):
        """Check if a player has gone out"""
        if len(self.hand_cards) > 0:
            return False
        if len(self.hand_list) > 0:
            return False
        return self.rules.goneOut(self.played_cards)

    def scoreRound(self):
        """Get score for round"""
        # Need to combine hand an foot for cancellation with played cards
        unplayed_cards = self.hand_cards
        for hand in self.hand_list:
            unplayed_cards += hand
        score = self.rules.scoreRound(self.played_cards, unplayed_cards, self.went_out)
        return score

    def reset(self):
        """Clear out round specific state to prepare for next round to start"""
        self.hand_list = []
        self.hand_cards = []
        self.played_cards = {}
        self.went_out = False
        self.discard_info = [None, 0]
        
    def newCards(self, card_list):
        """Update the cards in hand"""
        for card in card_list:
            self.hand_cards.append(card)

    def playCards(self, prepared_cards, player_index = 0, visible_cards=[{}]):
        """Move cards from hand to visible"""

        # cards in visible_cards are serialized, cards in prepared_cards are not.
        # First check that all the cards are in your hand.
        print('in ClientState.py, playCards method')
        tempHand = [x for x in self.hand_cards]
        try:
            for card_group in prepared_cards.values():
                for card in card_group:
                    tempHand.remove(card)
        except ValueError:
            raise Exception("Attempted to play cards that are not in your hand")
        #todo: put variable in rulesets regarding whether you can play on others groups.
        # for HandAndFoot it would be false, and for Liverpool it would be true.
        # that would determine whether self.played_cards = visible cards or cards that player played.
        if self.ruleset == 'HandAndFoot':
            self.rules.canPlay(prepared_cards, self.played_cards, self.round)
            for key, card_group in prepared_cards.items():
                for card in card_group:
                    self.hand_cards.remove(card)
                    self.played_cards.setdefault(key, []).append(card)
        elif self.ruleset == 'Liverpool':
            self.rules.canPlay(prepared_cards, visible_cards, player_index, self.round)
            # unlike self.played_cards used in HandAndFoot, visible_cards is obtained
            # from controller, and contains serialized cards.
            for key, card_group in prepared_cards.items():
                for card in card_group:
                    self.hand_cards.remove(card)
                    # 19oct - don't think liverpool really uses played_cards other than in my print statement...
                    self.played_cards.setdefault(key, []).append(card)
                    # todo:  Need to replace local record of played_cards with visible cards.
                    # This will have ripple effects in rules when merging played cards with visible cards.
                #TODO: debug THE NEXT 2 LINES!!!
                #  self.played_cards = visible_card[key0][key1]
                # self.played_cards.setdefault(key[1], []).append(card)
        print('at line 108 in clientState, played_cards: ')
        print(self.played_cards)

    def getValidKeys(self, card):
        """Get the keys that this card can be prepared with"""
        return self.rules.getKeyOptions(card)

    def pickupPileRuleCheck(self, prepared_cards):
        """Confirm a player can pick up the pile with the prepared cards"""
        # check there are enough cards
        if self.discard_info[1] < self.rules.Pickup_Size:
            text = 'Cannot pickup the pile until there are ' + str(self.rules.Pickup_Size) + ' cards.'
            raise Exception(text)
        return self.rules.canPickupPile(self.discard_info[0], prepared_cards, self.played_cards, self.round)

    def discardCards(self, card_list):
        """Discard cards from hand"""
        if len(card_list) != self.rules.Discard_Size:
            raise Exception("Wrong discard size. Must discard {0} cards".format(self.rules.Discard_Size))
        # check that all the cards are in your hand
        tempHand = [x for x in self.hand_cards]
        try:
            for card in card_list:
                tempHand.remove(card)
        except ValueError:
            raise Exception("Attempted to discard cards that are not in your hand")
        for card in card_list:
            self.hand_cards.remove(card)

    def updateDiscardInfo(self, top_card, size):
        """Update the discard information"""
        self.discard_info = [top_card, size]
    
    def getHandStatus(self):
        """Bundles public information in the format needed for sending to the server"""
        ### Public info has a hard coded order for interpretation - see the wiki to make sure it is kept consistent
        return [self.turn_phase, len(self.hand_cards), len(self.hand_list)]
