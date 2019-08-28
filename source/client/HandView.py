import pygame
import textwrap
from common.Card import Card
import client.UIConstants as UIC
from client.TableView import TableView
from time import sleep 
from PodSixNet.Connection import connection, ConnectionListener

class UICardWrapper():     
        """GUI needs image and position of card.  Do this when card is drawn.
        Do NOT re-wrap card in render loop -- that will reset "selected" status
        and reload image file.
        """

        def __init__(self, thiscard, loc_xy, img):
                # should we check that card is in deck?
                self._card = thiscard
                self._img = UICardWrapper.get_image(self._card)
                self._xy = loc_xy
                self._selected = False
        def get_image(onecard):
                temp = onecard._suit
                if(temp is not None):
                        temp = temp[0]
                else:
                        temp = 'N'
                imageFileName='client\card_images\card'+str(onecard._number)+ temp + '.png'
                print(imageFileName)
                img = pygame.image.load(imageFileName)
                return(img)


class HandView():
    """This class handles letting players actualy input information

    It handles the entire turn cycle
    """

    def __init__(self, controller):
        self.controller = controller
        # initialize pygame modules
        pygame.init()
        # initialize handInfo (handInfo =UICardWrapped elements of currentHand).
        self.handInfo = []                  
        # create window for game - left side is table=PUBLIC, right side is users
        # TO DO - change this so bottom is current hand and top is table.
        handDisplayWidth = UIC.displayWidth * UIC.handColumnFraction
        gameDisplay=pygame.display.set_mode((UIC.displayWidth,UIC.displayHeight))
        self.display = pygame.display.set_mode((UIC.displayWidth, UIC.displayHeight))
        pygame.display.set_caption(self.controller.Get_Name() + " View")
        self.display.fill(UIC.White)
        # render starting window, 
        self.Render()

    def Render(self):
        """This should render the actual UI, for now it just prints the hand"""
        #TODO render the table view showing the visible cards
        # TO DO change screen split so top=table and bottom = hand (instead of side-by-side)
        self.display.fill(UIC.White)
        currentHand = self.controller.Get_Hand()
        self.Show_Holding(self.handInfo)
        self.display.blit(UIC.backImg,(UIC.displayWidth/2,UIC.displayHeight/2))
        self.Print_Text("{0}".format(currentHand), (UIC.publicPrivateBoundary,0))
        pygame.display.update()

    def Next_Event(self):
        """This submits the next user input to the controller"""
        #TODO find out what user event was
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #The window crashed, we should handle this
                print("pygame crash, AAAHHH")

            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_9 or event.key == pygame.K_8) :
                    print("Refreshing view of hand -- seem to need to do this after drawing card.")
                    print(" TO DO -- preserve selection status (this currently resets selections)")
                    # TableView.Network_visibleCards()
                    # ?? was Network_visibleCards() renamed ??
                    currentHand = self.controller.Get_Hand()
                    card_XY = (100,100)
                    img = UIC.backImg
                    self.handInfo = []                   
                    for element in currentHand:
                        print(currentHand)
                        card_XY = (card_XY[0]+30,card_XY[1]+30)
                        element_wrapped = UICardWrapper(element,card_XY,img)
                        self.handInfo.append(element_wrapped)                    
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_9:
                    currentHand = self.controller.Get_Hand()
                    len_BeforeDraw = len(currentHand)
                    print(len_BeforeDraw)
                    print("Drawing card")
                    self.controller.Draw()
                    # will need to scale card_XY and img size later.
                    card_XY = (100,100)
                    img = UIC.backImg
                    self.handInfo = []                   
                    for element in currentHand:
                        print(currentHand)
                        card_XY = (card_XY[0]+30,card_XY[1]+30)
                        element_wrapped = UICardWrapper(element,card_XY,img)
                        self.handInfo.append(element_wrapped)
                    
                        
                if event.key == pygame.K_8:
                    print("Ending turn")
                    bogusDiscards = []
                    # while creating UI we want to simplify discards
                    # but discarding entire list of cards too simple.
                    if(len(self.handInfo)>0):
                        WrappedDiscardCard = self.handInfo[0]
                        bogusDiscards = [WrappedDiscardCard._card]
                    else:
                        # bogusDiscards = []
                        bogusDiscards = []                    
                    self.controller.Discard(bogusDiscards)
                    
                    

    def Show_Holding(self,wrappedCards):
        for wrappedElement in wrappedCards:
            self.display.blit(wrappedElement._img,wrappedElement._xy)

    def Print_Text(self, textString, textStartXY):
        """print the textString in a text box starting on the top left."""
        # self.display.fill(UIC.White)
        # Wrap the textString
        word_list = textwrap.wrap(text=textString,width=UIC.Wrap_Width)
        textStartXY_wfeed = textStartXY
        for element in word_list:
            text = UIC.bigText.render(element, True, UIC.Blue, UIC.White)
            textRect = text.get_rect()
            textRect.topleft = textStartXY_wfeed
            self.display.blit(text, textRect)
            textStartXY_wfeed = (textStartXY_wfeed[0],textStartXY_wfeed[1]+UIC.text_feed)
