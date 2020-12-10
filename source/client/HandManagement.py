import pygame
import client.Button as Btn
import client.UIConstants as UIC
from client.UICardWrapper import UICardWrapper
from time import sleep

"""This file contains methods used in displaying, selecting and sorting the hand"""


def WrapHand(hand_view, updated_hand, wrapped_hand):
    """Associate each card in updated_hand with a UICardWrapper

    updated_hand is list of cards in hand
    wrapped_hand is list of wrapped cards previously in hand (before update)
    If change in updated_hand is that new cards were added, then want to preserve location and
    status for cards that were already in hand.
    Note that discards are removed immediately after controller confirms discard legal.
    Variables from hand_view used: hand_view.hand_scaling (scaling and spacing of cards)
    """
    card_xy = (10, UIC.Table_Hand_Border + 40)
    updated_wrapped_hand = []
    if not updated_hand == []:
        for card in updated_hand:
            newcard = True
            # Check to see if card already in hand, and if it is change newcard to False.
            # Do this so if card already in hand, then its position and status is preserved.
            for already_wrapped in wrapped_hand:
                if newcard and card == already_wrapped.card:
                    newcard = False
                    card_wrapped = already_wrapped
                    # reset card_xy so new cards appear to right of old cards (card_xy[0] is max x-coord of cards).
                    card_xy = (max(card_xy[0], card_wrapped.img_clickable.x), card_xy[1])
                    wrapped_hand.remove(already_wrapped)
            if newcard:
                card_xy = (card_xy[0] + hand_view.hand_scaling[1], card_xy[1])
                card_wrapped = UICardWrapper(card, card_xy, hand_view.hand_scaling[0])
            updated_wrapped_hand.append(card_wrapped)
        # Should now have all the cards in the updated hand properly wrapped.
        # sort cards by location, so they will display more attractively and so RefreshXY will work properly if called.
        updated_wrapped_hand.sort(key=lambda wc: wc.img_clickable.x)
        # Next section checks all cards will be visible, and if hand too large, then it shrinks cards.
        # Once length of hand <= size at beginning of game it rescales cards to original size.
        maxX = UIC.Disp_Width - hand_view.hand_scaling[1]
        if card_xy[0] > maxX:
            # RefreshXY will remove any gaps between cards, and if necessary rescale the cards.
            updated_wrapped_hand = RefreshXY(hand_view, updated_wrapped_hand)
        if hand_view.hand_scaling[0] != UIC.scale and len(updated_wrapped_hand) <= hand_view.deal_size:
            hand_view.hand_scaling = (UIC.scale, UIC.Card_Spacing)
            updated_wrapped_hand = RescaleCards(hand_view, updated_wrapped_hand)
            updated_wrapped_hand = RefreshXY(hand_view, updated_wrapped_hand)
    return updated_wrapped_hand


def ClearPreparedCardsInHandView(wrapped_hand):
    for element in wrapped_hand:
        if element.status == 2:
            element.status = 0
            element.img_clickable.changeOutline(0)
    return wrapped_hand


def ClearSelectedCards(wrapped_hand):
    for element in wrapped_hand:
        if element.status == 1:
            element.status = 0
            element.img_clickable.changeOutline(0)


def RefreshXY(hand_view, original_wrapped_hand, layout_option=1):
    # After sorting need to refresh XY coords, may also wish to refresh card's xy coordinates when hand large
    maxX = UIC.Disp_Width - hand_view.hand_scaling[1]
    if not layout_option == 1:
        print('the only layout supported now is cards in a line, left to right')
    refreshed_wrapped_hand = []
    card_xy = (10, UIC.Table_Hand_Border + 40)
    for element in original_wrapped_hand:
        element.img_clickable.x = card_xy[0]
        element.img_clickable.y = card_xy[1]
        card_xy = (card_xy[0] + hand_view.hand_scaling[1], card_xy[1])
        refreshed_wrapped_hand.append(element)
    if card_xy[0] > maxX:
        scalingfactor = maxX / card_xy[0]
        hand_view.hand_scaling = (scalingfactor * hand_view.hand_scaling[0], scalingfactor * hand_view.hand_scaling[1])
        rescaled_wrapped_hand = RescaleCards(hand_view, refreshed_wrapped_hand)
        refreshed_wrapped_hand = rescaled_wrapped_hand
    return refreshed_wrapped_hand


def RescaleCards(hand_view, original_wrapped_hand):
    rescaled_wrapped_hand = []
    card_xy = (10, UIC.Table_Hand_Border + 40)
    for element in original_wrapped_hand:
        loc_xy = (card_xy[0], card_xy[1])
        scaled_element = UICardWrapper(element.card, loc_xy, hand_view.hand_scaling[0])
        scaled_element.status = element.status
        scaled_element.img_clickable.outline_index = element.img_clickable.outline_index
        rescaled_wrapped_hand.append(scaled_element)
        # set card_xy for next card in original_wrapped_hand.
        card_xy = (card_xy[0] + hand_view.hand_scaling[1], card_xy[1])
    return rescaled_wrapped_hand


def ShowHolding(hand_view, wrapped_cards):
    wrapped_cards.sort(key=lambda wc: wc.img_clickable.x)
    for wrapped_element in wrapped_cards:
        color = UIC.outline_colors[wrapped_element.img_clickable.outline_index]
        loc_xy = (wrapped_element.img_clickable.x, wrapped_element.img_clickable.y)
        wrapped_element.img_clickable.draw(hand_view.display, loc_xy, color)
    return


