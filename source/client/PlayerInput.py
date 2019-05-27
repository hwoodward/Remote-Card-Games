from common.Card import Card

from PodSixNet.Connection import connection, ConnectionListener

class BroadcastListener(ConnectionListener):
    """This class handles letting players actualy input information

    It handles the entire turn cycle
    """

    def __init__(self, gameClient):
        self.controller = gameClient        

    def Events(self):
        """This takes in player input and attempts the specified action"""
        if not self.controller.IsTurn():
            #For now simply not doing anything when it isn't the players turn
            return
        action = input("Type d to draw, and t to discard (only option is all cards)")
        if action in ['d', 'D', 'draw', 'Draw']:
            self.controller.Draw()
        elif action in ['t', 'T', 'trash', 'Trash', 'discard', 'Discard']:
            self.controller.Discard(self.controller.GetHand())
        else:
            print("not a valid action currently")

    def Render(self):
        """This should render the actual UI, for now it just prints the hand"""
        #TODO render the table info we got from the server broadcast
        print("Hand is: {0}".format(self.controller.GetHand()))
        
    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_visibleCards(self, data):
        print("Recieved an update about cards on the table")
        #TODO need to implement an internal representation to store this info

    def Network_discardInfo(self, data):
        print("Recieved an update about the discard pile")
        #TODO need to implement proper handling of this (which listener, should it be part of visible cards?)
        
