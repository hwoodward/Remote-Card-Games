import pygame

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
                    self.controller.Discard(self.controller.Get_Hand())

    def Print_Text(self, textString, boxCenter):
        """pring the textString in a text box centered at boxCenter in the display"""
        textSurface = UIC.bigText.render(textString, True, UIC.Black)
        textSurface.get_rect().center = boxCenter
        self.display.blit(textSurface, textSurface.get_rect())
