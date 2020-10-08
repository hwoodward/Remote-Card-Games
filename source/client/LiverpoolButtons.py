import pygame
import client.Button as Btn
from client.ClickableImage import ClickableImage as ClickImg
from common.Liverpool import notes
import client.HandManagement as HandManagement
import client.UIConstants as UIC
from client.UICardWrapper import UICardWrapper

"""This file contains methods used in displaying the buttons that enable the user to take actions

If a button is clicked, then typically 1 or 2 methods are called. The first initiates communication with the server, 
and when necessary a 2nd updates the display to reflect the action taken.  
Discards are confirmed within the GUI, and that code is currently split between this file and HandView.

This file is Liverpool specific because different games may need additional buttons, and may need them arranged
 differently, but most of this code should be useful for other games.
"""


def CreateButtons(hand_view):
    """This creates the buttons and text used for game. """
    hand_view.draw_pile = ClickImg(UIC.Back_Img, 10, 25, UIC.Back_Img.get_width(), UIC.Back_Img.get_height(), 0)
    hand_view.ready_yes_btn = \
        Btn.Button(UIC.White, (UIC.Disp_Width - 150), (UIC.Disp_Height - 70), 125, 25, text='Ready:YES')
    hand_view.ready_color_idx = 2  # color of outline will be: UIC.outline_colors(ready_color_idx)
    hand_view.ready_no_btn = \
        Btn.Button(UIC.White, (UIC.Disp_Width - 150), (UIC.Disp_Height - 30), 125, 25, text='Ready:NO')
    hand_view.not_ready_color_idx = 6  # color of outline will be: UIC.outline_colors(ready_color_idx)
    hand_view.round_indicator_xy = ((UIC.Disp_Width - 100), (UIC.Disp_Height - 20))
    hand_view.sort_status_btn = Btn.Button(UIC.White, 850, 25, 275, 20, text=' sort by status ')
    hand_view.sort_suit_al_btn = Btn.Button(UIC.White, 850, 50, 175, 20, text=' by suit (Aces=1) ')
    hand_view.sort_al_btn = Btn.Button(UIC.White, 850, 75, 175, 20, text=' by  no. (Aces=1) ')
    hand_view.sort_suit_ah_btn = Btn.Button(UIC.White, 1025, 50, 100, 20, text=' (Aces high)')
    hand_view.sort_ah_btn = Btn.Button(UIC.White, 1025, 75, 100, 20, text=' (Aces high)')
    #  For liverpool need multiple buttons to assign cards to appropriate set/run.
    #  and need to do this at beginning of each round, so those buttons are in separate method: newRound
    hand_view.btn_keys = []
    hand_view.assign_cards_btns = {} # [[]]
    hand_view.assigned_cards = {}
    hand_view.clear_prepared_cards_btn = Btn.Button(UIC.White, 320, 53, 225, 25, text='Clear prepared cards')
    hand_view.clear_selected_cards_btn = Btn.Button(UIC.White, 200, 90, 225, 25, text='Clear selected cards')
    hand_view.play_prepared_cards_btn = Btn.Button(UIC.White, 600, 53, 225, 25, text='Play prepared cards')
    hand_view.discard_action_btn = Btn.Button(UIC.Bright_Red, 190, 25, 100, 25, text='discard')
    # for HandAndFoot do not need discard pile at beginning of game, but do need initialize pickup_pile_sz and _outline
    hand_view.pickup_pile_sz = 0
    hand_view.pickup_pile_outline = UIC.outline_colors[0]
    return


def newRound(hand_view, sets_runs_tuple, num_players=1):
    """ At start of each round this creates buttons used to assign cards."""

    # Unlike columns for players (found in TableView.playerByPlayer)
    # it does not refresh if a player leaves mid-round.
    # todo: consider whether it should update if a player leaves mid-round.

    print(sets_runs_tuple)
    hand_view.assign_cards_btns = {} # []
    if num_players > 1:
        players_sp_w = UIC.Disp_Width / num_players
    else:
        players_sp_w = UIC.Disp_Width
    players_sp_h = UIC.Disp_Height / 8
    players_sp_top = (UIC.Disp_Height / 5) + players_sp_h
    for idx in range(num_players):
        w = 75  # width of following buttons
        h = 25  # height of following buttons
        for setnum in range(sets_runs_tuple[0]):
            txt = "set " + str(setnum+1)
            x = 100 + (players_sp_w*idx)
            y = players_sp_top + (players_sp_h*setnum)
            prepare_card_btn = Btn.Button(UIC.White, x, y, w, h, text=txt)
            btn_key = (idx, setnum)
            hand_view.btn_keys.append(btn_key)
            hand_view.assign_cards_btns[btn_key] = prepare_card_btn
            hand_view.assigned_cards[btn_key] = []  # this list will contain cards in a set.
        for runnum in range(sets_runs_tuple[1]):
            txt = "run " + str(runnum+1)
            jdx = sets_runs_tuple[0] + runnum
            x = 100 + (players_sp_w * idx)
            y = players_sp_top + (players_sp_h * jdx)
            prepare_card_btn = Btn.Button(UIC.White, x, y, w, h, text=txt)
            btn_key = (idx, jdx)
            hand_view.btn_keys.append(btn_key)
            hand_view.assign_cards_btns[btn_key] = prepare_card_btn
            hand_view.assigned_cards[btn_key] = []  # this list will contain cards in a run.
            #  oneplayers_assignbtns.append(prepare_card_btn)


