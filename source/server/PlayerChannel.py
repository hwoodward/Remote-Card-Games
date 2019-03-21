from PodSixNet.Channel import Channel

class PlayerChannel(Channel):
    """This is the server's representation of a single client"""

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
        if not self._server.active_game:
            self._server.DelPlayer(self)
            print(self, 'Client disconnected')
        else:
            print(self, 'Client disconnected during active game')

    ##################################
    ### Network callbacks          ###
    ##################################

    def Network_displayName(self, data):
        """Player submitted their displayName"""
        self.name = data['name']
        self._server.Send_turnOrder()

    ### Player Game Actions ###

    def Network_discard(self, data):
        self._server.shared_state.discard(data["cards"])
        self._server.NextTurn()

    def Network_draw(self):
        #TODO: adjust where draw number comes from
        cards = self._server.shared_state.draw(1)
        self._server.SendToActive({"action": "newCards", "cards": cardList})
