class ClientState():
    """ This class store client state for access by different listeners

    It tracks things like 'interactivity', a player's hand,
    It stores what is needed to compute scores and decide on move legality
    """

    def __init__(self):
        """ initialize a state tracker for a given client """
        self.interactive = False #Wait for server to start turn
        self.name = "guest"
        self.hand_cards = []
        self.visible_cards = []

    def NewCards(cardList):
        """Update the cards in hand"""
        self.hand_cards.append(cardList)

    def PlayCards(cardList):
        """Move cards from hand to visible"""
        for card in cardList:
            self.hand_cards.remove(card)
            self.visible_cards.append(card)

    def DiscardCards(cardList):
        for card in cardList:
            self.hand_cards.remove(card)
