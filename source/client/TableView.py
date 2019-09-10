from common.Card import Card

from PodSixNet.Connection import connection, ConnectionListener


class TableView(ConnectionListener):
    """This class handles letting players actualy input information

    It handles the entire turn cycle
    """

    def __init__(self):
        """This currently does nothing"""
        # TODO: set up any member variables here

    ''' Screen is no longer rendered in TableView.
    def render(self):
        """This should render the actual UI, for now it just prints the hand"""
        # TODO render the table view showing the visible cards
        print("draw visible cards")
    '''

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_publicInfo(self, data):
        print("Recieved an update about cards on the table")
        # TODO either:
        # a) copy the data to the internal save you are keeping and
        #    i) rerender immediately
        #    ii) rerender when explicitly told to
        # b) call Render with the provided data and only ever rerender on new broadcast