def ButtonDisplay(hand_view):
    """ This updates draw pile and action buttons. It is called in HandView.update each render cycle. """
    loc_xy = (hand_view.draw_pile.x, hand_view.draw_pile.y)
    hand_view.draw_pile.draw(hand_view.display, loc_xy, hand_view.draw_pile.outline_color)
    # update discard info and redraw
    discard_info = hand_view.controller.getDiscardInfo()
    hand_view.top_discard = discard_info[0]
    hand_view.pickup_pile_sz = discard_info[1]
    if hand_view.pickup_pile_sz > 0:
        # pickup_pile needs new clickable image each time any player discards or picks up the pile.
        # Next few lines insure pickup_pile image is up to date.
        hand_view.top_discard_wrapped = UICardWrapper(hand_view.top_discard, (100, 25), UIC.scale)
        hand_view.pickup_pile = hand_view.top_discard_wrapped.img_clickable
        loc_xy = (hand_view.pickup_pile.x, hand_view.pickup_pile.y)
        # UICardWrapper sets outline color to no outline, next line resets outline to proper value.
        hand_view.pickup_pile.outline_color = hand_view.pickup_pile_outline
        hand_view.pickup_pile.draw(hand_view.display, loc_xy, hand_view.pickup_pile.outline_color)
        hand_view.labelMedium(str(hand_view.pickup_pile_sz), 150, 35)
    if hand_view.controller._state.round == -1:
        hand_view.ready_yes_btn.draw(hand_view.display, hand_view.ready_yes_btn.outline_color)
        hand_view.ready_no_btn.draw(hand_view.display, hand_view.ready_no_btn.outline_color)
    hand_view.sort_status_btn.draw(hand_view.display, hand_view.sort_status_btn.outline_color)
    hand_view.sort_suit_al_btn.draw(hand_view.display, hand_view.sort_suit_al_btn.outline_color)
    hand_view.sort_al_btn.draw(hand_view.display, hand_view.sort_al_btn.outline_color)
    hand_view.sort_suit_ah_btn.draw(hand_view.display, hand_view.sort_suit_ah_btn.outline_color)
    hand_view.sort_ah_btn.draw(hand_view.display, hand_view.sort_ah_btn.outline_color)
    for key in hand_view.btn_keys:
        prepare_card_btn = hand_view.assign_cards_btns[key]
        prepare_card_btn.draw(hand_view.display, prepare_card_btn.outline_color)
    hand_view.clear_prepared_cards_btn.draw(hand_view.display, hand_view.clear_prepared_cards_btn.outline_color)
    hand_view.clear_selected_cards_btn.draw(hand_view.display, hand_view.clear_selected_cards_btn.outline_color)
    hand_view.play_prepared_cards_btn.draw(hand_view.display, hand_view.play_prepared_cards_btn.outline_color)
    hand_view.discard_action_btn.draw(hand_view.display, hand_view.discard_action_btn.outline_color)
    return


