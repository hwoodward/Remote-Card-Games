from PodSixNet.Channel import Channel

class PlayerChannel(Channel):
    """ This is the server's representation of a single client"""

    def __init__(self, *args, **kwargs):
        """This overrides the lower lvl channel init
        It's a place to set any client information thats provided from the server
        """
        self.name = "guest"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        """Called when a player disconnects
        Removes player from the turn order
        """
        self._server.DelPlayer(self)
        print(self, 'Client disconnected')    

    ##################################
    ### Network callbacks ###
    ##################################

    def Network(self, data):
        """ Fallback method to recieve data from a client
        We treat these as bad messages and log them for debugging
        """
        print('Recieved invalid data from client:', data)

    def Network_displayName(self, data):
        """Player submitted their displayName"""
        self.name = data['name']
        self._server.Send_turnOrder()

    ### Player Game Actions ###

    def Network_discard(self, data):
        self._server.NextTurn()
