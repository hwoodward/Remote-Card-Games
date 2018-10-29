import sys
from time import sleep

from PodSixNet.Server import Server
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
    ### Network specific callbacks ###
    ##################################

    def Network(self, data):
        """ Fallback method to recieve data from a client
        We treat these as bad messages and log them for debugging
        """
        print('Recieved invalid data from client:', data)

    def Network_displayName(self, data):
        """Player submitted their displayName"""
        self.name = data['name']
        self._server.SendTurnOrder()
        

class GameServer(Server):
    channelClass = PlayerChannel

    def __init__(self, *args, **kwargs):
        """This overrides the library server init
        It's a place to do any 'on launch' actions for the server
        """
        Server.__init__(self, *args, **kwargs)
        self.players = []
        self.active_game = False
        print('Server launched')

    def Connected(self, channel, addr):
        """Called when a client connects and establishes a channel"""
        if (self.active_game):
            channel.Send({"action": "connectionDenied"})
        else:
            self.players.append(channel)
            self.SendTurnOrder()
            print(channel, "Channel connected")

    def SendTurnOrder(self):
        """Adds a player to the end of the turn order"""
        self.SendToAll({"action": "turnOrder", "players": [p.name for p in self.players]})

    def DelPlayer(self, player):
        """Remove a player from the turn order"""
        self.players.remove(player)
        self.SendTurnOrder();

    def SendToAll(self, data):
        """Send data to every connected player"""
        [p.Send(data) for p in self.players]
    
# get command line argument of server, port
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    server = GameServer(localaddr=(host, int(port)))
    while True:
        server.Pump()
        sleep(0.0001)
