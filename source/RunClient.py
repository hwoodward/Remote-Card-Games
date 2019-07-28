import sys
from time import sleep

from PodSixNet.Connection import connection
from client.Controller import Controller
from client.TableView import TableView
from client.ClientState import ClientState

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    connection.DoConnect((host, int(port)))
    clientState = ClientState()
    gameControl = Controller(clientState)
    #TODO: add playerInterface
    tableView = TableView()
    while 1:
        #TODO: get next player event
        connection.Pump()
        gameControl.Pump()
        tableView.Pump()
        #TODO: reRender the playerInterface with updated information
        sleep(0.001)

