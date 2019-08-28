import pygame
import textwrap
from common.Card import Card
import client.UIConstants as UIC
from client.TableView import TableView
from time import sleep 

from PodSixNet.Connection import connection, ConnectionListener

class UICardWrapper():     
        """GUI needs image and position of card"""
        def __init__(self, thiscard, loc_xy, img):
                # should we check that card is in deck?
                self._card = thiscard
                self._img = UICardWrapper.get_image(self._card)
                print('do NOT want get_image in render loop.')
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
        # initialize handInfo (getting error handInfo is not defined)
        self.handInfo = []                  
        # create window for game - left side is table=PUBLIC, right side is users
        handDisplayWidth = UIC.displayWidth * UIC.handColumnFraction
        gameDisplay=pygame.display.set_mode((UIC.displayWidth,UIC.displayHeight))
        self.display = pygame.display.set_mode((UIC.displayWidth, UIC.displayHeight))
        pygame.display.set_caption(self.controller.Get_Name() + " View")
        self.display.fill(UIC.White)
        heldCards = []
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print("Refreshing view of table")
                    # TableView.Network_visibleCards()
                    # ?? was Network_visibleCards() renamed ??            
                if event.key == pygame.K_9:
                    '''
                    seem to need to pause while waiting for drawn card
                    to be returned.  Otherwise when wrap "currentHand"
                    card just drawn is omitted.
                    Handle this by monitoring length of currentHand before
                    and after draw.
                    '''
                    currentHand = self.controller.Get_Hand()
                    len_BeforeDraw = len(currentHand)
                    print(len_BeforeDraw)
                    print("Drawing card")
                    self.controller.Draw()
                    '''
                    sleep(1)
                    currentHand = self.controller.Get_Hand()
                    len_AfterDraw = len(currentHand)
                    print(len_AfterDraw)
                    icard = 0 
                    # NEED TO DEBUG WHY DON'T SEE FINAL CARD IN HAND.
                    # SECTION BELOW WAS AN ATTEMPT, BUT LEFT ME CONFUSED...
                    while(len_AfterDraw <= len_BeforeDraw and icard < 2):
                        currentHand = self.controller.Get_Hand()
                        len_AfterDraw = len(currentHand)
                        print('waiting for server to provide new card')
                        print(icard)
                        print(len_AfterDraw)
                        print(len_BeforeDraw)
                        print(currentHand)
                        sleep(1)
                        icard = icard + 1
                    '''
                    # will need to scale card_XY later.
                    card_XY = (100,100)
                    img = UIC.backImg
                    self.handInfo = []                   
                    for element in currentHand:
                        print(currentHand)
                        card_XY = (card_XY[0]+30,card_XY[1]+30)
                        element_wrapped = UICardWrapper(element,card_XY,img)
                        self.handInfo.append(element_wrapped)
                    print('Next loop for debugging')
                    for element in self.handInfo:
                        print(element._card)
                        print(element_wrapped._xy)
                        print(element_wrapped._selected)

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
