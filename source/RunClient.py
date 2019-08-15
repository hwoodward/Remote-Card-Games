import sys
from time import sleep

from PodSixNet.Connection import connection
from client.Controller import Controller
from client.TableView import TableView
from client.HandView import HandView
from client.ClientState import ClientState
#TODO: consistent import ordering for ease of finding stuff

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    connection.DoConnect((host, int(port)))
    clientState = ClientState()
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

