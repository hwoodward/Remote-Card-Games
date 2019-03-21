from PodSixNet.Connection import connection, ConnectionListener

class BaseListener(ConnectionListener):
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

    def Send_discard(self, discardList):
        """Send discard to server"""
        connection.Send({"action": "discard", "cards": discardList})

    def Send_draw(self):
        """Request a draw from the server"""
        #TODO need to check API doc to see if there is any data
        connection.Send({"action": "draw"})

    def Send_visibleCards(self):
        """Send the server the current set of visible cards"""
        #TODO implement me

    #TODO: this needs to take place in another class to manage waiting and interactivity
    def TakeTurn(self):
        """goes through the steps of a turn"""
        self.state.interactive = True
        print("Turn Started")
        input("Press enter to draw a card.")
        self.Draw()
        #TODO now need to wait for new cards
        input("Press enter to discard the card you drew")
        self.Discard()

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
        self.TakeTurn()

    def Network_newCards(self, data):
        self.state.NewCards(data['cards'])
        
