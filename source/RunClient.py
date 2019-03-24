import sys
from time import sleep

from PodSixNet.Connection import connection
from client.BaseClientListener import PersonalListener
from client.PlayerInput import BroadcastListener
from client.StateTracker import ClientState

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    connection.DoConnect((host, int(port)))
    clientState = ClientState()
    gameClient = PersonalListener(clientState)
    playerInterface = BroadcastListener(gameClient)
    while 1:
        playerInterface.Events()
        connection.Pump()
        gameClient.Pump()
        playerInterface.Pump()
        playerInterface.Render()
        sleep(0.001)

