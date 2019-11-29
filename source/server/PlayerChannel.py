from common.Card import Card
from PodSixNet.Channel import Channel

class PlayerChannel(Channel):
    """This is the server's representation of a single client"""

    def __init__(self, *args, **kwargs):
        """This overrides the lower lvl channel init
        It's a place to set any client information thats provided from the server
        """
        self.name = "guest"
        #visible cards and hand status are public info
        self.visible_cards = {}
        self.hand_status = [] #order of information in this is specified by the ruleset
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        """Called when a player disconnects
        Removes player from the turn order
        """
        if self._server.round == -1:
            self._server.delPlayer(self)
            print(self, 'Client disconnected')
        else:
            print(self, 'Client disconnected during active game')

    def Send_newCards(self, cards):
        """Serialize cards and format json to send newCards from a draw or pile pickup""" 
        serialized = [c.serialize() for c in cards]
        self.Send({"action": "newCards", "cards": serialized})

    def Send_deal(self, dealtCards):
        """Serialize and format json to send deal at start of round"""
        serializedDeal = [[c.serialize() for c in hand] for hand in dealtCards]
        self.Send({"action": "deal", "hands": serializedDeal})

    ##################################
    ### Network callbacks          ###
    ##################################

    def Network_displayName(self, data):
        """Player submitted their display name"""
        self.name = data['name']
        self._server.Send_turnOrder()

    ### Player Game Actions ###

    def Network_discard(self, data):
        card_list = [Card.deserialize(c) for c in data["cards"]]
        self._server.discardCards(card_list)
        self._server.Send_discardInfo()
        self._server.nextTurn()

    def Network_draw(self, data):
        cards = self._server.drawCards()
        self.Send_newCards(cards)

    #TODO: add pickup pile action
    
    ### Visible card updates ###
    def Network_publicInfo(self, data):
        """This is refreshed public information data from the client"""
        self.visible_cards = data["visible_cards"]
        self.hand_status = data["hand_status"]
        self._server.Send_publicInfo()
