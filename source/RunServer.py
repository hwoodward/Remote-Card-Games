import sys
from time import sleep

from server.GameServer import GameServer

# get command line argument of server, port
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    server = GameServer(localaddr=(host, int(port)))
    while True:
        server.Pump()
        sleep(0.0001)
