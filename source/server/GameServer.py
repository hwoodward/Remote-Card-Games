from server.PlayerChannel import PlayerChannel

from PodSixNet.Server import Server

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