def ClickedButton(hand_view, pos):
    """  Carry out action after mouse clicked on button. """
    if hand_view.pickup_pile_sz > 0:
        if hand_view.pickup_pile.isOver(pos):
            hand_view.controller.pickUpPile(notes[0])
    if hand_view.draw_pile.isOver(pos):
        hand_view.controller.draw()
    elif hand_view.sort_al_btn.isOver(pos):
        hand_view.hand_info.sort(key=lambda wc: wc.key_LP[1])
        hand_view.hand_info = HandManagement.RefreshXY(hand_view, hand_view.hand_info)
    elif hand_view.sort_ah_btn.isOver(pos):
        hand_view.hand_info.sort(key=lambda wc: wc.key_LP[0])
        hand_view.hand_info = HandManagement.RefreshXY(hand_view, hand_view.hand_info)
    elif hand_view.sort_suit_al_btn.isOver(pos):
        hand_view.hand_info.sort(key=lambda wc: wc.key_LP[3])
        hand_view.hand_info = HandManagement.RefreshXY(hand_view, hand_view.hand_info)
    elif hand_view.sort_suit_ah_btn.isOver(pos):
        hand_view.hand_info.sort(key=lambda wc: wc.key_LP[2])
        hand_view.hand_info = HandManagement.RefreshXY(hand_view, hand_view.hand_info)
    elif hand_view.sort_status_btn.isOver(pos):
        hand_view.hand_info.sort(
            key=lambda wc: (wc.img_clickable.x + (wc.status * UIC.Disp_Width))
        )
        hand_view.hand_info = HandManagement.RefreshXY(hand_view, hand_view.hand_info)
    elif hand_view.play_prepared_cards_btn.isOver(pos):
        hand_view.controller.play()
    elif hand_view.clear_prepared_cards_btn.isOver(pos):
        hand_view.controller.clearPreparedCards()
        hand_view.hand_info = HandManagement.ClearPreparedCardsInHandView(hand_view.hand_info)
    elif hand_view.clear_selected_cards_btn.isOver(pos):
        HandManagement.ClearSelectedCards(hand_view.hand_info)
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
        # if you don't want last round's hand to reappear, then
        # comment out line about 7 lines above this where hand_view.last_round_hand is defined
        hand_view.hand_info = hand_view.last_round_hand
        hand_view.ready_color_idx = 2  # color of outline will be: UIC.outline_colors(ready_color_idx)
        hand_view.not_ready_color_idx = 6  # color of outline will be: UIC.outline_colors(not_ready_color_idx)
    else:
        #  loop through all the buttons which prepare cards by assigning them to a particular run or set
        #Todo: this currently only supports sets, need to expand to support runs, too.
        for key in hand_view.btn_keys:
            prepare_card_btn = hand_view.assign_cards_btns[key]
            if prepare_card_btn.isOver(pos):
                # put all selected cards in a list
                hand_view.wrapped_cards_to_prep = hand_view.gatherSelected()
                hand_view.wild_cards = hand_view.controller.automaticallyPrepareCards(hand_view.wrapped_cards_to_prep)
                # wild_cards contains a list of lists.
                # The outer list contains [card that could not be automatically prepared,
                # list of possible options for that card]
                #       wild_cards[k][0] rank should be 0 (a joker)) for all k.
                #       wild_cards[k][1] is list of playable card values (might be anything in list of 1 to 13).
                #       Might make wild_cards[k][1] more sophisticated, so to add to a run of spades = [2,3,4,5]
                #       wild_cards[k][1] would be [1,6,7,8,9,10,11,12,13] << need number > 6 because other cards
                #       might also be prepared.
                hand_view.num_wilds = len(hand_view.wild_cards)
                hand_view.prepped_cards = hand_view.controller.getPreparedCards()
                for wrappedcard in hand_view.wrapped_cards_to_prep:
                    if wrappedcard.card in hand_view.prepped_cards:
                        wrappedcard.status = 2
                        wrappedcard.img_clickable.changeOutline(4)
                # This concludes handling of the automatically prepared cards.
                # If there are cards that could not be automatically prepared, then HandView.nextEvent
                # will be looking for keystrokes (buttons are not involved), and HandView.assignWilds will
                # take care of assigning values and marking wilds as prepared.
    return


def MouseHiLight(hand_view, pos):
    if hand_view.draw_pile.isOver(pos):
        hand_view.draw_pile.changeOutline(1)
    else:
        hand_view.draw_pile.changeOutline(0)
    if hand_view.pickup_pile_sz > 0:
        if hand_view.pickup_pile.isOver(pos):
            hand_view.pickup_pile.changeOutline(1)
            hand_view.pickup_pile_outline = hand_view.pickup_pile.outline_color
        else:
            hand_view.pickup_pile.changeOutline(0)
            hand_view.pickup_pile_outline = hand_view.pickup_pile.outline_color
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
    if hand_view.sort_al_btn.isOver(pos):
        hand_view.sort_al_btn.outline_color = UIC.Black  # set outline color
    else:
        hand_view.sort_al_btn.outline_color = UIC.Gray  # remove highlighted outline
    if hand_view.sort_ah_btn.isOver(pos):
        hand_view.sort_ah_btn.outline_color = UIC.Black  # set outline color
    else:
        hand_view.sort_ah_btn.outline_color = UIC.Gray  # remove highlighted outline
    if hand_view.sort_suit_al_btn.isOver(pos):
        hand_view.sort_suit_al_btn.outline_color = UIC.Black  # set outline color
    else:
        hand_view.sort_suit_al_btn.outline_color = UIC.Gray  # remove highlighted outline
    if hand_view.sort_suit_ah_btn.isOver(pos):
        hand_view.sort_suit_ah_btn.outline_color = UIC.Black  # set outline color
    else:
        hand_view.sort_suit_ah_btn.outline_color = UIC.Gray  # remove highlighted outline

    #  loop through all the assign card buttons
    for key in hand_view.btn_keys:
        prepare_card_btn = hand_view.assign_cards_btns[key]
        if prepare_card_btn.isOver(pos):
            prepare_card_btn.outline_color = UIC.Black  # set outline color
        else:
            prepare_card_btn.outline_color = UIC.Gray  # remove highlighted outline
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

