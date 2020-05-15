import pygame
import client.Button as Btn
import client.UIConstants as UIC
from client.UICardWrapper import UICardWrapper

"""This file contains methods used in displaying, selecting and sorting the hand"""


def wrapHand(hand_view, updated_hand, wrapped_hand):
    """Associate each card in updated_hand with a UICardWrapper

    if change is that new cards were added, then want to preserve location and status for cards that were
    already in hand.
    If cards were played, then the wrapped cards that are removed should be those cards with status = 2
    (prepared cards).
    Note that discards are removed immediately after controller confirms discard legal.
    Two variables from hand_view are used: hand_view.hand_scaling (size of cards) and hand_view.refresh_flag
    """
    card_xy = (10, UIC.Table_Hand_Border + 40)
    # sort cards so that if prepared cards were played, those are the instances of the cards that are removed.
    old_wrapped_hand = sorted(wrapped_hand, key=lambda x: x.status)
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
                card_xy = (card_xy[0] + hand_view.hand_scaling[1], card_xy[1])
                card_wrapped = UICardWrapper(card, card_xy, hand_view.hand_scaling[0])
            updated_wrapped_hand.append(card_wrapped)
        maxX = UIC.Disp_Width - hand_view.hand_scaling[1]
        if (card_xy[0] > maxX):
            scalingfactor = maxX / card_xy[0]
            hand_view.hand_scaling = (scalingfactor * hand_view.hand_scaling[0], scalingfactor * hand_view.hand_scaling[1])
            updated_wrapped_hand = rescaleCards(hand_view, updated_wrapped_hand, hand_view.hand_scaling[0])
            hand_view.refresh_flag = True
        if (hand_view.hand_scaling[0] != UIC.scale and len(updated_wrapped_hand) <= hand_view.deal_size):
            hand_view.hand_scaling = (UIC.scale, UIC.Card_Spacing)
            updated_wrapped_hand = rescaleCards(hand_view, updated_wrapped_hand, hand_view.hand_scaling[0])
    return updated_wrapped_hand

def clearPreparedCardsInHandView(wrapped_hand):
    for element in wrapped_hand:
        if element.status == 2:
            element.status = 0
            element.img_clickable.changeOutline(0)
    return wrapped_hand

def preparedCardsPlayed(hand_view):
    if len(hand_view.controller.prepared_cards) == 0:
        # manually remove cards played, else an ambiguity in wrapped cards causes
        # picked up cards to sometimes get coordinates of cards just played.
        # If statement insures that you don't remove cards if pick-up failed.
        for wrappedcard in hand_view.hand_info:
            if wrappedcard.status == 2:
                hand_view.hand_info.remove(wrappedcard)
                hand_view.last_hand.remove(wrappedcard.card)
    return

def refreshXY(hand_view, original, layout_option=1):
    hand_view.refresh_flag = False
    """After sorting or melding, may wish to refresh card's xy coordinates """
    maxX = UIC.Disp_Width - (hand_view.hand_scaling[1] / 2)
    if not layout_option == 1:
        print('the only layout supported now is cards in a line, left to right')
    refreshed = []
    card_xy = (10, UIC.Table_Hand_Border + 40)
    for element in original:
        element.img_clickable.x = card_xy[0]
        element.img_clickable.y = card_xy[1]
        card_xy = (card_xy[0] + hand_view.hand_scaling[1], card_xy[1])
        refreshed.append(element)
    if (card_xy[0] > maxX):
        scalingfactor = maxX / card_xy[0]
        hand_view.hand_scaling = (scalingfactor * hand_view.hand_scaling[0], scalingfactor * hand_view.hand_scaling[1])
        refreshed = rescaleCards(refreshed, hand_view.hand_scaling[0], scalingfactor)
    return refreshed

def rescaleCards(hand_view, original, card_scaling):
    rescaled = []
    for element in original:
        loc_xy = (element.img_clickable.x, element.img_clickable.y)
        scaledelement = UICardWrapper(element.card, loc_xy, card_scaling)
        scaledelement.status = element.status
        scaledelement.img_clickable.outline_index = element.img_clickable.outline_index
        rescaled.append(scaledelement)
    hand_view.refresh_flag = True
    return rescaled

def showHolding(hand_view, wrapped_cards):
    wrapped_cards.sort(key=lambda wc: wc.img_clickable.x)
    for wrapped_element in wrapped_cards:
        color = UIC.outline_colors[wrapped_element.img_clickable.outline_index]
        loc_xy = (wrapped_element.img_clickable.x, wrapped_element.img_clickable.y)
        wrapped_element.img_clickable.draw(hand_view.display, loc_xy, color)
    return

def MouseHiLight(hand_view, pos):
    for element in hand_view.hand_info:
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

