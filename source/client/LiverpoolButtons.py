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

This file is game specific because different games need different buttons, and may need them arranged
 differently, but most of this code should be useful for other games.
"""


def CreateButtons(hand_view, num_players=1):
    hand_view.num_players = num_players
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
    hand_view.sort_suit_al_btn = Btn.Button(UIC.White, 850, 55, 165, 20, text=' by suit (Aces=1) ')
    hand_view.sort_al_btn = Btn.Button(UIC.White, 850, 85, 165, 20, text=' by  no. (Aces=1) ')
    hand_view.sort_suit_ah_btn = Btn.Button(UIC.White, 1025, 55, 100, 20, text=' (Aces high)')
    hand_view.sort_ah_btn = Btn.Button(UIC.White, 1025, 85, 100, 20, text=' (Aces high)')
    hand_view.assign_cards_btns = [[]]  # list of card groups (each group is a set or run) for each player.
    hand_view.clear_prepared_cards_btn = Btn.Button(UIC.White, 320, 53, 225, 25, text='Clear prepared cards')
    hand_view.clear_selected_cards_btn = Btn.Button(UIC.White, 200, 90, 225, 25, text='Clear selected cards')
    hand_view.play_prepared_cards_btn = Btn.Button(UIC.White, 600, 53, 225, 25, text='Play prepared cards')
    hand_view.discard_action_btn = Btn.Button(UIC.Bright_Red, 190, 25, 100, 25, text='discard')
    hand_view.heart_btn = Btn.Button(UIC.White, 10, (UIC.Disp_Height - 30), 25, 25, text=str(u"\u2665"))
    # do not need discard pile at beginning of game, but do need initialize pickup_pile_sz and _outline
    hand_view.pickup_pile_sz = 0
    hand_view.pickup_pile_outline = UIC.outline_colors[0]
    return


def newRound(hand_view, sets_runs_tuple):
    """ At start of each round (after all players hit OK) this creates buttons used to assign cards."""

    #  For liverpool need multiple buttons to assign cards to appropriate set/run.
    #  and need to do this at beginning of each round, so those buttons are in this separate method.
    # btns = a list  of lists. Index of outer list = player_index for each player, index of inner list = # of group.
    # Buttons are used as keys in Dictionary of visible cards. (e.g. for  k_group, card_group in visible_cards.items())
    # k_group is a tuple of (player index, group number) and corresponds to one of the buttons about to be created.
    # Groups that are sets are always before groups that are runs (code depends on that).
    #
    hand_view.buttons_per_player = sets_runs_tuple[0] + sets_runs_tuple[1]
    hand_view.assign_cards_btns = [[]]
    w = 75  # width of following buttons
    h = 20  # height of following buttons
    if hand_view.num_players > 1:
        players_sp_w = UIC.Disp_Width / hand_view.num_players
    else:
        players_sp_w = UIC.Disp_Width
    players_sp_h = UIC.Disp_Height / 8
    players_sp_top = (UIC.Disp_Height / 5) + players_sp_h
    for idx in range(hand_view.num_players - 1):
        hand_view.assign_cards_btns.append([])
    for idx in range(hand_view.num_players):
        for setnum in range(sets_runs_tuple[0]):
            # hand_view.assign_cards_btns[idx].append([])
            txt = "set " + str(setnum+1)
            x = 10 + (players_sp_w*idx)
            y = players_sp_top + (players_sp_h*setnum)
            prepare_card_btn = Btn.Button(UIC.White, x, y, w, h, text=txt)
            hand_view.assign_cards_btns[idx].append(prepare_card_btn)
        for runnum in range(sets_runs_tuple[1]):
            txt = "run " + str(runnum+1)
            jdx = sets_runs_tuple[0] + runnum
            x = 10 + (players_sp_w * idx)
            y = players_sp_top + (players_sp_h * jdx)
            prepare_card_btn = Btn.Button(UIC.White, x, y, w, h, text=txt)
            # hand_view.assign_cards_btns[idx][jdx] = prepare_card_btn
            hand_view.assign_cards_btns[idx].append(prepare_card_btn)


def ButtonDisplay(hand_view):
    """ This updates draw pile and action buttons. It is called in HandView.update each render cycle. """

    # at beginning of round of Liverpool (or other shared_board game) create new buttons.
    # Review note - wait until all players hit OK else it crashes if you hit OK and then another player joins,
    # because then you won't have buttons for that player.
    if hand_view.need_updated_buttons and not hand_view.controller._state.round == -1:
        hand_view.RuleSetsButtons.newRound(hand_view, hand_view.Meld_Threshold[hand_view.round_index])
        hand_view.need_updated_buttons = False
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
        hand_view.need_updated_button = True # flags that will need to update assign buttons.
    hand_view.sort_status_btn.draw(hand_view.display, hand_view.sort_status_btn.outline_color)
    hand_view.sort_suit_al_btn.draw(hand_view.display, hand_view.sort_suit_al_btn.outline_color)
    hand_view.sort_al_btn.draw(hand_view.display, hand_view.sort_al_btn.outline_color)
    hand_view.sort_suit_ah_btn.draw(hand_view.display, hand_view.sort_suit_ah_btn.outline_color)
    hand_view.sort_ah_btn.draw(hand_view.display, hand_view.sort_ah_btn.outline_color)
    if not hand_view.need_updated_buttons:
        for idx in range(hand_view.num_players):
            for jdx in range(hand_view.buttons_per_player):
                prepare_card_btn = hand_view.assign_cards_btns[idx][jdx]
                prepare_card_btn.draw(hand_view.display, prepare_card_btn.outline_color)
    hand_view.clear_prepared_cards_btn.draw(hand_view.display, hand_view.clear_prepared_cards_btn.outline_color)
    hand_view.clear_selected_cards_btn.draw(hand_view.display, hand_view.clear_selected_cards_btn.outline_color)
    hand_view.play_prepared_cards_btn.draw(hand_view.display, hand_view.play_prepared_cards_btn.outline_color)
    hand_view.discard_action_btn.draw(hand_view.display, hand_view.discard_action_btn.outline_color)
    hand_view.heart_btn.draw(hand_view.display, hand_view.heart_btn.outline_color)
    return


def ClickedButton(hand_view, pos):
    """  Carry out action after mouse clicked on button. """
    if hand_view.pickup_pile_sz > 0:
        if hand_view.pickup_pile.isOver(pos):
            hand_view.controller.pickUpPile(notes[0])
    if hand_view.draw_pile.isOver(pos):
        if hand_view.pickup_pile_sz > 0:
            hand_view.controller.drawWithBuyOption()  # use different method for Liverpool than HandAndFoot
        else:
            hand_view.controller.draw()              # unless pile is empty (at start of each round)
    elif hand_view.sort_al_btn.isOver(pos):
        hand_view.hand_info.sort(key=lambda wc: wc.key[2])
        hand_view.hand_info = HandManagement.RefreshXY(hand_view, hand_view.hand_info)
    elif hand_view.sort_ah_btn.isOver(pos):
        hand_view.hand_info.sort(key=lambda wc: wc.key[1])
        hand_view.hand_info = HandManagement.RefreshXY(hand_view, hand_view.hand_info)
    elif hand_view.sort_suit_al_btn.isOver(pos):
        hand_view.hand_info.sort(key=lambda wc: wc.key[4])
        hand_view.hand_info = HandManagement.RefreshXY(hand_view, hand_view.hand_info)
    elif hand_view.sort_suit_ah_btn.isOver(pos):
        hand_view.hand_info.sort(key=lambda wc: wc.key[3])
        hand_view.hand_info = HandManagement.RefreshXY(hand_view, hand_view.hand_info)
    elif hand_view.sort_status_btn.isOver(pos):
        hand_view.hand_info.sort(
            key=lambda wc: (wc.img_clickable.x + (wc.status * UIC.Disp_Width))
        )
        hand_view.hand_info = HandManagement.RefreshXY(hand_view, hand_view.hand_info)
    elif hand_view.play_prepared_cards_btn.isOver(pos):
        hand_view.controller.sharedBoardPrepAndPlay(hand_view.visible_scards)
    elif hand_view.clear_prepared_cards_btn.isOver(pos):
        hand_view.controller.clearPreparedCards()
        hand_view.hand_info = HandManagement.ClearPreparedCardsInHandView(hand_view.hand_info)
    elif hand_view.clear_selected_cards_btn.isOver(pos):
        HandManagement.ClearSelectedCards(hand_view.hand_info)
    elif hand_view.discard_action_btn.isOver(pos):
        discard_list = hand_view.gatherSelected()
        hand_view.discard_confirm = hand_view.discardConfirmation(hand_view.discard_confirm, discard_list)
    elif hand_view.heart_btn.isOver(pos):
        hand_view.controller.note = "Believe in the heart of the cards " + str(u"\u2665")
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
    elif not hand_view.need_updated_buttons:
        #  loop through all the buttons which prepare cards by assigning them to a particular run or set
        for idx in range(len(hand_view.assign_cards_btns)):
            for jdx in range(hand_view.buttons_per_player):
                if hand_view.assign_cards_btns[idx][jdx].isOver(pos):
                    # put all selected cards in a list
                    hand_view.wr_crds_to_prep = hand_view.gatherSelected()
                    hand_view.controller.assignCardsToGroup((idx,jdx), hand_view.wr_crds_to_prep)
                    hand_view.prepped_cards = hand_view.controller.getPreparedCards()
                    for wrappedcard in hand_view.wr_crds_to_prep:
                        if wrappedcard.card in hand_view.prepped_cards:
                            wrappedcard.status = 2
                            wrappedcard.img_clickable.changeOutline(4)
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

    #  loop through all the assign card buttons (they aren't created until round has begun).
    if not hand_view.need_updated_buttons:
        for idx in range(hand_view.num_players):
            for jdx in range(hand_view.buttons_per_player):
                # prepare_card_btn = hand_view.assign_cards_btns[idx][jdx]
                if hand_view.assign_cards_btns[idx][jdx].isOver(pos):
                    hand_view.assign_cards_btns[idx][jdx].outline_color = UIC.Black  # set outline color
                else:
                    hand_view.assign_cards_btns[idx][jdx].outline_color = UIC.Gray  # remove highlighted outline
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

