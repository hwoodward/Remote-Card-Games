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
        # Will need to know player index in Liverpool because prepare cards buttons shared, but designated player
        # has to initiate play in that player's sets and runs.
        self.player_index = 0 # needed for Liverpool, will update when play cards.
        self.reset()  # Start with state cleared for a fresh round

    def getPlayerIndex(self, player_names):
        """This will udpate player index if another player drops out. """
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
        self.played_cards = {}    # in HandAndFoot this is dictionary of cards played by this client.
        #                           in Liverpool it is a dictionary containing cards played by all cards, hence
        #                           it is derived by processing data: visible cards in visible_scards[{...}]
        # self.visible_scards = [{}]  # Liverpool:  reset this so it won't cause server to be out of date.
        self.went_out = False
        self.discard_info = [None, 0]

    def newCards(self, card_list):
        """Update the cards in hand"""
        for card in card_list:
            self.hand_cards.append(card)

    def playCards(self, prepared_cards, visible_scards=[{}], player_index=0):
        """Move cards from hand to board if play follows rules, else inform what rule is broken."""

        # First check that all the cards are in your hand.
        self.player_index = player_index
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
            # in Liverpool and other shared board games need to consider all of the played cards.
            # Played cards (in deserialized form) are in visible_scards (in serialized form), which is obtained
            # from controller.
            # (Path taken by visible_scards:
            #          Tableview gets the serialized cards every msec to keep display up to date,
            #          In handview.update tableview.visible_scards list is passed to handview.visible_scards
            #          No need to process this unless playing cards, in which case visible_scards passed
            #          to controller and then to clientState, where only list item is deserialized and put in
            #          dictionary self.played_cards
            print('in ClientState, line 104')
            for key, scard_group in visible_scards[0].items():
                card_group=[]
                for scard in scard_group:
                    card = Card(scard[0], scard[1], scard[2])
                    card_group.append(card)
                self.played_cards[key] = card_group
                print(self.played_cards)
            print('line line 112 in clientstate')
            raw_dictionary = self.played_cards
            self.played_cards = self.rules.restoreRunAssignment(raw_dictionary, self.round)
            # restoreRunAssignment processes self.played_cards that are in runs so that positions of
            # Wilds and Aces are maintained.
            # This is done in rules because it will be specific to Liverpool (other shared_board games
            # will have different rules, such as whether Aces can be both high and low...)
            print('line line 120 in clientstate')
            for key, card_group in self.played_cards.items():
                for card in card_group:
                    print(card)
                    print(card.tempnumber)
            self.rules.canPlay(prepared_cards, self.played_cards, self.player_index, self.round)
            # If no exception raised, then must put cards in order prior to transmitting them to server.
            combined_cards = self.rules.combineCardDicts(self.played_cards, prepared_cards)
            for k_group, card_group in combined_cards.items():
                if k_group[1] >= self.rules.Meld_Threshold[self.round][0]:
                    card_group.sort(key=lambda wc: wc.tempnumber)
                else:
                    print('need to sort sets')
                    # card_group.sort(key=lambda wc: wc.suit)  < jokers don't sort this way, need to remove
                    # jokers, sort the rest and then add jokers to the end.
            # unlike HandAndFoot, self.played_cards includes cards played by everyone.
            self.played_cards = combined_cards
            print("line 141 in ClientState.py, prepared cards: ")
            for key, card_group in prepared_cards.items():
                for card in card_group:
                    self.hand_cards.remove(card)


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
