import pygame
import textwrap
from common.Card import Card
import client.UIConstants as UIC
from client.TableView import TableView

from PodSixNet.Connection import connection, ConnectionListener

class cardAndImage():     
        """GUI needs image and position of card"""
        def __init__(self, card, xy, img):
                # should we check that card is in deck?
                self._card = card
                self._img = cardAndImage.get_image(self._card)
                print('do NOT want get_image in render loop.')
                self._xy = xy      
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
        # render starting window, 
        self.Render()

    def Render(self):
        """This should render the actual UI, for now it just prints the hand"""
        #TODO render the table view showing the visible cards
        # TO DO change screen split so top=table and bottom = hand (instead of side-by-side)
        currentHand = self.controller.Get_Hand()
        self.Print_Text("{0}".format(currentHand), (UIC.publicPrivateBoundary,0))
        ''' temp values while creating Show_ - will eventually make next 2 variables lists of cardsandimages.....'''
        selectedCards_Images = UIC.card4guiTests
        heldCards_Images = UIC.card4guiTests
        heldCards_Images._xy=(10,UIC.displayHeight*0.9)
        self.Show_Selected(selectedCards_Images)
        self.Show_Holding(heldCards_Images)
        self.display.blit(UIC.backImg,(UIC.displayWidth/2,UIC.displayHeight/2))
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
                    if (len(currentHand) > 0):
                        print(currentHand)
                        tmp_indx=len(currentHand)-1
                        newCard = currentHand[tmp_indx]
                        print(newCard._number)
                        print(newCard._suit)
                        # card_XY = (card_XY[0]+30,card_XY[1]+30)
                        img = UIC.backImg
                        card4gui = cardAndImage(newCard,card_XY,img)
                        print(card4gui._card)
                        print(card4gui._xy)
                        
                        '''
                        card4gui[tmp_indx] = cardAndImage(newCard,card_XY,img)
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

    def Show_Holding(self,card4gui):
        self.display.blit(card4gui._img,card4gui._xy)

    def Show_Selected(self,card4gui):
        self.display.blit(card4gui._img,card4gui._xy)

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
