import sys
from time import sleep
from PodSixNet.Connection import connection, ConnectionListener
from client.ClientState import ClientState
from client.Controller import Controller
from client.CreateDisplay import CreateDisplay
from client.TableView import TableView
from client.HandView import HandView
# imports below added so that can generate executable using pyinstaller.
import common.HandAndFoot
import common.Liverpool
import common.Card
import client.Button
import client.ClickableImage
import client.UICardWrapper
import client.UIConstants


def RunClient():
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)
    """This is the launch point for the client.
    
    It sets up the various classes and starts the game loop.
    Steps -- 
    (i) player provides host:port info, and connection to server established.
    (ii) clientState initialized 
    (iii) controller initialized
    (iv) ruleset imported 
    (v) player provides name
    (vi) game window created
    (vii) tableView and handView initialized
    (viii) playername confirmed with server and player_index found.
    (ix) main game loop
    """
    # (i) Connect to server:
    host = str(input("Enter the host [localhost] ") or "localhost")
    port = str(input("Enter the port[12345] ") or "12345")
    connection.DoConnect((host, int(port)))
    # (ii)-(iv) initialize clientState and gameControl.  Will get name of game from server
    ruleset = "tbd"  # ruleset will be obtained from server. If wish to run in test mode than change "tbd" to "test"
    clientState = ClientState(ruleset)
    gameControl = Controller(clientState)
    gameControl.askForGame()    # Ask server for name of game to be played.
    while clientState.ruleset == "tbd":
        connection.Pump()
        gameControl.Pump()
        sleep(0.001)
    clientState.importRules(clientState.ruleset)   # Have rec'd ruleset name from server, so import the rules.
    #
    gameControl.setName()                        # Ask the player their name, and confirm it is acceptable.
    playername = gameControl.getName()           # Confirm server has player name.
    gameboard = CreateDisplay(playername)
    tableView = TableView(gameboard.display, clientState.ruleset)
    handView = HandView(gameControl, gameboard.display, clientState.ruleset)
    current_round = handView.round_index
    while(len(tableView.player_names) < 1) or (tableView.player_names.count('guest') > 0 ):
        # Note that if two people join with the same name almost simultaneously, then both might be renamed.
        gameboard.refresh()
        connection.Pump()
        gameControl.Pump()
        tableView.Pump()
        tableView.playerByPlayer(current_round)
        note = "Waiting for all current players to pick legit names. If wait seems too long, " \
               "then it is possible game has already begun, or you have the wrong server or port#..."
        gameboard.render(note)
        sleep(0.01)
    playername = gameControl.checkNames(tableView.player_names)
    # games with Shared_Board=True need player_index, hence need unique names.
    # first must insure that server is reporting correct name, this can take a few cycles.
    if clientState.rules.Shared_Board:
        clientState.player_index = -99
        while clientState.player_index == -99:
            try:
                clientState.player_index = tableView.player_names.index(playername)
            except Exception as err:
                note = "{0}   waiting for name in player_names to update...".format(err)
            gameboard.refresh()
            connection.Pump()
            gameControl.Pump()
            tableView.Pump()
            tableView.playerByPlayer(current_round)
            gameboard.render(note)
            sleep(0.001)
    while True:
        # Primary game loop.
        this_round = handView.round_index
        gameboard.refresh()
        handView.nextEvent()
        connection.Pump()
        gameControl.Pump()
        tableView.Pump()
        tableView.playerByPlayer(this_round)
        if  clientState.rules.Shared_Board:
            player_index = tableView.player_names.index(playername)
            visible_scards = tableView.visible_scards
            handView.update(player_index, len(tableView.player_names), visible_scards)
        else:
            handView.update()
        note = gameControl.note
        gameboard.render(note)
        sleep(0.001)

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("This version gets host:port and ruleSet after starting.")
        print("Do not include any arguments on command line")
    else:
        RunClient()
else:
    print("RunServer should not be imported anywhere")
