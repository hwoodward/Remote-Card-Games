import sys
import threading
from time import sleep
from server.GameServer import GameServer


def RunServer():
    """This is the functionality start point for the server."""

    # get command line argument of server, port
    host, port = sys.argv[1].split(":")
    ruleset_name = sys.argv[2]
    starting_round = sys.argv[3]
    server = GameServer(localaddr=(host, int(port)), ruleset=ruleset_name, startinground = starting_round )
    while not server.game_over:
        server.Pump()
        sleep(0.0001)
    print("To play again restart server with same command")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:", sys.argv[0], "host:port ruleset  starting_round")
        print("e.g.", sys.argv[0], "localhost:31425 HandAndFoot 0")
    else:
        RunServer()
else:
    print("RunServer should not be imported anywhere")
