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
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        """Called when a player disconnects"""
        print(self, 'Client disconnected')    

    ##################################
    ### Network specific callbacks ###
    ##################################

    def Network(self, data):
        """ Fallback method to recieve data from a client
        We treat these as bad messages and log them for debugging
        """
        print('Recieved invalid data from client:', data)


class GameServer(Server):
    channelClass = PlayerChannel

    def __init__(self, *args, **kwargs):
        """This overrides the library server init
        It's a place to do any 'on launch' actions for the server
        """
        Server.__init__(self, *args, **kwargs)
        print('Server launched')

    def Connected(self, channel, addr):
        """Called when a client connects and establishes a channel"""
        print(channel, "Channel connected")

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

# get command line argument of server, port
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    s = GameServer(localaddr=(host, int(port)))
    s.Launch()
