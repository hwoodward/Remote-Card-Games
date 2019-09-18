import pygame
import textwrap
import client.UIConstants as UIC
from client.UICardWrapper import UICardWrapper
import client.ClickableImage as Cli
import operator

# need "operator" for this command:  sorted_x = sorted(x, key=operator.attrgetter('score'))
# or this one: x.sort(key=operator.attrgetter('score'))
# Use key to trigger sorting or automatically sort cards when draw cards?
# Need to think about when to update xy locations of cards and how I want to do it...
# Want to see what you draw...
# Two parts to sorting -- one is putting list in order, 2nd part is making xy location recognize list order...

#  Next few imports flagged by pyCharm because not used. Keep for now in case needed later.
#  from common.Card import Card
#  from client.TableView import TableView
#  from time import sleep
#  from PodSixNet.Connection import connection, ConnectionListener


class HandView:
    """This class handles letting players actually input information

    It handles the entire turn cycle
    """
    def __init__(self, controller):
        self.controller = controller
        # initialize pygame modules
        pygame.init()
        # initialize hand_info
        # (hand_info =UICardWrapped elements of current_hand).
        self.current_hand = []
        self.hand_info = []
        # create window for game - left side is table=PUBLIC, right side is users
        # TO DO - change this so bottom is current hand and top is table.
        hand_disp_width = UIC.Disp_Width * UIC.Hand_Col_Fraction
        self.display = pygame.display.set_mode((UIC.Disp_Width, UIC.Disp_Height))
        pygame.display.set_caption(self.controller.getName() + " View")
        self.display.fill(UIC.White)
        # self.outline_color = UIC.outline_colors[0]
        self.draw_pile = Cli.ClickableImage\
                (UIC.Back_Img, 10, 255, UIC.Back_Img.get_width(), UIC.Back_Img.get_height(), 0)
        # render starting window
        self.render()

    def render(self):
        """This should render the actual UI, for now it just prints the hand"""

        # TODO
        # change screen split so top=table & bottom=hand(instead of side-by-side)
        # render the table view showing the visible cards
        self.display.fill(UIC.White)
        self.last_hand = self.current_hand
        self.current_hand = self.controller.getHand()
        if not self.last_hand == self.current_hand:
            self.hand_info = self.wrapHand(self.current_hand, self.hand_info)
            # to debug selecting cards have to make it so that wrapHand does NOT re-wrap cards!!
        self.showHolding(self.hand_info)
        # display draw pile
        self.draw_pile.draw(self.display, self.draw_pile.outline_color)
        # self.display.blit(UIC.Back_Img, (UIC.Disp_Width/2, UIC.Disp_Height/2))
        self.printText("{0}".format(self.current_hand), (UIC.Table_Hand_Border, 0))
        pygame.display.update()

    def nextEvent(self):
        """This submits the next user input to the controller"""

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                # The window crashed, we should handle this
                print("pygame crash, AAAHHH")
                # run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_9:
                    self.controller.draw()
                    UIC.debugflag = 0
                    
                if event.key == pygame.K_8:
                    print("Ending turn")
                    # bogus_discards = []
                    # while creating UI we want to simplify discards
                    # but discarding entire list of cards too simple.
                    if len(self.hand_info) > 0:
                        discard_wrapped = self.hand_info[0]
                        bogus_discards = [discard_wrapped.card]
                        # TODO - REMOVE DISCARD FROM WRAPPED CARDS ARRAY.
                    else:
                        bogus_discards = []                    
                    self.controller.discard(bogus_discards)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.draw_pile.isOver(pos):
                    self.controller.draw()
                else:
                    for element in self.hand_info:
                        if element.img_clickable.isOver(pos):
                            element.selected = not element.selected
                            if element.selected:
                                element.img_clickable.changeOutline(2)
                                # element.xy[1] = element.xy[1] + UIC.vertical_offset
                            else:
                                element.img_clickable.changeOutline(0)
                                # element.xy[1] = element.xy[1] - UIC.vertical_offset

            if event.type == pygame.MOUSEMOTION:
                if self.draw_pile.isOver(pos):   #later will need to require that it be the beginning of the turn, too.
                    self.draw_pile.changeOutline(1)
                else:
                    self.draw_pile.changeOutline(0)
                    for element in self.hand_info:
                        color_index = element.img_clickable.outline_index
                        if element.img_clickable.isOver(pos):
                            # Brighten colors that mouse is over.
                            # Odd colors are bright, even show selected status.
                            #
                            # discuss with others...
                            # Need to decide what card status we need to track...
                            # Might want options 'selected' and 'selected for discard'
                            # Note that color_index and 'selected' carry same info.
                            if (color_index % 2) == 0:
                                color_index = element.img_clickable.outline_index + 1
                                element.img_clickable.changeOutline(color_index)
                        else:
                            color_index = element.img_clickable.outline_index
                            if (color_index % 2) == 1:
                                color_index = color_index - 1
                                element.img_clickable.changeOutline(color_index)


    def wrapHand(self, updated_hand, wrapped_hand):
        """Associate each card in updated_hand with a UICardWrapper

        Only update new cards so that location and image not lost
        """
        # right now it updates all cards -- need to modify so that only
        # updates cards that aren't already wrapped.
        card_xy = (10, 10)
        # TO DO modify code so that only append new cards to wrapped_hand (preserve XY, img, selected)
        old_wrapped_hand = wrapped_hand
        updated_wrapped_hand = []
        if not updated_hand == []:
            for card in updated_hand:
                newcard = True
                for already_wrapped in old_wrapped_hand :
                    if newcard and card == already_wrapped.card :
                        element_wrapped = already_wrapped
                        # card_xy is where we start printing new cards. Should end up being beyond last card.
                        # this should work so long have routine to straighten cards somewhere else...
                        # else will march off of display.
                        card_xy = (element_wrapped.xy[0] + 50, element_wrapped.xy[1] + 50)
                        old_wrapped_hand.remove(already_wrapped)
                        newcard = False
                if newcard:
                    #TODO -- remove "50" [below] -- use fraction of disp size or card size or something.
                    card_xy = (card_xy[0] + 50, card_xy[1] + 50)
                    element_wrapped = UICardWrapper(card, card_xy)
                updated_wrapped_hand.append(element_wrapped)
        return updated_wrapped_hand

    def showHolding(self, wrapped_cards):
        for wrapped_element in wrapped_cards:
            # self.display.blit(wrapped_element.img, wrapped_element.xy)
            color = UIC.outline_colors[wrapped_element.img_clickable.outline_index]
            wrapped_element.img_clickable.draw(self.display, color)

    def printText(self, text_string, start_xy):
        """print the text_string in a text box starting on the top left."""

        # Wrap the text_string, beginning at start_xy
        word_list = textwrap.wrap(text=text_string, width=UIC.Wrap_Width)
        start_xy_wfeed = start_xy  # 'wfeed' -> "with line feed"
        for element in word_list:
            text = UIC.Big_Text.render(element, True, UIC.Blue, UIC.White)
            text_rect = text.get_rect()
            text_rect.topleft = start_xy_wfeed
            self.display.blit(text, text_rect)
            start_xy_wfeed = (start_xy_wfeed[0], start_xy_wfeed[1] + UIC.Text_Feed)
