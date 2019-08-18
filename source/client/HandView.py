import pygame
import textwrap
from common.Card import Card
import client.UIConstants as UIC

from PodSixNet.Connection import connection, ConnectionListener

class HandView():
    """This class handles letting players actualy input information

    It handles the entire turn cycle
    """

    def __init__(self, controller):
        self.controller = controller
        # initialize pygame modules
        pygame.init()
        # create window
        self.display = pygame.display.set_mode((UIC.displayWidth, UIC.displayHeight))
        pygame.display.set_caption(self.controller.Get_Name() + " Hand View")
        self.display.fill(UIC.White)
        # render starting window
        self.Render()

    def Render(self):
        """This should render the actual UI, for now it just prints the hand"""
        #TODO render the table view showing the visible cards
        currentHand = self.controller.Get_Hand()
        self.Print_Text("{0}".format(currentHand), (UIC.displayWidth/2, UIC.displayHeight/3))
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

    def Print_Text(self, textString, boxCenter):
        """pring the textString in a text box centered at boxCenter in the display"""
        self.display.fill(UIC.White)
        # tried this A: bkGrdRect = (0,0,200,50)
        # tried this A: pygame.draw.rect(self.display, UIC.Red, bkGrdRect)
        # Wrap this text.
        wrapper = textwrap.TextWrapper(width=50)
        word_list = textwrap.wrap(text=textString)
        # have hardcoded 50 for this test, will need to scale that later.
        for element in word_list:
            # print(element)
            textSurface = UIC.bigText.render(element, True, UIC.Black)
            # triedd this -- but it didn't work: boxCenter = (boxCenter[0],boxCenter[1]+30)
            textSurface.get_rect().center = boxCenter
            self.display.blit(textSurface, textSurface.get_rect())
        # tried this A: pygame.draw.rect(self.display, UIC.Red, bkGrdRect)
        
