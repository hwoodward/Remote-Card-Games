import pygame
import client.Button as Btn
import client.UIConstants as UIC
from client.UICardWrapper import UICardWrapper

"""This file contains methods used in displaying the hand, should be useful for many different games"""


def wrapHand(self, updated_hand, wrapped_hand):
    """Associate each card in updated_hand with a UICardWrapper

    if change is that new cards were added, then want to preserve location and status for cards that were
    already in hand.
    If cards were played, then the wrapped cards that are removed should to those cards with status = 2
    (prepared cards).
    Note that discards are removed immediately after controller confirms discard legal.
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
                card_xy = (card_xy[0] + self.hand_scaling[1], card_xy[1])
                card_wrapped = UICardWrapper(card, card_xy, self.hand_scaling[0])
            updated_wrapped_hand.append(card_wrapped)
        maxX = UIC.Disp_Width - (self.hand_scaling[1] / 2)
        if (card_xy[0] > maxX):
            scalingfactor = maxX / card_xy[0]
            self.hand_scaling = (scalingfactor * self.hand_scaling[0], scalingfactor * self.hand_scaling[1])
            updated_wrapped_hand = rescaleCards(self, updated_wrapped_hand, self.hand_scaling[0])
            self.refresh_flag = True
        if (self.hand_scaling[0] != UIC.scale and len(updated_wrapped_hand) <= self.deal_size):
            self.hand_scaling = (UIC.scale, UIC.Card_Spacing)
            updated_wrapped_hand = rescaleCards(self, updated_wrapped_hand, self.hand_scaling[0])
        return updated_wrapped_hand

def clearPreparedCardsGui(self):
    for element in self.hand_info:
        if element.status == 2:
            element.status = 0
            element.img_clickable.changeOutline(0)

def refreshXY(self, original, layout_option=1):
    self.refresh_flag = False
    """After sorting or melding, may wish to refresh card's xy coordinates """
    maxX = UIC.Disp_Width - (self.hand_scaling[1] / 2)
    if not layout_option == 1:
        print('the only layout supported now is cards in a line, left to right')
    refreshed = []
    card_xy = (10, UIC.Table_Hand_Border + 40)
    for element in original:
        element.img_clickable.x = card_xy[0]
        element.img_clickable.y = card_xy[1]
        card_xy = (card_xy[0] + self.hand_scaling[1], card_xy[1])
        refreshed.append(element)
    if (card_xy[0] > maxX):
        scalingfactor = maxX / card_xy[0]
        self.hand_scaling = (scalingfactor * self.hand_scaling[0], scalingfactor * self.hand_scaling[1])
        refreshed = rescaleCards(refreshed, self.hand_scaling[0])
    return refreshed

def rescaleCards(self, original, card_scaling):
    rescaled = []
    for element in original:
        loc_xy = (element.img_clickable.x, element.img_clickable.y)
        scaledelement = UICardWrapper(element.card, loc_xy, card_scaling)
        scaledelement.status = element.status
        scaledelement.img_clickable.outline_index = element.img_clickable.outline_index
        rescaled.append(scaledelement)
    self.refresh_flag = True
    return rescaled

def showHolding(self, wrapped_cards):
    wrapped_cards.sort(key=lambda wc: wc.img_clickable.x)
    for wrapped_element in wrapped_cards:
        color = UIC.outline_colors[wrapped_element.img_clickable.outline_index]
        loc_xy = (wrapped_element.img_clickable.x, wrapped_element.img_clickable.y)
        wrapped_element.img_clickable.draw(self.display, loc_xy, color)


