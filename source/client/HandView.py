import pygame
import textwrap
import client.Button as Btn
from client.ClickableImage import ClickableImage as ClickImg
from client.UICardWrapper import UICardWrapper
import client.UIConstants as UIC
from common.Card import Card


class HandView:
    """This class handles letting players actually input information

    Drawing, melding and discards are all done in this class.
    Player can also fidget with hand during other players' turns.
    """
    def __init__(self, controller, display):
        self.controller = controller
        self.display = display
        self.current_hand = []
        self.last_hand = []
        self.hand_info = []          # will contain UICardWrapped elements of current_hand
        self.discards = []
        self.discard_confirm = False
        # TODO: verify that self.discard_confirm is still needed.
        self.draw_pile = ClickImg(UIC.Back_Img, 10, 25, UIC.Back_Img.get_width(), UIC.Back_Img.get_height(), 0)
        self.displayPile(Card(3,'Hearts'))
        # Buttons to cause actions -- e.g. cards will be sorted by selection status or by number.
        # will move hard coded numbers to UIC constants once I've worked them out a bit more.
        self.mv_selected_btn = Btn.Button(UIC.White, 900, 25, 225, 25, text='move selected cards')
        self.mv_selected_btn.outline_color = UIC.Gray
        self.sort_btn = Btn.Button(UIC.White, 900, 75, 225, 25, text='sort')
        self.prepare_card_btn = Btn.Button(UIC.Bright_Blue, 300, 25, 225, 25, text='Prepare selected cards')
        self.clear_prepared_cards_btn = Btn.Button(UIC.Bright_Blue, 300, 75, 225, 25, text='Clear prepared cards')
        self.play_prepared_cards_btn = Btn.Button(UIC.Bright_Blue, 600, 75, 225, 25, text='Play prepared cards')
        self.discard_action_btn = Btn.Button(UIC.Bright_Red, 190, 25, 100, 25, text='discard')

    def update(self):
        """This updates the view of the hand """

        self.last_hand = self.current_hand
        self.current_hand = self.controller.getHand()
        if not self.last_hand == self.current_hand:
            self.hand_info = self.wrapHand(self.current_hand, self.hand_info)
        self.showHolding(self.hand_info)               # displays hand
        # display draw pile and various action buttons
        loc_xy = (self.draw_pile.x, self.draw_pile.y)
        self.draw_pile.draw(self.display, loc_xy, self.draw_pile.outline_color)
        self.displayPile(Card(3,'Hearts'))
        self.mv_selected_btn.draw(self.display, self.mv_selected_btn.outline_color)
        self.sort_btn.draw(self.display, self.sort_btn.outline_color)
        self.prepare_card_btn.draw(self.display, self.prepare_card_btn.outline_color)
        self.clear_prepared_cards_btn.draw(self.display, self.clear_prepared_cards_btn.outline_color)
        self.play_prepared_cards_btn.draw(self.display, self.play_prepared_cards_btn.outline_color)
        self.discard_action_btn.draw(self.display, self.discard_action_btn.outline_color)

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
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.sort_btn.isOver(pos):
                    self.hand_info.sort(key=lambda wc: wc.key)
                    self.hand_info = self.refreshXY(self.hand_info)
                if self.mv_selected_btn.isOver(pos):
                    self.hand_info.sort(
                        key=lambda wc: (wc.img_clickable.x + UIC.Disp_Width)
                        if wc.selected else wc.img_clickable.x
                        )
                    self.hand_info = self.refreshXY(self.hand_info)
                if self.discard_action_btn.isOver(pos):
                    self.discard_confirm = self.discardConfirmation(self.discard_confirm, self.gatherSelected())
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
                if self.mv_selected_btn.isOver(pos):
                    self.mv_selected_btn.outline_color = UIC.Black  # set outline color
                else:
                    self.mv_selected_btn.outline_color = UIC.Gray  # remove outline
                if self.sort_btn.isOver(pos):
                    self.sort_btn.outline_color = UIC.Blue  # set outline color
                else:
                    self.sort_btn.outline_color = UIC.Bright_Blue  # remove highlighted outline
                if self.discard_action_btn.isOver(pos):
                    self.discard_action_btn.outline_color = UIC.Black  # set outline color
                else:
                    self.discard_action_btn.outline_color = UIC.Bright_Red  # remove highlighted outline
                if self.draw_pile.isOver(pos):
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
                for already_wrapped in old_wrapped_hand:
                    if newcard and card == already_wrapped.card:
                        card_wrapped = already_wrapped
                        card_xy = (max(card_xy[0], card_wrapped.img_clickable.x), card_xy[1])
                        old_wrapped_hand.remove(already_wrapped)
                        newcard = False
                if newcard:
                    card_xy = (card_xy[0] + UIC.Card_Spacing, card_xy[1])
                    card_wrapped = UICardWrapper(card, card_xy)
                updated_wrapped_hand.append(card_wrapped)
        return updated_wrapped_hand

    def refreshXY(self, original, layout_option=1):
        """After sorting or melding, may wish to refresh card's xy coordinates """

        if not layout_option == 1:
            print('the only layout supported now is cards in a line, left to right')
        refreshed = []
        card_xy = (10, UIC.Table_Hand_Border + 40)
        for element in original:
            element.img_clickable.x = card_xy[0]
            element.img_clickable.y = card_xy[1]
            card_xy = (card_xy[0] + UIC.Card_Spacing, card_xy[1])
            if card_xy[0] > UIC.Disp_Width:
                print('Need to make loc_xy assignment more sophisticated')
            refreshed.append(element)
        return refreshed

    def showHolding(self, wrapped_cards):
        wrapped_cards.sort(key=lambda wc: wc.img_clickable.x)
        for wrapped_element in wrapped_cards:
            color = UIC.outline_colors[wrapped_element.img_clickable.outline_index]
            loc_xy = (wrapped_element.img_clickable.x, wrapped_element.img_clickable.y)
            wrapped_element.img_clickable.draw(self.display, loc_xy, color)

    def gatherSelected(self):
        self.selected_list = []
        for element in self.hand_info:
            if element.selected:
                self.selected_list.append(element.card)
        return self.selected_list

    # Draw top card of discard pile and make it a clickable image, to trigger picking up the pile.
    def displayPile(self, top_discard):
        # TODO: get top_discard from server, for now use 3 of Hearts.
        # Put in check if size of pile is 0, if so, then don't display the pile.
        #
        top_of_pile = UICardWrapper(top_discard, (100,25))
        loc_xy = (top_of_pile.img_clickable.x, top_of_pile.img_clickable.y)
        top_of_pile.img_clickable.draw(self.display, loc_xy, UIC.White)
        # TODO: Need to stop hard-coding positions (instead of 60,25 should scale with screen and card size)

    # Confirm a user is sure about a discard and then perform it once confirmed
    def discardConfirmation(self, confirmed, discards):
        if self.discards != discards:
            confirmed = False
            self.discards = discards
        if not confirmed:
            self.controller.note = "Please confirm - discard  " + "{0}".format(self.discards)
            self.discards_to_confirm = self.discards
            return True  # ask for confirmation
        else:
            # confirmed is True, performing discard
            self.controller.discard(self.discards)
            return False # now that this is done, we don't have anything waiting on confirmation
