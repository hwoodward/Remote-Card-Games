from common.Card import Card

from PodSixNet.Connection import connection, ConnectionListener

class Controller(ConnectionListener):
    """ This client connects to a GameServer which will host a cardgame

    Currently the client is incomplete

    The client displays the game state it recieves from the server
    It validates and submits player actions to the server during the player's turn
    It submits its score on round or game end
    """

    def __init__(self, clientState):
        self.state = clientState
        self.SetName()

    ### Player Actions ###
    def SetName(self):
        """Set up a display name and send it to the server"""
        displayName = input("Select a display name: ")
        self.state.name = displayName
        connection.Send({"action": "displayName", "name": displayName})

    def Discard(self, discardList):
        """Send discard to server"""
        self.state.DiscardCards(discardList)
        self.state.interactive = False #turn is over
        connection.Send({"action": "discard", "cards": [c.serialize() for c in discardList]})

    def Draw(self):
        """Request a draw from the server"""
        connection.Send({"action": "draw"})

    def Play(self, cardSet):
        """Send the server the current set of visible cards"""
        self.state.PlayCards(cardSet)
        serialized = [c.serialize() for c in self.state.visible_card]
        connection.Send({"visibleCards": serialized})

    def Get_Name(self):
        """return player name for labeling"""
        return self.state.name

    def Get_Hand(self):
        """sends state to UI"""
        return self.state.hand_cards.copy()

    def Is_Turn(self):
        """return if the player should be active"""
        return self.state.interactive

    def GetDiscardInfo(self):
        """let the UI know the discard information"""
        return self.state.discardInfo.copy()

    #######################################
    ### Network event/message callbacks ###
    #######################################
    # built in stuff
    
    def Network_connected(self, data):
        print("Connected to the server")
    
    def Network_error(self, data):
        print('error:', data['error'])
        connection.Close()
    
    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

    ### Setup messages ###
    def Network_connectionDenied(self, data):
        """Server denied the connection, likely due to a game already in progress"""
        print('Server denied connection request')
        connection.Close()

    def Network_turnOrder(self, data):
        """Turn order changed"""
        print('Turn order is', data['players'])

    ### Gameplay messages ###
    def Network_startTurn(self, data):
        self.state.interactive=True

    def Network_newCards(self, data):
        cardList = [Card.deserialize(c) for c in data["cards"]]
        self.state.NewCards(cardList)

    def Network_discardInfo(self, data):
        topCard = Card.deserialize(data["topCard"])
        size = data["size"]
        self.state.UpdateDiscardInfo(topCard, size)
