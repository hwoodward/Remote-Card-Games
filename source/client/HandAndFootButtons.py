import pygame
import client.Button as Btn
from client.ClickableImage import ClickableImage as ClickImg
import client.HandManagement as HandManagement
import client.UIConstants as UIC
from client.UICardWrapper import UICardWrapper

"""This file contains methods used in displaying the buttons that enable the user to take actions

If a button is clicked then generally two actions take place -- one action initiates communication with the server 
and the second updates the display to reflect the action taken.  
Discards are confirmed within the GUI, and that code is currently split between this file and HandView.

This file is Hand and Foot specific because different games may need additional buttons, and may need them arranged
 differently, but most of this code should be useful for other games.
"""


def CreateButtons(Hand_View):
    """This creates the buttons used for HandAndFoot. """
    Hand_View.draw_pile = ClickImg(UIC.Back_Img, 10, 25, UIC.Back_Img.get_width(), UIC.Back_Img.get_height(), 0)
    Hand_View.ready_yes_btn = Btn.Button(UIC.White, (UIC.Disp_Width - 150), (UIC.Disp_Height - 70), 125, 25, text='Ready:YES')
    Hand_View.ready_color_idx = 2  # color of outline will be: UIC.outline_colors(ready_color_idx)
    Hand_View.ready_no_btn = Btn.Button(UIC.White, (UIC.Disp_Width - 150), (UIC.Disp_Height - 30), 125, 25, text='Ready:NO')
    Hand_View.not_ready_color_idx = 6  # color of outline will be: UIC.outline_colors(ready_color_idx)
    Hand_View.sort_status_btn = Btn.Button(UIC.White, 900, 25, 225, 25, text='sort by status')
    Hand_View.sort_btn = Btn.Button(UIC.White, 900, 75, 225, 25, text='sort by number')
    Hand_View.prepare_card_btn = Btn.Button(UIC.White, 400, 25, 345, 25, text='Selected cards -> prepared cards')
    Hand_View.clear_prepared_cards_btn = Btn.Button(UIC.White, 320, 75, 225, 25, text='Clear prepared cards')
    Hand_View.play_prepared_cards_btn = Btn.Button(UIC.White, 600, 75, 225, 25, text='Play prepared cards')
    Hand_View.discard_action_btn = Btn.Button(UIC.Bright_Red, 190, 25, 100, 25, text='discard')
    return

def ButtonDisplay(Hand_View):
    """ This updates draw pile and action buttons. It is called in HandView.update each render cycle. """
    loc_xy = (Hand_View.draw_pile.x, Hand_View.draw_pile.y)
    Hand_View.draw_pile.draw(Hand_View.display, loc_xy, Hand_View.draw_pile.outline_color)
    # update discard info and redraw
    discard_info = Hand_View.controller.getDiscardInfo()
    Hand_View.top_discard = discard_info[0]
    Hand_View.pickup_pile_sz = discard_info[1]
    if Hand_View.pickup_pile_sz > 0:
        Hand_View.top_discard_wrapped = UICardWrapper(Hand_View.top_discard, (100, 25), UIC.scale)
        Hand_View.pickup_pile = Hand_View.top_discard_wrapped.img_clickable
        loc_xy = (Hand_View.pickup_pile.x, Hand_View.pickup_pile.y)
        Hand_View.pickup_pile.draw(Hand_View.display, loc_xy, Hand_View.pickup_pile.outline_color)
        Hand_View.labelMedium(str(Hand_View.pickup_pile_sz), 150, 35)
    if Hand_View.controller._state.round == -1:
        Hand_View.ready_yes_btn.draw(Hand_View.display, Hand_View.ready_yes_btn.outline_color)
        Hand_View.ready_no_btn.draw(Hand_View.display, Hand_View.ready_no_btn.outline_color)
    Hand_View.sort_status_btn.draw(Hand_View.display, Hand_View.sort_status_btn.outline_color)
    Hand_View.sort_btn.draw(Hand_View.display, Hand_View.sort_btn.outline_color)
    Hand_View.prepare_card_btn.draw(Hand_View.display, Hand_View.prepare_card_btn.outline_color)
    Hand_View.clear_prepared_cards_btn.draw(Hand_View.display, Hand_View.clear_prepared_cards_btn.outline_color)
    Hand_View.play_prepared_cards_btn.draw(Hand_View.display, Hand_View.play_prepared_cards_btn.outline_color)
    Hand_View.discard_action_btn.draw(Hand_View.display, Hand_View.discard_action_btn.outline_color)
    return


