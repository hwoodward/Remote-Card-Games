from common.Card import Card

from PodSixNet.Connection import connection, ConnectionListener

#TODO: figure out where this should actually live
Turn_Phases = ['inactive', 'draw', 'forcedAction', 'play']

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

    def discard(self, discard_list):
        """Send discard to server"""
        if self._state.turn_phase != Turn_Phases[3]:
            self.note = "You can only discard at the end of your turn (after having drawn)"
            return
        self._state.discardCards(discard_list)
        connection.Send({"action": "discard", "cards": [c.serialize() for c in discard_list]})
        self.turn_phase = Turn_Phases[0] #end turn after discard
        self.sendPublicInfo()

    def draw(self):
        """Request a draw from the server"""
        if self._state.turn_phase != Turn_Phases[1]:
            self.note = "You can only draw at the start of your turn"
            return
        connection.Send({"action": "draw"})
    
    def pickUpPile(self):
        """Attempt to pick up the pile"""
        if self._state.turn_phase != Turn_Phases[1]:
            self.note = "You can only pick up the pile at the start of your turn"
            return
        #TODO: call clientstate to confirm legality of pickup
        #TODO: call server to get new cards
        self.turn_phase = Turn_Phases[2] #Set turn phase to reflect forced action
        self.note = "Waiting for new cards to make required play"

    def makeForcedPlay(self, top_card):
        """Complete the required play for picking up the pile"""
        self.note = "Performing the play required to pick up the pile"
        #TODO: add top_card to prepared cards (it should be able to be automatically given a key)
        self.play()
        
    def play(self):
        """Send the server the current set of visible cards"""
        if self._state.turn_phase != Turn_Phases[3]:
            self.note = "You can only play on your turn after you draw"
            return
        self._state.playCards(self.prepared_cards)
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
        self._state.turn_phase = Turn_Phases[1]
        self.note = "Your turn has started. You may draw or attempt to pick up the pile"
        self.sendPublicInfo() #Let everyone know its your turn.

    def Network_newCards(self, data):
        card_list = [Card.deserialize(c) for c in data["cards"]]
        self._state.newCards(card_list)
        if self._state.turn_phase == Turn_Phases[2]:
            #This is the result of a pickup and we have a forced action
            self.makeForcedPlay(card_list[0])
        #Now ready to be in play turn phase
        self._state.turn_phase = Turn_Phases[3]
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