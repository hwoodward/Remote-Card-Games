import importlib
from commonCard import Card

class ClientState():
    """ This class store client state for access by different listeners

    It tracks things like 'interactivity', a player's hand, discard state, etc.
    It stores what is needed to compute scores and decide on move legality
    """

    def __init__(self, ruleset = None):
        """Initialize a state tracker for a given client"""
        if ruleset != None:
            # rule_module = "common." + ruleset
            rule_module = "commonHandAndFoot"
        else:
            #This is the unit test case - we may want to put a dummy ruleset in
            print("In unittest mode - using HandAndFoot rules")
            # rule_module = "common.HandAndFoot"
            rule_module = "commonHandAndFoot"

        self.rules = importlib.import_module(rule_module)
        #Turn phase handled bcoy controller
        self.turn_phase = 'inactive' #hard coded start phase as 'not my turn'
        self.round = -1 #Start with the 'no current round value
        self.went_out = False #Boolean to track if you went out.
        self.name = "guest"
        self.hand_list = []
        self.hand_cards = []
        self.played_cards = {}
        self.discard_info = [None, 0] #This is top_card and then size

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
        """Get score for round and clears round specific state in preparation for next round to start"""
        # Need to combine hand an foot for cancellation with played cards
        unplayed_cards = self.hand_cards
        for hand in self.hand_list:
            unplayed_cards += hand
        score = self.rules.scoreRound(self.played_cards, unplayed_cards, self.went_out)
        
        # Clear out round-specific state.
        self.hand_list = []
        self.hand_cards = []
        self.played_cards = {}
        self.went_out = False
        self.discard_info = [None, 0]
        
        return score
        
    def newCards(self, card_list):
        """Update the cards in hand"""
        for card in card_list:
            self.hand_cards.append(card)

    def playCards(self, prepared_cards):
        """Move cards from hand to visible"""
        #First check that all the cards are in your hand
        tempHand = [x for x in self.hand_cards]
        try:
            for card_group in prepared_cards.values():
                for card in card_group:
                    tempHand.remove(card)
        except ValueError:
            raise Exception("Attempted to play cards that are not in your hand")
        self.rules.canPlay(prepared_cards, self.played_cards, self.round)
        for key, card_group in prepared_cards.items():
            for card in card_group:
                self.hand_cards.remove(card)
                self.played_cards.setdefault(key, []).append(card)
    
    def getValidKeys(self, card):
        """Get the keys that this card can be prepared with"""
        return self.rules.getKeyOptions(card)

    def pickupPileRuleCheck(self, prepared_cards):
        """Confirm a player can pick up the pile with the prepared cards"""
        # check there are enough cards
        if self.discard_info[1] < self.rules.Pickup_Size:
            raise Exception("Cannot pickup the pile until there are 8 cards")
        # check prepared cards meet the forced play requirements
        return self.rules.canPickupPile(self.discard_info[0], prepared_cards, self.played_cards, self.round)

    def discardCards(self, card_list):
        """Discard cards from hand"""
        if len(card_list) != self.rules.Discard_Size:
            raise Exception("Wrong discard size. Must discard {0} cards".format(self.rules.Discard_Size))
        #check that all the cards are in your hand
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
