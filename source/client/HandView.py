import pygame
import textwrap
import client.UIConstants as UIC
from client.UICardWrapper import UICardWrapper
from client.ClickableImage import ClickableImage as ClickImg
import client.Button as Btn
import operator

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
        self.display = pygame.display.set_mode((UIC.Disp_Width, UIC.Disp_Height))
        pygame.display.set_caption(self.controller.getName() + " View")
        self.display.fill(UIC.White)
        self.draw_pile = ClickImg(UIC.Back_Img, 10, 25, UIC.Back_Img.get_width(), UIC.Back_Img.get_height(), 0)
        # Buttons to cause cards to be realigned, or realigned and sorted (by rank).
        # will move hard coded numbers to UIC constants once I've worked them out a bit more.
        self.realign_btn = Btn.Button(UIC.White, 900, 25, 50, 50, text='Align hand')
        self.realign_btn.outline_color = UIC.Gray
        self.sort_btn = Btn.Button(UIC.Bright_Blue, 1000, 25, 50, 50, text='sort')
        # render starting window
        self.render()

    def render(self):
        """This should render the entire UI, for now it just
        prints the hand and a few action buttons"""

        self.display.fill(UIC.White)
        self.last_hand = self.current_hand
        self.current_hand = self.controller.getHand()
        if not self.last_hand == self.current_hand:
            self.hand_info = self.wrapHand(self.current_hand, self.hand_info)
        self.showHolding(self.hand_info)  # displays hand
        # display draw pile and various action buttons
        self.draw_pile.draw(self.display, self.draw_pile.outline_color)
        self.realign_btn.draw(self.display, self.realign_btn.outline_color)
        self.sort_btn.draw(self.display, self.sort_btn.outline_color)
        # printText below is for debugging purposes.
        # Will eventually replace hand display with info on game progress.
        self.printText("{0}".format(self.current_hand), (5,UIC.Table_Hand_Border))
        pygame.display.update()

    def nextEvent(self):
        """This submits the next user input to the controller"""

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                # The window crashed, we should handle this
                print("pygame crash, AAAHHH")
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_9:
                    self.controller.draw()
                    UIC.debugflag = 0
                    
                if event.key == pygame.K_8:
                    print("Ending turn")
                    # while creating UI we want to simplify discards
                    # but discarding entire list of cards too simple.
                    if len(self.hand_info) > 0:
                        discard_wrapped = self.hand_info[0]
                        bogus_discards = [discard_wrapped.card]
                    else:
                        bogus_discards = []                    
                    self.controller.discard(bogus_discards)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.sort_btn.isOver(pos):
                    # sort cards - for now draw, because that action works.
                    self.controller.draw()
                if self.realign_btn.isOver(pos):
                    # sort cards - for now draw, because that action works.
                    self.controller.draw()
                if self.draw_pile.isOver(pos):
                    self.controller.draw()
                else:
                    for element in self.hand_info:
                        if element.img_clickable.isOver(pos):
                            element.selected = not element.selected
                            if element.selected:
                                element.img_clickable.changeOutline(2)
                            else:
                                element.img_clickable.changeOutline(0)

            if event.type == pygame.MOUSEMOTION:
                if self.realign_btn.isOver(pos):
                    self.realign_btn.outline_color = UIC.Black  # set outline color
                else:
                    self.realign_btn.outline_color = UIC.Gray  # remove outline
                if self.sort_btn.isOver(pos):
                    self.sort_btn.outline_color = UIC.Blue  # set outline color
                else:
                    self.sort_btn.outline_color = UIC.Bright_Blue  # remove highlighted outline
                if self.draw_pile.isOver(pos):   #later will need to require that it be the beginning of the turn, too.
                    self.draw_pile.changeOutline(1)
                else:
                    self.draw_pile.changeOutline(0)
                    for element in self.hand_info:
                        color_index = element.img_clickable.outline_index
                        if element.img_clickable.isOver(pos):
                            # Brighten colors that mouse is over.
                            # Odd colors are bright, even show selected status.
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
        card_xy = (10, UIC.Table_Hand_Border + 40)
        old_wrapped_hand = wrapped_hand
        updated_wrapped_hand = []
        if not updated_hand == []:
            for card in updated_hand:
                newcard = True
                for already_wrapped in old_wrapped_hand :
                    if newcard and card == already_wrapped.card :
                        element_wrapped = already_wrapped
                        card_xy = (max(card_xy[0],element_wrapped.xy[0]), card_xy[1])
                        old_wrapped_hand.remove(already_wrapped)
                        newcard = False
                if newcard:
                    #TODO -- remove "50" [below] -- use fraction of disp size or card size or something.
                    card_xy = (card_xy[0] + 50, card_xy[1])
                    element_wrapped = UICardWrapper(card, card_xy)
                updated_wrapped_hand.append(element_wrapped)
        return updated_wrapped_hand

    def showHolding(self, wrapped_cards):
        for wrapped_element in wrapped_cards:
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
