from PodSixNet.Connection import connection

# connect to the server - optionally pass hostname and port like: ("mccormick.cx", 31425)
connection.Connect()

# to disconnect call connection.close()
# TODO: add a listener for the server to send back a 'game in progress' action, and close if its recieved

# eventually I should look into separating this out
# possibly into a set of smaller classes
from PodSixNet.Connection import ConnectionListener

class PlayerListener(ConnectionListener):

    def Network(self, data):
        """Fallback method to recieve data from the server"""
        print('network data:', data)

    def Network_connected(self, data):
        print("connected to the server")

    def Network_error(self, data):
        print("network error:", data['error'][1])

    def Network_disconnected(self, data):
        print("disconnected from the server")

    def Network_myaction(data):
        print("myaction:", data)
