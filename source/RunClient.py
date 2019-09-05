import sys
from time import sleep

from PodSixNet.Connection import connection
from client.Controller import Controller
from client.TableView import TableView
from client.HandView import HandView
from client.ClientState import ClientState
#TODO: consistent import ordering for ease of finding stuff

def RunClient():
    """This is the launch point for the client.
    
    It sets up the various classes and starts the game loop
    """
    host, port = sys.argv[1].split(":")
    ruleset = sys.argv[2]
    connection.DoConnect((host, int(port)))
    clientState = ClientState(ruleset)
    gameControl = Controller(clientState)
    handView = HandView(gameControl)
    tableView = TableView()
    while 1:
        handView.Next_Event()
        connection.Pump()
        gameControl.Pump()
        tableView.Pump()
        handView.Render()
        sleep(0.001)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "host:port ruleset")
        print("e.g.", sys.argv[0], "localhost:31425 HandAndFoot")
    else:
        RunClient()
else:
    print("RunServer should not be imported anywhere")
