class ClientState():
    """ This class store client state for access by different listeners

    It tracks things like 'interactivity', a player's hand,
    It stores what is needed to compute scores and decide on move legality
    """

    def __init__(self):
        """ initialize a state tracker for a given client """
        self.interactive = False #Wait for server to start turn
        self.name = "guest"
