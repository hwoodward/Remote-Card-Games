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


def CreateButtons(hand_view):
    """This creates the buttons used for HandAndFoot. """
    hand_view.draw_pile = ClickImg(UIC.Back_Img, 10, 25, UIC.Back_Img.get_width(), UIC.Back_Img.get_height(), 0)
    hand_view.ready_yes_btn = Btn.Button(UIC.White, (UIC.Disp_Width - 150), (UIC.Disp_Height - 70), 125, 25, text='Ready:YES')
    hand_view.ready_color_idx = 2  # color of outline will be: UIC.outline_colors(ready_color_idx)
    hand_view.ready_no_btn = Btn.Button(UIC.White, (UIC.Disp_Width - 150), (UIC.Disp_Height - 30), 125, 25, text='Ready:NO')
    hand_view.not_ready_color_idx = 6  # color of outline will be: UIC.outline_colors(ready_color_idx)
    hand_view.sort_status_btn = Btn.Button(UIC.White, 900, 25, 225, 25, text='sort by status')
    hand_view.sort_btn = Btn.Button(UIC.White, 900, 75, 225, 25, text='sort by number')
    hand_view.prepare_card_btn = Btn.Button(UIC.White, 400, 15, 345, 25, text='Selected cards -> prepared cards')
    hand_view.clear_prepared_cards_btn = Btn.Button(UIC.White, 320, 53, 225, 25, text='Clear prepared cards')
    hand_view.clear_selected_cards_btn = Btn.Button(UIC.White, 200, 90, 225, 25, text='Clear selected cards')
    hand_view.play_prepared_cards_btn = Btn.Button(UIC.White, 600, 53, 225, 25, text='Play prepared cards')
    hand_view.discard_action_btn = Btn.Button(UIC.Bright_Red, 190, 25, 100, 25, text='discard')
    # for HandAndFoot do not need discard pile at beginning of game, but do need initiate pickup_pile_sz.
    hand_view.pickup_pile_sz = 0
    return

def ButtonDisplay(hand_view):
    """ This updates draw pile and action buttons. It is called in HandView.update each render cycle. """
    loc_xy = (hand_view.draw_pile.x, hand_view.draw_pile.y)
    hand_view.draw_pile.draw(hand_view.display, loc_xy, hand_view.draw_pile.outline_color)
    # update discard info and redraw
    discard_info = hand_view.controller.getDiscardInfo()
    hand_view.top_discard = discard_info[0]
    hand_view.pickup_pile_sz = discard_info[1]
    if hand_view.pickup_pile_sz > 0:
        hand_view.top_discard_wrapped = UICardWrapper(hand_view.top_discard, (100, 25), UIC.scale)
        hand_view.pickup_pile = hand_view.top_discard_wrapped.img_clickable
        loc_xy = (hand_view.pickup_pile.x, hand_view.pickup_pile.y)
        hand_view.pickup_pile.draw(hand_view.display, loc_xy, hand_view.pickup_pile.outline_color)
        hand_view.labelMedium(str(hand_view.pickup_pile_sz), 150, 35)
    if hand_view.controller._state.round == -1:
        hand_view.ready_yes_btn.draw(hand_view.display, hand_view.ready_yes_btn.outline_color)
        hand_view.ready_no_btn.draw(hand_view.display, hand_view.ready_no_btn.outline_color)
    hand_view.sort_status_btn.draw(hand_view.display, hand_view.sort_status_btn.outline_color)
    hand_view.sort_btn.draw(hand_view.display, hand_view.sort_btn.outline_color)
    hand_view.prepare_card_btn.draw(hand_view.display, hand_view.prepare_card_btn.outline_color)
    hand_view.clear_prepared_cards_btn.draw(hand_view.display, hand_view.clear_prepared_cards_btn.outline_color)
    hand_view.clear_selected_cards_btn.draw(hand_view.display, hand_view.clear_selected_cards_btn.outline_color)
    hand_view.play_prepared_cards_btn.draw(hand_view.display, hand_view.play_prepared_cards_btn.outline_color)
    hand_view.discard_action_btn.draw(hand_view.display, hand_view.discard_action_btn.outline_color)
    return