def ClickedButton(Hand_View, pos):
    # carry out action after mouse clicked on button.
    if Hand_View.pickup_pile_sz > 0:
        if Hand_View.pickup_pile.isOver(pos):
            Hand_View.controller.pickUpPile()
            HandManagement.preparedCardsPlayedGui(Hand_View)
    if Hand_View.draw_pile.isOver(pos):
        Hand_View.controller.draw()
    elif Hand_View.sort_btn.isOver(pos):
        Hand_View.hand_info.sort(key=lambda wc: wc.key)
        Hand_View.hand_info = HandManagement.refreshXY(Hand_View, Hand_View.hand_info)
        if Hand_View.refresh_flag:  # if needed to rescale card size, then refreshXY again.
            Hand_View.hand_info = HandManagement.refreshXY(Hand_View, Hand_View.hand_info)
    elif Hand_View.controller._state.round == -1 and Hand_View.ready_yes_btn.isOver(pos):
        Hand_View.controller.setReady(True)
        Hand_View.last_round_hand = Hand_View.hand_info
        Hand_View.hand_info = []
        Hand_View.ready_color_idx = 6  # color of outline will be: UIC.outline_colors(ready_color_idx)
        Hand_View.not_ready_color_idx = 8  # color of outline will be: UIC.outline_colors(not_ready_color_idx)
    elif Hand_View.controller._state.round == -1 and Hand_View.ready_no_btn.isOver(pos):
        Hand_View.controller.setReady(False)
        # comment out next line and the line above where Hand_View.last_round_hand is defined
        # if you don't want last round's hand to reappear.
        Hand_View.hand_info = Hand_View.last_round_hand
        Hand_View.ready_color_idx = 2  # color of outline will be: UIC.outline_colors(ready_color_idx)
        Hand_View.not_ready_color_idx = 6  # color of outline will be: UIC.outline_colors(not_ready_color_idx)
    elif Hand_View.sort_status_btn.isOver(pos):
        Hand_View.hand_info.sort(
            key=lambda wc: (wc.img_clickable.x + (wc.status * UIC.Disp_Width))
        )
        Hand_View.hand_info = HandManagement.refreshXY(Hand_View, Hand_View.hand_info)
        # TODO: check if the following lines are ever used.
        if Hand_View.refresh_flag:  # if needed to rescale card size, then refreshXY again.
            Hand_View.hand_info = HandManagement.refreshXY(Hand_View, Hand_View.hand_info)
    elif Hand_View.prepare_card_btn.isOver(pos):
        Hand_View.already_prepared_cards = Hand_View.controller.getPreparedCards()
        Hand_View.wrapped_cards_to_prep = Hand_View.gatherSelected()
        Hand_View.wild_cards = Hand_View.controller.automaticallyPrepareCards(Hand_View.wrapped_cards_to_prep)
        # wild_cards contains a list of lists.
        # The latter contains [card that could not be automatically prepared, list of possible options for that card]
        # In HandAndFoot:
        #       wild_cards[k][0] rank should be 0 or 2 (a wild card) for all k.
        #       wild_cards[k][1] is list of playable card values: [1,4,5,6,7,8,9,10,11,12,13]
        Hand_View.num_wilds = len(Hand_View.wild_cards)
        Hand_View.newly_prepped_cards = Hand_View.controller.getPreparedCards()
        for element in Hand_View.already_prepared_cards:
            Hand_View.newly_prepped_cards.remove(element)
        # Hand_View newly_prepped_cards is now all prepared cards minus already_prepared_cards
        for wrappedcard in Hand_View.wrapped_cards_to_prep:
            if wrappedcard.card in Hand_View.newly_prepped_cards:
                Hand_View.newly_prepped_cards.remove(wrappedcard.card)
                wrappedcard.status = 2
                wrappedcard.img_clickable.changeOutline(4)
        # This concludes handling of the automatically prepared cards.
        # If there are cards that could not be automatically prepared, then HandView.nextEvent
        # will be looking for keystrokes (buttons are not involved), and HandView.assignWilds will
        # take care of assigning values and marking wilds as prepared.
    elif Hand_View.play_prepared_cards_btn.isOver(pos):
        Hand_View.controller.play()
        HandManagement.preparedCardsPlayedGui(Hand_View)
    elif Hand_View.clear_prepared_cards_btn.isOver(pos):
        Hand_View.controller.clearPreparedCards()
        HandManagement.clearPreparedCardsGui(Hand_View)
    elif Hand_View.discard_action_btn.isOver(pos):
        discard_list = Hand_View.gatherSelected()
        Hand_View.discard_confirm = Hand_View.discardConfirmation(Hand_View.discard_confirm, discard_list)
    return


