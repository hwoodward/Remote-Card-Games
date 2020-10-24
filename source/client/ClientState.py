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

    def playCards(self, prepared_cards, player_index = 0, visible_scards=[{}]):
        """Move cards from hand to board"""

        # First check that all the cards are in your hand.
        tempHand = [x for x in self.hand_cards]
        try:
            for card_group in prepared_cards.values():
                for card in card_group:
                    tempHand.remove(card)
        except ValueError:
            raise Exception("Attempted to play cards that are not in your hand")
        # Check ruleset to determine whether self.played_cards = all visible cards or cards that this client played.
        # todo: Create rule:  Shared_Board == True or False, it would be False for HandAndFoot, Canasta, etc...
        # but True for Liverpool and other Rummy games.
        if self.ruleset == 'HandAndFoot':
            self.rules.canPlay(prepared_cards, self.played_cards, self.round)
            for key, card_group in prepared_cards.items():
                for card in card_group:
                    self.hand_cards.remove(card)
                    self.played_cards.setdefault(key, []).append(card)
        elif self.ruleset == 'Liverpool':
            # unlike in HandAndFoot, where self.played_cards was used to check rules.
            # in Liverpool need to consider all of the played cards.
            # This will be true for all games with Shared_Board == True
            # Played cards are in visible_scards, which is obtained
            # from controller, and contains serialized cards.
            # To reduce computations, don't deserialize them until click on play cards button.
            visible_cards = [{}]
            print('in ClientState, line 104')
            for key, scard_group in visible_scards[0].items():
                card_group=[]
                for scard in scard_group:
                    # card = scard.deserialize()
                    card = Card(scard[0], scard[1], scard[2])
                    # card = 'debugging'
                    print(scard)
                    card_group.append(card)
                visible_cards[0][key]=card_group
                print(visible_cards)

            #visible_cards[0] = {key: [scard.deserialize() for scard in scard_group] for (key, scard_group) in
            #                    visible_scards[0].items()}
            self.played_cards = visible_cards[0]  # in Liverpool all players' cards are included.
            print("line 108 in ClientState.py, played_cards: ")
            for key, card_group in self.played_cards.items():
                for card in card_group:
                    print(card)
            self.rules.canPlay(prepared_cards, visible_cards, player_index, self.round)
            print("line 112 in ClientState.py, prepared cards: ")
            for key, card_group in prepared_cards.items():
                for card in card_group:
                    self.hand_cards.remove(card)
                    self.played_cards.setdefault(key, []).append(card)
                    # todo: need to sort cards here (or in Liverpool.;py)
                    #  -- have to figure out how to designate wilds nominal value.
                    # if its in the middle that's easy but Aces and wilds need to be set high or low.
                    # can do that in a separate method...
            # unlike HandAndFoot, self.played_cards includes cards played by everyone.

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
