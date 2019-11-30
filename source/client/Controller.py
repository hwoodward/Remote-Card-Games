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
        try:
            self._state.discardCards(discard_list)
        except Exception as err:
            self.note = "{0}".format(err)
            return
        connection.Send({"action": "discard", "cards": [c.serialize() for c in discard_list]})
        self.turn_phase = Turn_Phases[0] #end turn after discard
        self.note = "Discard completed. Your turn is over."
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

    def automaticallyPrepareCards(self, selected_cards):
        """Prepare selected cards to be played
        
        Fully prepares natural cards
        Returns options for where to play wild cards
        Returns message that you can't play 3s
        """
        if self._state.turn_phase == Turn_Phases[2]:
            self.note = "You can't change prepared cards while waiting to finish picking up the pile"
            return

        user_input_cards = []
        for card in selected_cards:
            key_opts = []
            try:
                key_opts = self._state.getValidKeys(card)
            except Exception as err:
                #This note will probably be overwritten before the user sees it, unless they try to prepare only 3s
                self.note = "Did not prepare card: {0}".format(err) 
            else:
                if len(key_opts) == 1:
                    self.prepareCard(key_opts[0], card) #Automatically prepare as much as possible
                else:
                    user_input_cards.append([card, key_opts])
        return user_input_cards
        
    def prepareCard(self, key, card):
        """Prepare the selected card with the specified key"""
        if self._state.turn_phase == Turn_Phases[2]:
            self.note = "You can't change prepared cards while waiting to finish picking up the pile"
            return
        self.prepared_cards.setdefault(key, []).append(card)
        self.note = "You have the following cards prepared to play: {0}".format(self.prepared_cards) #Is this format readable enough?
        
    def clearPreparedCards(self):
        """Clears prepared cards"""
        if self._state.turn_phase == Turn_Phases[2]:
            self.note = "You can't change prepared cards while waiting to finish picking up the pile"
            return
        self.prepared_cards = {}
        self.note = "You have no cards prepared to play"
        
    def play(self):
        """Send the server the current set of visible cards"""
        if self._state.turn_phase != Turn_Phases[3]:
            self.note = "You can only play on your turn after you draw"
            return
        self._state.playCards(self.prepared_cards)
        self.clearPreparedCards()
        #TODO: Check for turn transition due to out or zephod
        self.sendPublicInfo()

    def getName(self):
        """return player name for labeling"""
        return self._state.name

    def getHand(self):
        """sends _state to UI"""
        return self._state.hand_cards.copy()

    def getPreparedCards(self):
        """lets the UI fetch prepared cards"""
        #TODO: Sheri - should this information be returned in getHand or is a separate method best?
        return self.prepared_cards.copy()

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
        self.note = "You can now play cards or discard"
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
