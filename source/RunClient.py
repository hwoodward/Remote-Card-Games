import sys
from time import sleep
from PodSixNet.Connection import connection, ConnectionListener
from client.ClientState import ClientState
from client.Controller import Controller
from client.CreateDisplay import CreateDisplay
from client.HandView import HandView
from client.TableView import TableView
# need to import the following here makes it easier to get pyinstaller to work.
import common.HandAndFoot
import common.Card
import client.Button
import client.ClickableImage
import client.UICardWrapper
import client.UIConstants


def RunClient():
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)
    """This is the launch point for the client.
    
    It sets up the various classes and starts the game loop
    """
    # ruleset = sys.argv[2]
    ruleset = "HandAndFoot"
    hostinfo = str(input("Enter the host:port[localhost:12345] ") or "localhost:12345")
    host, port = hostinfo.split(":")
    print(host)
    print(port)
    ruleset = str(input("Enter the ruleset[HandAndFoot] ") or "HandAndFoot")
    print(ruleset)
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
    '''
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "host:port ruleset")
        print("e.g.", sys.argv[0], "localhost:31425 HandAndFoot")
    else:
        RunClient()
    '''
    if len(sys.argv) != 1:
        print("This version gets hardcoded host:port and RuleSet after starting.")
        print("Do not include any arguments on command line")
    else:
        RunClient()
else:
    print("RunServer should not be imported anywhere")
