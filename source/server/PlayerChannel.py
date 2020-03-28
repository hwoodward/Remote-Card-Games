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
        self.scores = []
        self.ready = False #for consensus transitions
        Channel.__init__(self, *args, **kwargs)

    def scoreForRound(self, round):
        """Handles getting score for round so we don't error if this player hasn't reported yet"""
        try:
            return self.scores[round]
        except:
            return None
        
    def Close(self):
        """Called when a player disconnects
        Removes player from the turn order
        """
        self._server.disconnect(self)
        print(self, 'Client disconnected')

    def Send_newCards(self, cards):
        """Serialize cards and format json to send newCards from a draw or pile pickup""" 
        serialized = [c.serialize() for c in cards]
        self.Send({"action": "newCards", "cards": serialized})

    def Send_deal(self, dealtCards, round):
        """Serialize and format json to send deal at start of round"""
        serializedDeal = [[c.serialize() for c in hand] for hand in dealtCards]
        self.Send({"action": "deal", "hands": serializedDeal, "round": round})

    ##################################
    ### Network callbacks          ###
    ##################################

    def Network_displayName(self, data):
        """Player submitted their display name"""
        self.name = data['name']
        self._server.Send_publicInfo()

    def Network_ready(self, data):
        """Player changed their ready state"""
        self.ready = data['state']
        self._server.checkReady()

    ### Player Game Actions ###
    def Network_discard(self, data):
        card_list = [Card.deserialize(c) for c in data["cards"]]
        self._server.discardCards(card_list)
        self._server.Send_discardInfo()
        self._server.nextTurn()

    def Network_draw(self, data):
        cards = self._server.drawCards()
        self.Send_newCards(cards)

    def Network_pickUpPile(self, data):
        cards = self._server.pickUpPile()
        self.Send_newCards(cards)
        self._server.Send_discardInfo()
    
    def Network_goOut(self, data):
        self._server.Send_endRound(self.name)
        self._server.in_round = False
        
    ### Score reports ###
    def Network_reportScore(self, data):
        score = data["score"]
        self.scores.append(score)
        self._server.Send_scores()
        #Clear out visible cards since the round is over (This clear won't be broadcast until later)
        self.visible_cards = {}
        #In case everyone is already ready to go and don't want to analyze:
        self._server.checkReady()
        
    ### Visible card updates ###
    def Network_publicInfo(self, data):
        """This is refreshed public information data from the client"""
        self.visible_cards = data["visible_cards"]
        self.hand_status = data["hand_status"]
        self._server.Send_publicInfo()
