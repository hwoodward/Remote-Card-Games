import pygame
import textwrap
from common.Card import Card
import client.UIConstants as UIC
import client.TableView as TV

from PodSixNet.Connection import connection, ConnectionListener

class HandView():
    """This class handles letting players actualy input information

    It handles the entire turn cycle
    """

    def __init__(self, controller):
        self.controller = controller
        # initialize pygame modules
        pygame.init()
        # create window for game - left side is table=PUBLIC, right side is users
        handDisplayWidth = UIC.displayWidth * UIC.handColumnFraction
        gameDisplay=pygame.display.set_mode((UIC.displayWidth,UIC.displayHeight))
        self.display = pygame.display.set_mode((UIC.displayWidth, UIC.displayHeight))
        pygame.display.set_caption(self.controller.Get_Name() + " View")
        self.display.fill(UIC.White)
        # render starting window
        self.Render()

    def Render(self):
        """This should render the actual UI, for now it just prints the hand"""
        #TODO render the table view showing the visible cards
        # 
        currentHand = self.controller.Get_Hand()
        self.Print_Text("{0}".format(currentHand), (UIC.publicPrivateBoundary,0))

        pygame.display.update()

    def Next_Event(self):
        """This submits the next user input to the controller"""
        #TODO find out what user event was
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #The window crashed, we should handle this
                print("pygame crash, AAAHHH")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_9:
                    print("Drawing card")
                    self.controller.Draw()
                if event.key == pygame.K_8:
                    print("Ending turn")
                    # self.controller.Discard(self.controller.Get_Hand())
                    bogusDiscards = self.controller.Get_Hand()
                    # while creating UI we want to simplify discards
                    # but discarding entire list of cards too simple.
                    if(len(bogusDiscards)>0):
                        bogusDiscards = [bogusDiscards[0]]
                    else:
                        bogusDiscards = []
                    self.controller.Discard(bogusDiscards)

    def Print_Text(self, textString, textStartXY):
        """print the textString in a text box starting on the top left."""
        self.display.fill(UIC.White)
        # Wrap the textString
        word_list = textwrap.wrap(text=textString,width=UIC.Wrap_Width)
        textStartXY_wfeed = textStartXY
        for element in word_list:
            text = UIC.bigText.render(element, True, UIC.Blue, UIC.White)
            textRect = text.get_rect()
            textRect.topleft = textStartXY_wfeed
            self.display.blit(text, textRect)
            textStartXY_wfeed = (textStartXY_wfeed[0],textStartXY_wfeed[1]+UIC.text_feed)

        