def MouseHiLight(wrapped_hand, pos):
    for element in wrapped_hand:
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
    return


def ManuallyAssign(hand_view):
    """ Cards that cannot be automatically assigned to sets must be manually assigned.

    Used in HandAndFoot (HandAndFootButtons.py contains methods that eventually trigger this method).
    Only wild cards need to be manually assigned.
    For other games it may be more complex (e.g. games with runs and sets)
    """
    textnote = "Designate one of " + str(hand_view.num_wilds) + "  wildcard(s)"
    textnote = textnote + " enter value by typing:  1-9, 0 (for ten), j, q, k or a. "
    acceptable_keys = hand_view.wild_cards[0][1]
    hand_view.controller.note = textnote
    this_wild = hand_view.wild_cards[0][0]
    if hand_view.event.key == pygame.K_a:
        wild_key = 1
    elif hand_view.event.key == pygame.K_0:
        wild_key = 10
    elif hand_view.event.key == pygame.K_j:
        wild_key = 11
    elif hand_view.event.key == pygame.K_q:
        wild_key = 12
    elif hand_view.event.key == pygame.K_k:
        wild_key = 13
    elif hand_view.event.unicode in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
        wild_key = int(hand_view.event.unicode)
    else:
        hand_view.controller.note = 'invalid key:' + textnote
        wild_key = 666
    if wild_key in acceptable_keys:
        hand_view.controller.note = str(this_wild) + ' will be a ' + str(wild_key)
        icount = 0
        for wrappedcard in hand_view.wrapped_cards_to_prep:
            if wrappedcard.card == this_wild and icount == 0 and wrappedcard.status == 1:
                icount = 1
                wrappedcard.status = 2
                wrappedcard.img_clickable.changeOutline(4)
        hand_view.controller.prepareCard(wild_key, this_wild)
        if hand_view.num_wilds > 0:
            hand_view.wild_cards = hand_view.wild_cards[1:]
        hand_view.num_wilds = len(hand_view.wild_cards)
    return


def wildsHiLo_step1(hand_view):
    """ Used in Liverpool and other games with runs to assign wilds.

    Assigning wilds is as automated as possible, so this is only used to determine
    if wilds are high or low.  There should be at most one wild card in unassigned_wilds.
    """
    # hand_view.controller.unassigned_wilds_dict[k_group] = [processed_group, wild_options, unassigned_wilds]

    for k_group, group_info in hand_view.controller.unassigned_wilds_dict.items():
        processed_group = group_info[0]
        unassigned_wilds = group_info[2]
        if len(unassigned_wilds) > 0:
            textnote = "USE KEY STROKES!! For the " + str(processed_group[1].suit) + " run: "
            for card in processed_group:
                textnote = textnote + str(card.number) + ','
            textnote = textnote + "should the wild be high or low?  type H or L ?"
            hand_view.controller.note = textnote
            hand_view.bad_strokes = 0   # if too many bad key-strokes, make wild automatically high.
    return

def wildsHiLo_step2(hand_view):
    """ Used in Liverpool and other games with runs to assign wilds.

    Assigning wilds is as automated as possible, so this is only used to determine
    if wilds are high or low.  There should be at most one wild card in unassigned_wilds.
    """
    # hand_view.controller.unassigned_wilds_dict[k_group] = [processed_group, wild_options, unassigned_wilds]

    key_list = []
    for k_group in hand_view.controller.unassigned_wilds_dict.keys():
        key_list.append(k_group)
    if len(key_list) > 0:
        k_group = key_list[0]
        group_info = hand_view.controller.unassigned_wilds_dict[k_group]
        processed_group = group_info[0]
        wild_options = group_info[1]
        unassigned_wilds = group_info[2]
        if len(unassigned_wilds) > 0:
            this_wild = unassigned_wilds[0]
            if hand_view.event.type == pygame.KEYDOWN:
                if hand_view.event.key == pygame.K_l:
                    this_wild.tempnumber = wild_options[0]
                    del hand_view.controller.unassigned_wilds_dict[k_group]
                elif hand_view.event.key == pygame.K_h:
                    this_wild.tempnumber = wild_options[1]
                    del hand_view.controller.unassigned_wilds_dict[k_group]
                else:
                    hand_view.bad_strokes = hand_view.bad_strokes + 1
                    hand_view.controller.note = hand_view.controller.note + 'INVALID KEY STROKE'
                    if hand_view.bad_strokes > 4:
                        hand_view.controller.note = 'Invalid response more than 3 times, made wild card high'
                        this_wild.tempnumber = wild_options[1]
                        del hand_view.controller.unassigned_wilds_dict[k_group]
                processed_group.append(this_wild)
                processed_group.sort(key=lambda wc: wc.tempnumber)
                hand_view.controller.processed_full_board[k_group] = processed_group
            # reset count of num_wilds.
            hand_view.num_wilds = len(hand_view.controller.unassigned_wilds_dict.keys())
            if hand_view.num_wilds > 0:
                wildsHiLo_step1(hand_view)
            else:
                hand_view.controller.play()
        else:
            print('In HandManagement.wildsHiLo_step2.')
            print('Why is there an entry in hand_view.controller.unassigned_wilds_dict with no unassigned_wilds?')
    return



