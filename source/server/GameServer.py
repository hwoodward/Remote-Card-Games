from server.PlayerChannel import PlayerChannel
from server.ServerState import ServerState

from PodSixNet.Server import Server

class GameServer(Server):
    channelClass = PlayerChannel

    def __init__(self, *args, **kwargs):
        """This overrides the library server init
        It's a place to do any 'on launch' actions for the server
        """
        Server.__init__(self, *args, **kwargs)
        self.players = []
        self.shared_state = ServerState()
        self.active_game = False
        self.turn_index = 0
        print('Server launched')

    def Connected(self, channel, addr):
        """Called when a client connects and establishes a channel"""
        if self.active_game:
            print(channel, 'Client tried to connect during active game')
            channel.Send({"action": "connectionDenied"})
        else:
            self.players.append(channel)
            self.Send_turnOrder()
            print(channel, "Client connected")

    def StartGame(self):
        self.active_game = True
        #TODO: need to call 'start round' here when we add dealing and rounds
        self.NextTurn()

    def DelPlayer(self, player):
        """Remove a player from the turn order"""
        self.players.remove(player)
        self.Send_turnOrder();

    def NextTurn(self):
        """Advance to the next trun"""
        newIndex = (self.turn_index + 1) % len(self.players)
        self.turn_index = newIndex
        self.SendToActive({"action": "startTurn"})
        
    def SendToAll(self, data):
        """Send data to every connected player"""
        [p.Send(data) for p in self.players]

    def SendToActive(self, data):
        """Send data to the player whose turn it is"""
        self.players[self.turn_index].Send(data)

    def Send_turnOrder(self):
        """Adds a player to the end of the turn order"""
        self.SendToAll({"action": "turnOrder", "players": [p.name for p in self.players]})
