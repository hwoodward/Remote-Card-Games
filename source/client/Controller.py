from common.Card import Card

from PodSixNet.Connection import connection, ConnectionListener

class Controller(ConnectionListener):
    """ This client connects to a GameServer which will host a cardgame

    Currently the client is incomplete

    The client displays the game _state it receives from the server
    It validates and submits player actions to the server during the player's turn
    It submits its score on round or game end
    """

    def __init__(self, clientState):
        self._state = clientState
        self.prepared_cards = {} #This is the dict of cards prepared to be played
        self.setName()
        self.note = "Game is beginning."

    ### Player Actions ###
    def setName(self):
        """Set up a display name and send it to the server"""
        displayName = input("Select a display name: ")
        self._state.name = displayName
        connection.Send({"action": "displayName", "name": displayName})

    def discard(self, discardList):
        """Send discard to server"""
        self._state.discardCards(discardList)
        self._state.turn_phase = False #this is changing to a phase advancement
        connection.Send({"action": "discard", "cards": [c.serialize() for c in discardList]})
        self.sendPublicInfo()

    def draw(self):
        """Request a draw from the server"""
        connection.Send({"action": "draw"})

    def play(self, cardSet):
        """Send the server the current set of visible cards"""
        self._state.playCards(cardSet)
        #TODO: Check for turn transition due to out or zephod
        self.sendPublicInfo()

    def getName(self):
        """return player name for labeling"""
        return self._state.name

    def getHand(self):
        """sends _state to UI"""
        return self._state.hand_cards.copy()

    def getTurnPhase(self):
        """return if the player should be active"""
        return self._state.turn_phase

    def getDiscardInfo(self):
        """let the UI know the discard information"""
        return self._state.discard_info.copy()
    
    def sendPublicInfo(self):
        """Utility method to send public information to the server"""
        serialized_cards = {key:[card.serialize() for card in card_group] for (key, card_group) in self._state.played_cards.items()}
        status_info = self._state.getHandStatus()
        connection.Send({"action": "publicInfo", "visible_cards":serialized_cards, "hand_status":status_info})

    #######################################
    ### Network event/message callbacks ###
    #######################################
    
    ### built in stuff ###
    def Network_connected(self, data):
        print("Connected to the server")
        self.note = "Connected to the server!"
    
    def Network_error(self, data):
        print('error:', data['error'])
        connection.Close()
    
    def Network_disconnected(self, data):
        print('Server disconnected')
        self.note = "Disconnected from the server :("
        exit()

    ### Setup messages ###
    def Network_connectionDenied(self, data):
        """Server denied the connection, likely due to a game already in progress"""
        print('Server denied connection request')
        self.note = "Server denied connection request :("
        connection.Close()

    def Network_turnOrder(self, data):
        """Turn order changed"""
        print('Turn order is', data['players'])

    ### Gameplay messages ###
    def Network_startTurn(self, data):
        self._state.turn_phase=True #This is going to change to a phase advancement
        self.sendPublicInfo() #Let everyone know its your turn.

    def Network_newCards(self, data):
        card_list = [Card.deserialize(c) for c in data["cards"]]
        self._state.newCards(card_list)
        self.sendPublicInfo() #More cards in hand now, need to update public information
    
    def Network_deal(self, data):
        hand_list = [[Card.deserialize(c) for c in hand] for hand in data["hands"]]
        #TODO: we want to allow the player to choose the order of the hands eventually
        self._state.dealtHands(hand_list)
        self.sendPublicInfo() #More cards in hand now, need to update public information

    def Network_discardInfo(self, data):
        top_card = Card.deserialize(data["top_card"])
        size = data["size"]
        self._state.updateDiscardInfo(top_card, size)

    ### Check user's actions, and remind them of rules as necessary ###
    #TODO: this needs slight refactor to move and to implement intended confirmation procedure and error catching
    #May be combined somewhat with existing discard method depending on confirmation method
    def discardLogic(self, confirmed, discards):
        self.discards = discards
        self.numbercards = len(discards)
        if not confirmed:
            # for other games may wish to have alternate discard rules.
            # here discard = 1 unless len(hand)==0. < ==this has been submitted as an issue.
            # to address issue will also need to update "self.note = " statements below.

            if self.numbercards == 1:
                self.note = "Please confirm - discard  " + "{0}".format(self.discards)
                self.discards_to_confirm = self.discards
                please_confirm = True  # ask for confirmation
            else:
                self.note = "Precisely one card must be selected to discard. "
                please_confirm = False
        else:
            # confirmed is True
            if self.discards == self.discards_to_confirm:
                self.discard(self.discards)
                self.note = "Discard complete, your turn is over. "
            else:
                self.note = "Discard selection changed, discard canceled. "
            please_confirm = False
        return please_confirm, self.note