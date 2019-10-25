import sys
from time import sleep
from PodSixNet.Connection import connection
from client.Controller import Controller
from client.ClientState import ClientState
from client.CreateDisplay import CreateDisplay
from client.HandView import HandView
from client.TableView import TableView

def RunClient():
    """This is the launch point for the client.
    
    It sets up the various classes and starts the game loop
    """
    host, port = sys.argv[1].split(":")
    ruleset = sys.argv[2]
    connection.DoConnect((host, int(port)))
    clientState = ClientState(ruleset)
    gameControl = Controller(clientState)
    playername = gameControl.getName()
    createDisplay = CreateDisplay(playername)
    handView = HandView(gameControl, createDisplay.display)
    tableView = TableView(createDisplay.display)
    while True:
        createDisplay.refresh()
        handView.nextEvent()
        connection.Pump()
        gameControl.Pump()
        tableView.Pump()
        handView.update()
        tableView.playerByPlayer()
        note = gameControl.note
        createDisplay.render(note)
        sleep(0.001)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "host:port ruleset")
        print("e.g.", sys.argv[0], "localhost:31425 HandAndFoot")
    else:
        RunClient()
else:
    print("RunServer should not be imported anywhere")
