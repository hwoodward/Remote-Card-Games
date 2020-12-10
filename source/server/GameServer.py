from server.PlayerChannel import PlayerChannel
from server.ServerState import ServerState

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from time import time, sleep


class GameServer(Server, ServerState):
    channelClass = PlayerChannel

    def __init__(self, localaddr, ruleset, startinground):
        """This overrides the library server init
        It's a place to do any 'on launch' actions for the server
        """
        Server.__init__(self, localaddr=localaddr)
        ServerState.__init__(self, ruleset)
        self.starting_round = int(startinground)
        self.players = []
        self.in_round = False
        self.game_over = False
        if self.rules.Shared_Board:      #  True for Liverpool, False for HandAndFoot.
            self.visible_cards_now = {}
        print('Server launched')

    def Connected(self, channel, addr):
        """Called by podsixnet when a client connects and establishes a channel"""
        if self.in_round:
            print(channel, 'Client tried to connect during active round, try again between rounds')
            channel.Send({"action": "connectionDenied"})
        else:
            self.players.append(channel)
            self.Send_publicInfo()
            print(channel, "Client connected")
            if self.round >= 0:
                print(channel, 'a client joined between rounds')

    def disconnect(self, channel):
        """Called by a channel when it disconnects"""
        if channel not in self.players:
            #Disconnecting a channel that never fully joined the game, do nothing
            return
        #For players who did join the game need to handle removing them safely
        self.delPlayer(channel)
         
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
        if self.round == -1:
            self.round = self.starting_round
        else:
            self.round += 1
        self.in_round = True
        if self.round > self.rules.Number_Rounds-1: #Need to take one off Number_Rounds because we index from zero
            #Game is over
            print("GAME OVER - CHECK LAST SCORE REPORT FOR FINAL RESULT")
            self.game_over = True
        self.prepareRound(len(self.players))
        for player in self.players:
            player.Send_deal(self.dealHands(), self.round)
        self.Send_scores()              # need to retransmit all the scores in case a player has joined between rounds
        self.turn_index = self.round    # define which player starts the next round.
        self.nextTurn()

    def delPlayer(self, player):
        """Safely remove a player from the turn order
        
        Checks for game over if no more players and quits server
        Moves turn forward if it was deleted players turn
        """
        player_index = self.players.index(player)
        self.players.remove(player)
        self.Send_publicInfo()
        #Check for no more players
        if len(self.players) == 0:
            self.game_over = True
            return
        #Check if it was deleted players turn and if so, make sure next player can start
        if self.turn_index == player_index and self.in_round:
            self.turn_index = self.turn_index % len(self.players) 
            self.players[self.turn_index].Send({"action": "startTurn"})


    def nextTurn(self):
        """Advance to the next turn"""
        newIndex = (self.turn_index + 1) % len(self.players)
        self.turn_index = newIndex
        self.players[self.turn_index].Send({"action": "startTurn"})
        if self.rules.Buy_Option:
            self.Send_buyingOpportunity()

    def cardBuyingResolution(self):
        """ Resolve who gets to purchase card for games with Buy_Option = True
        This is called upon player clicking on draw pile. """
        timelimit = time() + self.rules.purchase_time
        buying_phase = True # else this routine would not be called
        i_max = len(self.players) - 2
        index = (self.turn_index + 1) % len(self.players)
        icount = 0
        while buying_phase and icount < i_max:
            while self.players[index].want_card is None and time() < timelimit:
                # wait patiently(?) while updating information from players, timer begins when
                # next player attempts to draw.
                self.Pump()
                sleep(0.0001)
            if self.players[index].want_card:
                self.Send_buyingResult(self.players[index].name)
                # send cards
                cards = self.players[index]._server.drawCards()   # note number of cards is same as DrawSize
                cards = cards + self.players[index]._server.pickUpPile()   # number of cards is same as Pickup_Size
                self.players[index].Send_newCards(cards)
                self.Send_discardInfo()
                buying_phase = False
            index = (index + 1) % len(self.players)
            icount = icount + 1

    ######################################################

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

        #NOTE: visible_cards needs to be serialized form to be transmitted.
        # On server keep them in serialized form.

        if self.rules.Shared_Board:
            # Shared_Board is True: (e.g. Liverpool) - each player can play on any players cards.
            self.v_cards = [p.visible_cards for p in self.players]
            if len(self.v_cards) == 0:
                self.v_cards = [{}]
            # v_cards contains a dictionary from each player/client
            # each dictionary contains all the played cards that player/client is aware of.
            # set self.visible_cards_now to the dictionary in v_cards with the most cards.
            #
            # todo: consider whether checking the length is the best way to determine which dictionary is most
            # recent version of visible_cards.
            max_len = -1
            self.visible_cards_now = {}
            for v_cards_dict in self.v_cards:
                temp_length = 0
                for key, scard_group in v_cards_dict.items():
                    temp_length = temp_length + len(scard_group)
                if temp_length > max_len:
                    self.visible_cards_now = v_cards_dict
                    max_len = temp_length
            # Next line must be long (no line breaks) or it doesn't work properly.
            self.Send_broadcast({"action": "publicInfo", "player_names": [p.name for p in self.players],"visible_cards": [self.visible_cards_now],"hand_status": [p.hand_status for p in self.players]})
        else:
            # Shared_Board is False: (e.g. HandAndFoot) -- each player can only play on their own cards.
            # Next line must be long (no line breaks) or it doesn't work properly.
            self.Send_broadcast({"action": "publicInfo", "player_names": [p.name for p in self.players], "visible_cards": [p.visible_cards for p in self.players], "hand_status": [p.hand_status for p in self.players]})


    def Send_pickUpAnnouncement(self, name, top_card):
            self.Send_broadcast({"action": "pickUpAnnouncement", "player_name": name, "top_card": top_card.serialize()})

    def Send_discardInfo(self):
        """Send the update to the discard pile"""
        info = self.getDiscardInfo()
        self.Send_broadcast({"action": "discardInfo", "top_card": info[0].serialize(), "size": info[1]})

    def Send_buyingOpportunity(self):
        """ Let eligible players know there's a buying opportunity

        Used in games with with Buy_Option = True (i.e. Liverpool)
        where you can buy the top discard if the next player doesn't want
        it.  If there are N players, then N-2 players are eligible to buy card
        (neither player who discarded, nor current active player are eligible).
        """
        for p in self.players:
            p.want_card = None     # reset all buying responses to None
        info = self.getDiscardInfo()
        i_max = len(self.players) - 2
        for i_count in range(i_max):
            index = (self.turn_index + i_count + 1) % len(self.players)
            self.players[index].Send({"action": "buyingOpportunity", "top_card": info[0].serialize()})

    def Send_buyingResult(self, buyer):
        """ Broadcast who purchased what card in last auction."""
        info = self.getDiscardInfo()  # be sure to send this before giving the player the top card.
        self.Send_broadcast({"action": "buyingResult", "top_card": info[0].serialize(), "buyer": buyer})

