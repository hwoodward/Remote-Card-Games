import importlib

class ClientState():
    """ This class store client state for access by different listeners

    It tracks things like 'interactivity', a player's hand, discard state, etc.
    It stores what is needed to compute scores and decide on move legality
    """

    def __init__(self, ruleset = None):
        """Initialize a state tracker for a given client"""
        if ruleset != None:
            rule_module = "common." + ruleset
        else:
            #This is the unit test case - we may want to put a dummy ruleset in
            print("In unittest mode - using HandAndFoot rules")
            rule_module = "common.HandAndFoot"

        self.rules = importlib.import_module(rule_module)
        #TODO: turn phase should go from "is my turn" boolean to 'drawing, playing, not my turn anymore' indicator 
        # can hard code turn phases b/c this will only play games fitting that mode. If we ever make a trick game it will need its own app (although code can probably be reused)
        self.turn_phase = False
        self.name = "guest"
        self.hand_list = []
        self.hand_cards = []
        self.played_cards = {}
        self.discard_info = (None, 0) #This is top_card and then size

    def dealtHands(self, hands):
        """Store the extra hands dealt to player for use after first hand is cleared"""
        self.newCards(hands[0])
        self.hand_list = hands[1:]
        
    def newCards(self, card_list):
        """Update the cards in hand"""
        for card in card_list:
            self.hand_cards.append(card)

    def playCards(self, prepared_cards):
        """Move cards from hand to visible"""
        #TODO: verify this is a legal move
        for key, card_group in prepared_cards.items():
            for card in card_group:
                self.hand_cards.remove(card)
                self.played_cards.setdefault(key, []).append(card)

    def discardCards(self, card_list):
        """Discard cards from hand"""
        #Note: remove errors if you don't have that card
        for card in card_list:
            self.hand_cards.remove(card)

    def updateDiscardInfo(self, top_card, size):
        """Update the discard information"""
        self.discard_info = (top_card, size)
    
    def getHandStatus(self):
        """Returns the bundled public information that should be broadcast to the server"""
        ### Public info has a hard coded order for interpretation - see the wiki to make sure it is kept consistent
        return [self.turn_phase, len(self.hand_cards), len(self.hand_list)]
