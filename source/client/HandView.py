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
        self.prepared_cards = []     # will contain list of prepared cards from controller
        self.discards = []
        self.discard_confirm = False
        self.draw_pile = ClickImg(UIC.Back_Img, 10, 25, UIC.Back_Img.get_width(), UIC.Back_Img.get_height(), 0)
        #discard info
        discard_info = self.controller.getDiscardInfo()
        self.top_discard = discard_info[0]  
        self.pickup_pile_sz = discard_info[1]
        if self.pickup_pile_sz > 0:
            self.top_discard_wrapped = UICardWrapper(self.top_discard, (100, 25))
            self.pickup_pile = self.top_discard_wrapped.img_clickable
        # Buttons to cause actions -- e.g. cards will be sorted by selection status or by number.
        # will move hard coded numbers to UIC constants once I've worked them out a bit more.
        self.mv_selected_btn = Btn.Button(UIC.White, 900, 25, 225, 25, text='move selected cards')
        self.sort_btn = Btn.Button(UIC.White, 900, 75, 225, 25, text='sort all cards')
        self.prepare_card_btn = Btn.Button(UIC.White, 320, 25, 225, 25, text='Prepare selected cards')
        self.clear_prepared_cards_btn = Btn.Button(UIC.White, 320, 75, 225, 25, text='Clear prepared cards')
        self.play_prepared_cards_btn = Btn.Button(UIC.White, 600, 75, 225, 25, text='Play prepared cards')
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
        #update discard info and redraw
        discard_info = self.controller.getDiscardInfo()
        self.top_discard = discard_info[0]
        self.pickup_pile_sz = discard_info[1]
        if self.pickup_pile_sz > 0:
            self.top_discard_wrapped = UICardWrapper(self.top_discard, (100, 25))
            self.pickup_pile = self.top_discard_wrapped.img_clickable
            loc_xy = (self.pickup_pile.x, self.pickup_pile.y)
            self.pickup_pile.draw(self.display, loc_xy, self.pickup_pile.outline_color)
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
                    # this is a leftover appendage from earlier phase.
                    # Keep for now so I have example of keydown.
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.draw_pile.isOver(pos):
                    self.controller.draw()
                if self.pickup_pile_sz > 0:
                    if self.pickup_pile.isOver(pos):
                        self.controller.pickUpPile()
                if self.sort_btn.isOver(pos):
                    self.hand_info.sort(key=lambda wc: wc.key)
                    self.hand_info = self.refreshXY(self.hand_info)
                if self.mv_selected_btn.isOver(pos):
                    self.hand_info.sort(
                        key=lambda wc: (wc.img_clickable.x + UIC.Disp_Width)
                        if wc.status == 1 else wc.img_clickable.x
                        )
                    # TODO: for sheri - move prepared even further to the right.
                    self.hand_info = self.refreshXY(self.hand_info)
                if self.prepare_card_btn.isOver(pos):
                    self.already_prepared_cards = self.controller.getPreparedCards()
                    self.wrapped_cards_to_prep = self.gatherSelected()
                    self.cards_to_prep = []
                    for element in self.wrapped_cards_to_prep:
                        self.cards_to_prep.append(element.card)
                    user_input_cards = self.controller.automaticallyPrepareCards(self.cards_to_prep)
                    if (len(user_input_cards)>0):
                        print("We still need to handle wild cards.")
                    # The user_input_cards are a list of card/key option pairs ex. [[(0, None), [1,4,5,6,7,8,9,10,11,12,13]], [(2, 'Hearts'), [1,4,5,6,7,8,9,10,11,12,13]]]
                    # TODO: for Sheri - need to get user input on what key to prepare user_input_cards (wild cards) in.
                    # To prepare them when ready call self.controller.prepareCard(card, key)
                    #
                    # TODO: for Sheri - need to update display so that prepared cards are obvious...
                    # will probably move them vertically and might change outline color.
                    #
                    # newly_prepped_cards = all prepared cards minus already_prepared_cards
                    self.newly_prepped_cards = self.controller.getPreparedCards()
                    for element in self.already_prepared_cards:
                        self.newly_prepped_cards.remove(element)
                    for wrappedcard in self.wrapped_cards_to_prep:
                        if wrappedcard.card in self.newly_prepped_cards:
                            self.newly_prepped_cards.remove(wrappedcard.card)
                            wrappedcard.status == 2
                            wrappedcard.img_clickable.changeOutline(4)
                if self.clear_prepared_cards_btn.isOver(pos):
                    self.controller.clearPreparedCards()
                    for element in self.hand_info:
                        if element.status > 1:
                            # todo:  Sheri - understand why ==2  didn't work.
                            element.status = 0
                            element.img_clickable.changeOutline(0)
                if self.play_prepared_cards_btn.isOver(pos):
                    self.controller.play()
                if self.discard_action_btn.isOver(pos):
                    card_list = []
                    for element in self.gatherSelected():
                        card_list.append(element.card)
                    self.discard_confirm = self.discardConfirmation(self.discard_confirm, card_list)
                else:
                    for element in self.hand_info:
                        if element.img_clickable.isOver(pos):
                            if element.status == 2:
                                element.img_clickable.changeOutline(4)
                                # prepared cards (status = 2) managed by controller.
                                # to change prepared card's status must clear prepared cards.
                            else:
                                if element.status == 1:
                                    element.status = 0
                                    element.img_clickable.changeOutline(0)
                                else:
                                    element.status = 1
                                    element.img_clickable.changeOutline(2)

            if event.type == pygame.MOUSEMOTION:
                if self.draw_pile.isOver(pos):
                    self.draw_pile.changeOutline(1)
                else:
                    self.draw_pile.changeOutline(0)
                if self.pickup_pile_sz > 0:
                    if self.pickup_pile.isOver(pos):
                       self.pickup_pile.changeOutline(1)
                    else:
                       self.pickup_pile.changeOutline(0)
                if self.mv_selected_btn.isOver(pos):
                    self.mv_selected_btn.outline_color = UIC.Black  # set outline color
                else:
                    self.mv_selected_btn.outline_color = UIC.Gray  # change outline
                if self.sort_btn.isOver(pos):
                    self.sort_btn.outline_color = UIC.Black  # set outline color
                else:
                    self.sort_btn.outline_color = UIC.Gray  # remove highlighted outline
                if self.prepare_card_btn.isOver(pos):
                    self.prepare_card_btn.outline_color = UIC.Bright_Blue  # set outline color
                else:
                    self.prepare_card_btn.outline_color = UIC.Blue  # remove highlighted outline
                if self.clear_prepared_cards_btn.isOver(pos):
                    self.clear_prepared_cards_btn.outline_color = UIC.Bright_Red  # set outline color
                else:
                    self.clear_prepared_cards_btn.outline_color = UIC.Red  # remove highlighted outline
                if self.play_prepared_cards_btn.isOver(pos):
                    self.play_prepared_cards_btn.outline_color = UIC.Bright_Green  # set outline color
                else:
                    self.play_prepared_cards_btn.outline_color = UIC.Green  # remove highlighted outline
                if self.discard_action_btn.isOver(pos):
                    self.discard_action_btn.outline_color = UIC.Black  # set outline color
                else:
                    self.discard_action_btn.outline_color = UIC.Bright_Red  # remove highlighted outline
                    for element in self.hand_info:
                        color_index = element.img_clickable.outline_index
                        if element.img_clickable.isOver(pos):
                            # Brighten colors that mouse is over.
                            # Odd colors are bright, even show status.
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
            if element.status == 1:
                self.selected_list.append(element)
                #todo: from Sheri for Sheri verify that changing this from element.card to element OK
        return self.selected_list

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
