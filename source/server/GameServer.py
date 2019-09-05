from server.PlayerChannel import PlayerChannel
from server.ServerState import ServerState

from PodSixNet.Server import Server

class GameServer(Server, ServerState):
    channelClass = PlayerChannel

    def __init__(self, localaddr, ruleset):
        """This overrides the library server init
        It's a place to do any 'on launch' actions for the server
        """
        Server.__init__(self, localaddr=localaddr)
        ServerState.__init__(self, ruleset)
        self.players = []
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
        if len(self.players) == 0:
            raise Exception("Can't start a game with no players")
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

    def Send_publicInfo(self):
        """Send the update to the melded cards on the table"""
        #NOTE: visible_cards needs to be serialized.
        #Current plan: never deserialize them, the client sends them in serialized and
        #we leave them serialized in the channel during storage and thus when they go out again
        self.SendToAll({"action": "publicInfo", "visible_cards": [p.visible_cards for p in self.players], "hand_status": [p.hand_status for p in self.players]})

    def Send_discardInfo(self):
        """Send the update to the discard pile"""
        info = self.DiscardInfo()
        self.SendToAll({"action": "discardInfo", "topCard": info[0].serialize(), "size": info[1]})


