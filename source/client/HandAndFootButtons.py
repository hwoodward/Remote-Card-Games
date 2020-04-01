import pygame
import client.Button as Btn
import client.HandManagement as HandManagement
import client.UIConstants as UIC
from client.UICardWrapper import UICardWrapper

"""This file contains methods used in displaying the buttons that enable the user to take actions

If a button is clicked then generally two actions take place -- one action initiates communication with the server 
and the second updates the display to reflect the action taken.  
Discards are confirmed within the GUI, and that code is currently split between this file and HandView.

It is Hand and Foot specific because different games may need additional buttons, and may need them arranged
 differently, but most of this code should be useful for other games.
"""
# todo: decide where discard code should go, and how much of the action code following a button click should go in this file.
# Might want to make this file focus on button creation and drawing and actions be in a separate file.


def CreateButtons(self):
    """This creates the buttons used for HandAndFoot. """
    self.ready_yes_btn = Btn.Button(UIC.White, (UIC.Disp_Width-150), (UIC.Disp_Height-70), 125, 25, text='Ready:YES')
    self.ready_color_idx = 2 # color of outline will be: UIC.outline_colors(ready_color_idx)
    self.ready_no_btn = Btn.Button(UIC.White, (UIC.Disp_Width-150), (UIC.Disp_Height-30), 125, 25, text='Ready:NO')
    self.not_ready_color_idx = 6 # color of outline will be: UIC.outline_colors(ready_color_idx)
    self.sort_status_btn = Btn.Button(UIC.White, 900, 25, 225, 25, text='sort by status')
    self.sort_btn = Btn.Button(UIC.White, 900, 75, 225, 25, text='sort by number')
    self.prepare_card_btn = Btn.Button(UIC.White, 400, 25, 345, 25, text='Selected cards -> prepared cards')
    self.clear_prepared_cards_btn = Btn.Button(UIC.White, 320, 75, 225, 25, text='Clear prepared cards')
    self.play_prepared_cards_btn = Btn.Button(UIC.White, 600, 75, 225, 25, text='Play prepared cards')
    self.discard_action_btn = Btn.Button(UIC.Bright_Red, 190, 25, 100, 25, text='discard')
    return

def ButtonDisplay(self):
    # display draw pile and various action buttons
    loc_xy = (self.draw_pile.x, self.draw_pile.y)
    self.draw_pile.draw(self.display, loc_xy, self.draw_pile.outline_color)
    # update discard info and redraw
    discard_info = self.controller.getDiscardInfo()
    self.top_discard = discard_info[0]
    self.pickup_pile_sz = discard_info[1]
    if self.pickup_pile_sz > 0:
        self.top_discard_wrapped = UICardWrapper(self.top_discard, (100, 25), UIC.scale)
        self.pickup_pile = self.top_discard_wrapped.img_clickable
        loc_xy = (self.pickup_pile.x, self.pickup_pile.y)
        self.pickup_pile.draw(self.display, loc_xy, self.pickup_pile.outline_color)
        self.labelMedium(str(self.pickup_pile_sz), 150, 35)
    if self.controller._state.round == -1:
        self.ready_yes_btn.draw(self.display, self.ready_yes_btn.outline_color)
        self.ready_no_btn.draw(self.display, self.ready_no_btn.outline_color)
    self.sort_status_btn.draw(self.display, self.sort_status_btn.outline_color)
    self.sort_btn.draw(self.display, self.sort_btn.outline_color)
    self.prepare_card_btn.draw(self.display, self.prepare_card_btn.outline_color)
    self.clear_prepared_cards_btn.draw(self.display, self.clear_prepared_cards_btn.outline_color)
    self.play_prepared_cards_btn.draw(self.display, self.play_prepared_cards_btn.outline_color)
    self.discard_action_btn.draw(self.display, self.discard_action_btn.outline_color)
    return

