import importlib

class ClientState():
    """ This class store client state for access by different listeners

    It tracks things like 'interactivity', a player's hand, discard state, etc.
    It stores what is needed to compute scores and decide on move legality
    """

    def __init__(self, ruleset):
        """Initialize a state tracker for a given client"""
        ruleModule = "common." + ruleset
        self.Rules = importlib.import_module(ruleModule)
        self.interactive = False #Wait for server to start turn
        self.name = "guest"
        self.hand_cards = []
        self.discardInfo = (None, 0) #This is topCard and then size

    def NewCards(self, cardList):
        """Update the cards in hand"""
        for card in cardList:
            self.hand_cards.append(card)

    def PlayCards(self, cardList):
        """Move cards from hand to visible"""
        #TODO: verify this is a legal move
        for card in cardList:
            self.hand_cards.remove(card)
            self.visible_cards.append(card)

    def discardCards(self, cardList):
        """Discard cards from hand"""
        #Note: remove errors if you don't have that card
        for card in cardList:
            self.hand_cards.remove(card)

    def UpdateDiscardInfo(self, topCard, size):
        """Update the discard information"""
        self.discardInfo = (topCard, size)