def ClickedButton(hand_view, pos):
    """  Carry out action after mouse clicked on button. """
    if hand_view.pickup_pile_sz > 0:
        if hand_view.pickup_pile.isOver(pos):
            hand_view.controller.pickUpPile()
            HandManagement.preparedCardsPlayed(hand_view)
    if hand_view.draw_pile.isOver(pos):
        hand_view.controller.draw()
    elif hand_view.sort_btn.isOver(pos):
        hand_view.hand_info.sort(key=lambda wc: wc.key)
        hand_view.hand_info = HandManagement.refreshXY(hand_view, hand_view.hand_info)
    elif hand_view.sort_status_btn.isOver(pos):
        hand_view.hand_info.sort(
            key=lambda wc: (wc.img_clickable.x + (wc.status * UIC.Disp_Width))
        )
        hand_view.hand_info = HandManagement.refreshXY(hand_view, hand_view.hand_info)
    elif hand_view.prepare_card_btn.isOver(pos):
        hand_view.already_prepared_cards = hand_view.controller.getPreparedCards()
        hand_view.wrapped_cards_to_prep = hand_view.gatherSelected()
        hand_view.wild_cards = hand_view.controller.automaticallyPrepareCards(hand_view.wrapped_cards_to_prep)
        # wild_cards contains a list of lists.
        # The latter contains [card that could not be automatically prepared, list of possible options for that card]
        # In HandAndFoot:
        #       wild_cards[k][0] rank should be 0 or 2 (a wild card) for all k.
        #       wild_cards[k][1] is list of playable card values: [1,4,5,6,7,8,9,10,11,12,13]
        hand_view.num_wilds = len(hand_view.wild_cards)
        hand_view.newly_prepped_cards = hand_view.controller.getPreparedCards()
        for element in hand_view.already_prepared_cards:
            hand_view.newly_prepped_cards.remove(element)
        # hand_view newly_prepped_cards is now all prepared cards minus already_prepared_cards
        for wrappedcard in hand_view.wrapped_cards_to_prep:
            if wrappedcard.card in hand_view.newly_prepped_cards:
                hand_view.newly_prepped_cards.remove(wrappedcard.card)
                wrappedcard.status = 2
                wrappedcard.img_clickable.changeOutline(4)
        # This concludes handling of the automatically prepared cards.
        # If there are cards that could not be automatically prepared, then HandView.nextEvent
        # will be looking for keystrokes (buttons are not involved), and HandView.assignWilds will
        # take care of assigning values and marking wilds as prepared.
    elif hand_view.play_prepared_cards_btn.isOver(pos):
        hand_view.controller.play()
        HandManagement.preparedCardsPlayed(hand_view)
    elif hand_view.clear_prepared_cards_btn.isOver(pos):
        hand_view.controller.clearPreparedCards()
        hand_view.hand_info = HandManagement.clearPreparedCardsInHandView(hand_view.hand_info)
    elif hand_view.clear_selected_cards_btn.isOver(pos):
        HandManagement.clearSelectedCards(hand_view)
    elif hand_view.discard_action_btn.isOver(pos):
        discard_list = hand_view.gatherSelected()
        hand_view.discard_confirm = hand_view.discardConfirmation(hand_view.discard_confirm, discard_list)
    # following two buttons only appear at beginning of round, used to notify server ready to begin round.
    elif hand_view.controller._state.round == -1 and hand_view.ready_yes_btn.isOver(pos):
        hand_view.controller.setReady(True)
        hand_view.last_round_hand = hand_view.hand_info
        hand_view.hand_info = []
        hand_view.ready_color_idx = 6  # color of outline will be: UIC.outline_colors(ready_color_idx)
        hand_view.not_ready_color_idx = 8  # color of outline will be: UIC.outline_colors(not_ready_color_idx)
    elif hand_view.controller._state.round == -1 and hand_view.ready_no_btn.isOver(pos):
        hand_view.controller.setReady(False)
        # comment out next line and the line above where hand_view.last_round_hand is defined
        # if you don't want last round's hand to reappear.
        hand_view.hand_info = hand_view.last_round_hand
        hand_view.ready_color_idx = 2  # color of outline will be: UIC.outline_colors(ready_color_idx)
        hand_view.not_ready_color_idx = 6  # color of outline will be: UIC.outline_colors(not_ready_color_idx)
    return

def MouseHiLight(hand_view, pos):
    if hand_view.draw_pile.isOver(pos):
        hand_view.draw_pile.changeOutline(1)
    else:
        hand_view.draw_pile.changeOutline(0)
    if hand_view.pickup_pile_sz > 0:
        if hand_view.pickup_pile.isOver(pos):
            hand_view.pickup_pile.changeOutline(1)
        else:
            hand_view.pickup_pile.changeOutline(0)
    if hand_view.ready_yes_btn.isOver(pos):
        hand_view.ready_yes_btn.outline_color = UIC.outline_colors[hand_view.ready_color_idx + 1]
    else:
        hand_view.ready_yes_btn.outline_color = UIC.outline_colors[hand_view.ready_color_idx]
    if hand_view.ready_no_btn.isOver(pos):
        hand_view.ready_no_btn.outline_color = UIC.outline_colors[hand_view.not_ready_color_idx + 1]
    else:
        hand_view.ready_no_btn.outline_color = UIC.outline_colors[hand_view.not_ready_color_idx]
    if hand_view.sort_status_btn.isOver(pos):
        hand_view.sort_status_btn.outline_color = UIC.Black  # set outline color
    else:
        hand_view.sort_status_btn.outline_color = UIC.Gray  # change outline
    if hand_view.sort_btn.isOver(pos):
        hand_view.sort_btn.outline_color = UIC.Black  # set outline color
    else:
        hand_view.sort_btn.outline_color = UIC.Gray  # remove highlighted outline
    if hand_view.prepare_card_btn.isOver(pos):
        hand_view.prepare_card_btn.outline_color = UIC.Bright_Blue  # set outline color
    else:
        hand_view.prepare_card_btn.outline_color = UIC.Blue  # remove highlighted outline
    if hand_view.clear_prepared_cards_btn.isOver(pos):
        hand_view.clear_prepared_cards_btn.outline_color = UIC.Bright_Red  # set outline color
    else:
        hand_view.clear_prepared_cards_btn.outline_color = UIC.Red  # remove highlighted outline
    if hand_view.clear_selected_cards_btn.isOver(pos):
        hand_view.clear_selected_cards_btn.outline_color = UIC.Bright_Orange  # set outline color
    else:
        hand_view.clear_selected_cards_btn.outline_color = UIC.Orange  # remove highlighted outline
    if hand_view.play_prepared_cards_btn.isOver(pos):
        hand_view.play_prepared_cards_btn.outline_color = UIC.Bright_Green  # set outline color
    else:
        hand_view.play_prepared_cards_btn.outline_color = UIC.Green  # remove highlighted outline
    if hand_view.discard_action_btn.isOver(pos):
        hand_view.discard_action_btn.outline_color = UIC.Black  # set outline color
    else:
        hand_view.discard_action_btn.outline_color = UIC.Bright_Red  # remove highlighted outline
    return
