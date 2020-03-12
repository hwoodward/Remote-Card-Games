from server.PlayerChannel import PlayerChannel
from server.ServerState import ServerState

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class GameServer(Server, ServerState):
    channelClass = PlayerChannel

    def __init__(self, localaddr, ruleset):
        """This overrides the library server init
        It's a place to do any 'on launch' actions for the server
        """
        Server.__init__(self, localaddr=localaddr)
        ServerState.__init__(self, ruleset)
        self.players = []
        self.in_round = False
        self.game_over = False
        print('Server launched')

    def Connected(self, channel, addr):
        """Called by podsixnet when a client connects and establishes a channel"""
        if self.round >= 0:
            print(channel, 'Client tried to connect during active game')
            channel.Send({"action": "connectionDenied"})
        else:
            self.players.append(channel)
            self.Send_publicInfo()
            print(channel, "Client connected")

    def disconnect(self, channel):
        """Called by a channel when it disconnects"""
        player_index = self.players.index(channel)
        self.delPlayer(channel)
        if self.turn_index == player_index:
            #It was disconnected players turn, need to send newTurn to the next player, accounting for adjusted list
            self.turn_index = self.turn_index % len(self.players) 
            self.players[self.turn_index].Send({"action": "startTurn"})
         
    def checkReady(self):
        """Confirm if all players are ready to move on to next round"""
        if self.in_round:
            return False
        player_states = [p.ready for p in self.players]
        if False not in player_states:
            self.nextRound()
            self.Send_broadcast({"action":"clearReady"}) #Reset in preparation for next round end

    def nextRound(self):
        """Start the next round of play"""
        self.round += 1
        self.in_round = True
        if self.round > self.rules.Number_Rounds:
            #Game is over
            print("GAME OVER - CHECK LAST SCORE REPORT FOR FINAL RESULT")
            self.game_over = True
        self.constructDeck(len(self.players))
        for player in self.players:
            player.Send_deal(self.dealHands(), self.round)
        #set turn index to the dealer then start play
        self.turn_index = self.round
        self.nextTurn()

    def delPlayer(self, player):
        """Remove a player from the turn order"""
        self.players.remove(player)
        self.Send_publicInfo();
        if len(self.players) == 0:
            self.game_over = True

    def nextTurn(self):
        """Advance to the next trun"""
        newIndex = (self.turn_index + 1) % len(self.players)
        self.turn_index = newIndex
        self.players[self.turn_index].Send({"action": "startTurn"})
        
    def Send_broadcast(self, data):
        """Send data to every connected player"""
        [p.Send(data) for p in self.players]

    def Send_endRound(self, player_name):
        """Notifies players that player_name has gone out and the round is over"""
        self.Send_broadcast({"action": "endRound", "player": player_name})
        
    def Send_scores(self):
        """Send the scores to all players"""
        round_scores = [p.scoreForRound(self.round) for p in self.players]
        total_scores = [sum(p.scores) for p in self.players]
        if None not in round_scores:
            self.Send_broadcast({"action": "scores", "round_scores": round_scores, "total_scores": total_scores})

    def Send_publicInfo(self):
        """Send the update to the melded cards on the table"""
        #NOTE: visible_cards needs to be serialized.
        #Current plan: never deserialize them, the client sends them in serialized and
        #we leave them serialized in the channel during storage and thus when they go out again
        self.Send_broadcast({"action": "publicInfo", "player_names": [p.name for p in self.players], "visible_cards": [p.visible_cards for p in self.players], "hand_status": [p.hand_status for p in self.players]})

    def Send_discardInfo(self):
        """Send the update to the discard pile"""
        info = self.getDiscardInfo()
        self.Send_broadcast({"action": "discardInfo", "top_card": info[0].serialize(), "size": info[1]})