def MouseHiLight(Hand_View, pos):
    if Hand_View.draw_pile.isOver(pos):
        Hand_View.draw_pile.changeOutline(1)
    else:
        Hand_View.draw_pile.changeOutline(0)
    if Hand_View.pickup_pile_sz > 0:
        if Hand_View.pickup_pile.isOver(pos):
            Hand_View.pickup_pile.changeOutline(1)
        else:
            Hand_View.pickup_pile.changeOutline(0)
    if Hand_View.ready_yes_btn.isOver(pos):
        Hand_View.ready_yes_btn.outline_color = UIC.outline_colors[Hand_View.ready_color_idx + 1]
    else:
        Hand_View.ready_yes_btn.outline_color = UIC.outline_colors[Hand_View.ready_color_idx]
    if Hand_View.ready_no_btn.isOver(pos):
        Hand_View.ready_no_btn.outline_color = UIC.outline_colors[Hand_View.not_ready_color_idx + 1]
    else:
        Hand_View.ready_no_btn.outline_color = UIC.outline_colors[Hand_View.not_ready_color_idx]
    if Hand_View.sort_status_btn.isOver(pos):
        Hand_View.sort_status_btn.outline_color = UIC.Black  # set outline color
    else:
        Hand_View.sort_status_btn.outline_color = UIC.Gray  # change outline
    if Hand_View.sort_btn.isOver(pos):
        Hand_View.sort_btn.outline_color = UIC.Black  # set outline color
    else:
        Hand_View.sort_btn.outline_color = UIC.Gray  # remove highlighted outline
    if Hand_View.prepare_card_btn.isOver(pos):
        Hand_View.prepare_card_btn.outline_color = UIC.Bright_Blue  # set outline color
    else:
        Hand_View.prepare_card_btn.outline_color = UIC.Blue  # remove highlighted outline
    if Hand_View.clear_prepared_cards_btn.isOver(pos):
        Hand_View.clear_prepared_cards_btn.outline_color = UIC.Bright_Red  # set outline color
    else:
        Hand_View.clear_prepared_cards_btn.outline_color = UIC.Red  # remove highlighted outline
    if Hand_View.play_prepared_cards_btn.isOver(pos):
        Hand_View.play_prepared_cards_btn.outline_color = UIC.Bright_Green  # set outline color
    else:
        Hand_View.play_prepared_cards_btn.outline_color = UIC.Green  # remove highlighted outline
    if Hand_View.discard_action_btn.isOver(pos):
        Hand_View.discard_action_btn.outline_color = UIC.Black  # set outline color
    else:
        Hand_View.discard_action_btn.outline_color = UIC.Bright_Red  # remove highlighted outline
