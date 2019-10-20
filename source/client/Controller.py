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

    def draw(self):
        """Request a draw from the server"""
        connection.Send({"action": "draw"})

    def play(self, cardSet):
        """Send the server the current set of visible cards"""
        self._state.playCards(cardSet)
        serialized = [c.serialize() for c in self._state.visible_card]
        #TODO: hand status is state information and order specified in ruleset - need to make helpers for handling it still
        connection.Send({"action": "publicInfo", "visible_cards":serialized, "hand_status":[]})
        #TODO: Check for turn transition due to out or zephod

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

    def Network_newCards(self, data):
        cardList = [Card.deserialize(c) for c in data["cards"]]
        self._state.newCards(cardList)

    def Network_discardInfo(self, data):
        top_card = Card.deserialize(data["top_card"])
        size = data["size"]
        self._state.updateDiscardInfo(top_card, size)

    ### Check user's actions, and remind them of rules as necessary ###
    def discardLogic(self, confirmed, discards):
        self.discards = discards
        self.numbercards = len(discards)
        if not confirmed:
            # for other games may wish to have alternate discard rules.
            # here discard = 1 unless len(hand)==0. < ==this has been submitted as an issue.
            # to address issue will also need to update "self.note = " statements below.
            if len(self._state.hand_cards) == 0:
                self.discard(self.discards)
                self.note = "Zaephod - no discard required, turn is over"
                please_confirm = False
            else:
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