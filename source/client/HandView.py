import pygame
import textwrap
from common.Card import Card
import client.UIConstants as UIC
from client.TableView import TableView

from PodSixNet.Connection import connection, ConnectionListener

class UICardWrapper():     
        """GUI needs image and position of card"""
        ''' Realized that whether cards are selected or not
        can be an attribute of UICardWrapper, rather than trying 
        to separate hand into two arrays.  However, have not begun
        doing that yet.
        This will enable me to get rid of "selectedCards baggage'''
        def __init__(self, thiscard, loc_xy, img):
                # should we check that card is in deck?
                self._card = thiscard
                self._img = UICardWrapper.get_image(self._card)
                print('do NOT want get_image in render loop.')
                self._xy = loc_xy      
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
        # create window for game - left side is table=PUBLIC, right side is users
        handDisplayWidth = UIC.displayWidth * UIC.handColumnFraction
        gameDisplay=pygame.display.set_mode((UIC.displayWidth,UIC.displayHeight))
        self.display = pygame.display.set_mode((UIC.displayWidth, UIC.displayHeight))
        pygame.display.set_caption(self.controller.Get_Name() + " View")
        self.display.fill(UIC.White)
        selectedCards = []
        heldCards = []
        # render starting window, 
        self.Render()

    def Render(self):
        """This should render the actual UI, for now it just prints the hand"""
        #TODO render the table view showing the visible cards
        # TO DO change screen split so top=table and bottom = hand (instead of side-by-side)
        currentHand = self.controller.Get_Hand()
        ''' maybe put in comparison between length of currentHand and length
        of hand that's been wrapped, and only run for loop when they disagree.
        '''
        '''
card_XY = (10,10)
        icard = 0
        # if (len(currentHand) > 0):
        for element in currentHand:
            # print(currentHand)
            # tmp_indx=len(currentHand)-1
            # newCard = currentHand[tmp_indx]
            print(element._number)
            print(element._suit)
            card_XY = (card_XY[0]+30,card_XY[1]+30)
            img = UIC.backImg
            element_wrapped = UICardWrapper(element,card_XY,img)
            print(element_wrapped._card)
            print(element_wrapped._xy)
            # need to debug next 2 lines. "heldCards is not defined"
            # heldCards[icard]=element_wrapped
            # print(heldCards[icard]._card)
            print(element_wrapped._card)
            icard = icard+1
        # self.Show_Selected(holdingCards)
        # self.Show_Holding(self.heldCards)
        '''
        self.display.blit(UIC.backImg,(UIC.displayWidth/2,UIC.displayHeight/2))
        self.Print_Text("{0}".format(currentHand), (UIC.publicPrivateBoundary,0))
        '''
        if(len(currentHand) > 1):
           self.display.blit(card4gui._img,card4gui._xy)
        '''
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
                    # PROPOSE MAKING UPDATING TABLE VIEW AN EVENT TRIGGERED BY USER.
                    # TableView.Network_visibleCards()             
                if event.key == pygame.K_9:
                    print("Drawing card")
                    self.controller.Draw()
                    # seem to need to pause while waiting for drawn card to be returned?
                    # NEED TO FIGURE THIS OUT.
                    currentHand = self.controller.Get_Hand()
                    card_XY = (10,10)
                    icard=0
                    # if (len(currentHand) > 0):
                    for element in currentHand:
                        # print(currentHand)
                        # tmp_indx=len(currentHand)-1
                        # newCard = currentHand[tmp_indx]
                        print(element._number)
                        print(element._suit)
                        card_XY = (card_XY[0]+30,card_XY[1]+30)
                        img = UIC.backImg
                        element_wrapped = UICardWrapper(element,card_XY,img)
                        print(element_wrapped._card)
                        print(element_wrapped._xy)
                        # self.heldCards.append(element_wrapped)
                        # heldCards[icard]=element_wrapped
                        # print(heldCards[icard]._card)
                        print(element_wrapped._card)
                        icard = icard+1
                        '''
                        card4gui[tmp_indx] = UICardWrapper(newCard,card_XY,img)
                        print(card4gui[tmp_indx]._card)
                        print(card4gui[tmp_indx]._xy)
                        '''
                        # print(card4gui._img)
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
            junk = 'In Show_Holding ' + str(wrappedElement.thiscard)
            print(junk)
            self.display.blit(wrappedElement._img,wrappedElement._xy)

    def Show_Selected(self,card4gui):
        ''' temp values while creating Show_ - will eventually make next 2 variables lists of cardsandimages.....'''
        facedown=Card(3,'Clubs')
        card4guiTests = UICardWrapper(facedown,(10,10),UIC.backImg)
        # card4guiTests._img = backImg
        selectedCards[0] = card4guiTests
        for cardElement in selectedCards:
            junk = 'In Show_Selected' + str(selectedCards[0].thiscard)
            print(junk)
            self.display.blit(cardElement._img,cardElement._xy)        

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
