import sys
import threading

from time import sleep
from server.GameServer import GameServer

Waiting_For_Start = True
Waiting_For_End = True

def commandLineTransitions():
    """This waits on input for game start and end"""
    global Waiting_For_Start, Waiting_For_End
    temp = input("Press enter when all players are connected to start the game\n")
    Waiting_For_Start = False
    temp = input("Press enter to end the game when finsihed playing\n")
    Waiting_For_End = False

def runServer():
    """This is the functionality start point for the server."""
    # get command line argument of server, port
    host, port = sys.argv[1].split(":")
    rulesetName = sys.argv[2]
    server = GameServer(localaddr=(host, int(port)), ruleset=rulesetName)
    #set up thread for user input
    global Waiting_For_Start, Waiting_For_End
    inputThread = threading.Thread(target=commandLineTransitions)
    inputThread.start()
    # wait for game to start
    while Waiting_For_Start:
        server.Pump()
        sleep(0.0001)
    #set active_game to true and run loop until game is over
    server.StartGame()
    while Waiting_For_End:
        server.Pump()
        sleep(0.0001)
    print("To play again restart server with same command")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "host:port ruleset")
        print("e.g.", sys.argv[0], "localhost:31425 HandAndFoot")
    else:
        runServer()
else:
    print("RunServer should not be imported anywhere")
