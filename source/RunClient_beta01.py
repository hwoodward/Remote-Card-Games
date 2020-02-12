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
    # host, port = sys.argv[1].split(":")
    # ruleset = sys.argv[2]
    host, port = "localhost", "12345"
    ruleset = "HandAndFoot"
    print(host)
    print(port)
    print(ruleset)
    connection.DoConnect((host, int(port)))
    clientState = ClientState(ruleset)
    gameControl = Controller(clientState)
    playername = gameControl.getName()
    print("DEBUG: reached point A in RunClient")
    createDisplay = CreateDisplay(playername)
    print("DEBUG: reached point B in RunClient")
    handView = HandView(gameControl, createDisplay.display)
    print("DEBUG: reached point C in RunClient")
    tableView = TableView(createDisplay.display)
    print("DEBUG: reached point D in RunClient")
    while True:
        createDisplay.refresh()
        print("DEBUG: reached point E in RunClient")
        handView.nextEvent()
        print("DEBUG: reached point F in RunClient")
        connection.Pump()
        print("DEBUG: reached point G in RunClient")
        gameControl.Pump()
        print("DEBUG: reached point H in RunClient")
        tableView.Pump()
        print("DEBUG: reached point I in RunClient")
        handView.update()
        print("DEBUG: reached point J in RunClient")
        tableView.playerByPlayer()
        print("DEBUG: reached point K in RunClient")
        note = gameControl.note
        print("DEBUG: reached point L in RunClient")
        createDisplay.render(note)
        print("DEBUG: reached point M in RunClient")
        sleep(0.001)

if __name__ == "__main__":
    '''
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "host:port ruleset")
        print("e.g.", sys.argv[0], "localhost:31425 HandAndFoot")
    else:
        RunClient()
    '''
    RunClient()
else:
    print("RunServer should not be imported anywhere")
