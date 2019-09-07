import pygame
import textwrap
from common.Card import Card
import client.UIConstants as UIC
from client.TableView import TableView
from client.UICardWrapper import UICardWrapper
# from time import sleep 
# from PodSixNet.Connection import connection, ConnectionListener

class HandView():
    """This class handles letting players actualy input information

    It handles the entire turn cycle
    """
    def __init__(self, controller):
        self.controller = controller
        # initialize pygame modules
        pygame.init()
        # initialize hand_info
        # (hand_info =UICardWrapped elements of current_hand).
        self.hand_info = []                  
        # create window for game - left side is table=PUBLIC, right side is users
        # TO DO - change this so bottom is current hand and top is table.
        hand_disp_width = UIC.Disp_Width * UIC.Hand_Col_Fraction
        self.display = pygame.display.set_mode((UIC.Disp_Width, UIC.Disp_Height))
        pygame.display.set_caption(self.controller.getName() + " View")
        self.display.fill(UIC.White)
        # render starting window 
        self.render()

    def render(self):
        """This should render the actual UI, for now it just prints the hand"""
        #TODO render the table view showing the visible cards
        # TO DO
        # change screen split so top=table & bottom=hand(instead of side-by-side)
        self.display.fill(UIC.White)
        current_hand = self.controller.getHand()       
        self.hand_info = self.wrapHand(current_hand) 
        self.showHolding(self.hand_info)
        self.display.blit(UIC.Back_Img,(UIC.Disp_Width/2,UIC.Disp_Height/2))
        self.printText("{0}".format(current_hand), (UIC.Table_Hand_Border,0))
        pygame.display.update()

    def nextEvent(self):
        """This submits the next user input to the controller"""
        #TODO find out what user event was
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #The window crashed, we should handle this
                print("pygame crash, AAAHHH")
                              
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_9:
                    self.controller.draw()
                    
                if event.key == pygame.K_8:
                    print("Ending turn")
                    bogus_discards = []
                    # while creating UI we want to simplify discards
                    # but discarding entire list of cards too simple.
                    if(len(self.hand_info)>0):
                        discard_wrapped = self.hand_info[0]
                        bogus_discards = [discard_wrapped._card]
                    else:
                        bogus_discards = []                    
                    self.controller.discard(bogus_discards)

    def wrapHand(self,updated_hand):
        """Associate each card in updated_hand with a UICardWrapper

        Only update new cards so that location and image not lost
        """
        # right now it updates all cards -- need to modify so that only
        # updates cards that aren't already wrapped.
        card_XY = (10,10)
        img = UIC.Back_Img
        self.wrapped_hand = []
        for element in updated_hand:
            # print(updated_hand)
            card_XY = (card_XY[0]+50,card_XY[1]+50)
            element_wrapped = UICardWrapper(element,card_XY,img)
            self.wrapped_hand.append(element_wrapped)
        return(self.wrapped_hand)

        
    def showHolding(self,wrapped_cards):
        for wrapped_element in wrapped_cards:
            self.display.blit(wrapped_element._img,wrapped_element._xy)

    def printText(self, text_string, start_xy):
        """print the text_string in a text box starting on the top left."""
        # self.display.fill(UIC.White)
        # Wrap the text_string, beginning at start_xy
        word_list = textwrap.wrap(text=text_string,width=UIC.Wrap_Width)
        start_xy_wfeed = start_xy  # 'wfeed' -> "with line feed"
        for element in word_list:
            text = UIC.Big_Text.render(element, True, UIC.Blue, UIC.White)
            textRect = text.get_rect()
            textRect.topleft = start_xy_wfeed
            self.display.blit(text, textRect)
            start_xy_wfeed = (start_xy_wfeed[0],start_xy_wfeed[1]+UIC.Text_Feed)