def ClickedButton(self,pos):
    # carry out action after mouse clicked on button.
    if self.pickup_pile_sz > 0:
        if self.pickup_pile.isOver(pos):
            self.controller.pickUpPile()
            if len(self.controller.prepared_cards) == 0:
                # manually remove cards played, else an ambiguity in wrapped cards causes
                # picked up cards to sometimes get coordinates of cards just played.
                # If statement insures that you don't remove cards if pick-up failed.
                for wrappedcard in self.hand_info:
                    if wrappedcard.status == 2:
                        self.hand_info.remove(wrappedcard)
                        self.last_hand.remove(wrappedcard.card)
    if self.draw_pile.isOver(pos):
        self.controller.draw()
    elif self.sort_btn.isOver(pos):
        self.hand_info.sort(key=lambda wc: wc.key)
        self.hand_info = HandManagement.refreshXY(self, self.hand_info)
        if self.refresh_flag:  # if needed to rescale card size, then refreshXY again.
            self.hand_info = HandManagement.refreshXY(self, self.hand_info)
    elif self.controller._state.round == -1 and self.ready_yes_btn.isOver(pos):
        self.controller.setReady(True)
        self.ready_color_idx = 6  # color of outline will be: UIC.outline_colors(ready_color_idx)
        self.not_ready_color_idx = 8  # color of outline will be: UIC.outline_colors(not_ready_color_idx)
    elif self.controller._state.round == -1 and self.ready_no_btn.isOver(pos):
        self.controller.setReady(False)
        self.ready_color_idx = 2  # color of outline will be: UIC.outline_colors(ready_color_idx)
        self.not_ready_color_idx = 6  # color of outline will be: UIC.outline_colors(not_ready_color_idx)
    elif self.sort_status_btn.isOver(pos):
        self.hand_info.sort(
            key=lambda wc: (wc.img_clickable.x + (wc.status * UIC.Disp_Width))
        )
        self.hand_info = HandManagement.refreshXY(self, self.hand_info)
        if self.refresh_flag:  # if needed to rescale card size, then refreshXY again.
            self.hand_info = HandManagement.refreshXY(self, self.hand_info)
    elif self.prepare_card_btn.isOver(pos):
        self.already_prepared_cards = self.controller.getPreparedCards()
        self.wrapped_cards_to_prep = gatherSelected(self)
        self.wild_cards = self.controller.automaticallyPrepareCards(self.wrapped_cards_to_prep)
        # wild_cards[0] contains prepared cards minus automatically prepared cards wild card
        # that have not yet been designated, and wild_cards[1] is the
        # list of possible cards each could be assigned to.  Currently list of possibilities is
        # full list of playable cards [1,4,5....13] rather than something more sophisticated.
        self.num_wilds = len(self.wild_cards)
        # newly_prepped_cards = all prepared cards minus already_prepared_cards
        self.newly_prepped_cards = self.controller.getPreparedCards()
        for element in self.already_prepared_cards:
            self.newly_prepped_cards.remove(element)
        for wrappedcard in self.wrapped_cards_to_prep:
            if wrappedcard.card in self.newly_prepped_cards:
                self.newly_prepped_cards.remove(wrappedcard.card)
                wrappedcard.status = 2
                wrappedcard.img_clickable.changeOutline(4)
    elif self.play_prepared_cards_btn.isOver(pos):
        self.controller.play()
        if len(self.controller.prepared_cards) == 0:
            # manually remove cards played, else an ambiguity in wrapped cards can cause
            # different wrapped cards with identical card values to be used.
            for wrappedcard in self.hand_info:
                if wrappedcard.status == 2:
                    self.hand_info.remove(wrappedcard)
                    self.last_hand.remove(wrappedcard.card)
    elif self.clear_prepared_cards_btn.isOver(pos):
        self.controller.clearPreparedCards()
        HM.clearPreparedCardsGui(self)
    elif self.discard_action_btn.isOver(pos):
        wc_list = []
        for element in gatherSelected(self):
            wc_list.append(element)
        self.discard_confirm = self.discardConfirmation(self.discard_confirm, wc_list)
    return

def MouseHiLight(self,pos):
    if self.draw_pile.isOver(pos):
        self.draw_pile.changeOutline(1)
    else:
        self.draw_pile.changeOutline(0)
    if self.pickup_pile_sz > 0:
        if self.pickup_pile.isOver(pos):
            self.pickup_pile.changeOutline(1)
        else:
            self.pickup_pile.changeOutline(0)
    if self.ready_yes_btn.isOver(pos):
        self.ready_yes_btn.outline_color = UIC.outline_colors[self.ready_color_idx + 1]
    else:
        self.ready_yes_btn.outline_color = UIC.outline_colors[self.ready_color_idx]
    if self.ready_no_btn.isOver(pos):
        self.ready_no_btn.outline_color = UIC.outline_colors[self.not_ready_color_idx + 1]
    else:
        self.ready_no_btn.outline_color = UIC.outline_colors[self.not_ready_color_idx]
    if self.sort_status_btn.isOver(pos):
        self.sort_status_btn.outline_color = UIC.Black  # set outline color
    else:
        self.sort_status_btn.outline_color = UIC.Gray  # change outline
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

def gatherSelected(self):
    self.selected_list = []
    for element in self.hand_info:
        if element.status == 1:
            self.selected_list.append(element)
    return self.selected_list