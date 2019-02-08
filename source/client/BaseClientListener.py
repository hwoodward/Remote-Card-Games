from PodSixNet.Connection import connection, ConnectionListener

class BaseListener(ConnectionListener):
    """ This client connects to a GameServer which will host a cardgame

    Currently the client is incomplete

    The client displays the game state it recieves from the server
    It validates and submits player actions to the server during the player's turn
    It submits its score on round or game end
    """

    def __init__(self, clientState):
        self._state = clientState
        self.setName()

    ### Player Actions ###
    def setName(self):
        """Set up a display name and send it to the server"""
        displayName = input("Select a display name: ")
        self._state.name = displayName
        connection.Send({"action": "displayName", "name": displayName})

    def discard(self, discardList):
        """Send discard to server"""
        self._state.interactive = False #turn is over
        connection.Send({"action": "discard", "cards": discardList})

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
        self._state.interactive = True
        print("Turn started")
