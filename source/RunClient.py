import sys
from time import sleep

from PodSixNet.Connection import connection
from client.BaseClientListener import BaseListener
from client.StateTracker import ClientState

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    connection.DoConnect((host, int(port)))
    clientState = ClientState()
    gameClient = BaseListener(clientState)
    while 1:
        connection.Pump()
        gameClient.Pump()
        sleep(0.001)

