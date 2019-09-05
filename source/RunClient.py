import sys
from time import sleep

from PodSixNet.Connection import connection
from client.Controller import Controller
from client.TableView import TableView
from client.HandView import HandView
from client.ClientState import ClientState
#TODO: consistent import ordering for ease of finding stuff

if len(sys.argv) != 3:
    print("Usage:", sys.argv[0], "host:port ruleset")
    print("e.g.", sys.argv[0], "localhost:31425 HandAndFoot")
else:
    host, port = sys.argv[1].split(":")
    ruleset = sys.argv[2]
    connection.DoConnect((host, int(port)))
    clientState = ClientState(ruleset)
    gameControl = Controller(clientState)
    handView = HandView(gameControl)
    tableView = TableView()
    while 1:
        handView.nextEvent()
        connection.Pump()
        gameControl.Pump()
        tableView.Pump()
        handView.render()
        sleep(0.001)

