import sys
from time import sleep
from PodSixNet.Connection import connection, ConnectionListener
from client.ClientState import ClientState
from client.Controller import Controller
from client.CreateDisplay import CreateDisplay
# Currently import TableView methods for both HandAndFoot and Liverpool
# (attempted using importlib, got it working with interpreter,
# but could not create RunClient executable without further debugging).
# # in future may merge TableView files and have dedicated methods within each.
from client.TableView import TableView            # this is for Liverpool
from client.TableView_HF import TableView_HF      # this is for HandAndFoot
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
    
    It sets up the various classes and starts the game loop
    """
    hostinfo = str(input("Enter the host:port[localhost:12345] ") or "localhost:12345")
    host, port = hostinfo.split(":")
    print(host)
    print(port)
    ruleset = str(input("Enter the ruleset[Liverpool] ") or "Liverpool")
    print(ruleset)
    connection.DoConnect((host, int(port)))
    clientState = ClientState(ruleset)
    gameControl = Controller(clientState)
    playername = gameControl.getName()
    gameboard = CreateDisplay(playername)
    if ruleset == 'Liverpool':
        tableView = TableView(gameboard.display)
    elif ruleset == 'HandAndFoot':
        tableView = TableView_HF(gameboard.display)
    else:
        print('that ruleset is not supported')
    handView = HandView(gameControl, gameboard.display, ruleset)
    while(len(tableView.player_names) < 1) or (tableView.player_names.count('guest') > 0 ):
        # Note that if two people join with the same name almost simultaneously, then both might be renamed.
        note = "waiting for updated list of player names"
        gameboard.refresh()
        connection.Pump()
        gameControl.Pump()
        tableView.Pump()
        tableView.playerByPlayer()
        note = "updating list of player names"
        gameboard.render(note)
        sleep(0.001)
    gameControl.checkNames(tableView.player_names)
    if ruleset == 'Liverpool':
        # Thought I would need different primary loops for 2 games, so put in if statement, then
        # realized I didn't need to do that YET.  Kept if statement just in case
        # I do need separate primary loops in the future.
        while True:
            # Primary game loop.
            gameboard.refresh()
            handView.nextEvent()
            connection.Pump()
            gameControl.Pump()
            tableView.Pump()
            tableView.playerByPlayer() # for Liverpool need to put handView.update on TOP of playerByPlayer.
            handView.update(len(tableView.player_names))
            # added tableView.player_names because Liverpool needs # players (HandAndFoot did not).
            # tableView.playerByPlayer()
            note = gameControl.note
            gameboard.render(note)
            sleep(0.001)
    if ruleset =='HandAndFoot':
        # Thought I would need different primary loops for 2 games, so put in if statement, then
        # realized I didn't need to do that YET.  Kept if statement just in case
        # I do need separate primary loops in the future.
        while True:
            # Primary game loop.
            gameboard.refresh()
            handView.nextEvent()
            connection.Pump()
            gameControl.Pump()
            tableView.Pump()
            tableView.playerByPlayer() # for Liverpool need to put handView.update on TOP of playerByPlayer.
            handView.update(len(tableView.player_names))
            # added tableView.player_names because Liverpool needs # players (HandAndFoot did not).
            # tableView.playerByPlayer()
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