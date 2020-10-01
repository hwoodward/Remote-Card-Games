import pygame
import os
import client.UIConstants as UIC
from client.ClickableImage import ClickableImage as ClickImg


class UICardWrapper:
    """GUI needs image and position of card. """

    def __init__(self, this_card, loc_xy, card_scaling):
        self.card = this_card
        self.img = UICardWrapper.getImage(self.card, card_scaling)
        self.img_clickable = ClickImg(self.img, loc_xy[0], loc_xy[1], self.img.get_width(), self.img.get_height(), 0)
        self.status = 0     # 0 = not selected or prepared, 1 = selected, 2 = prepared (ready for play)
        self.key  = UICardWrapper.sortKey(this_card)
        self.key2 = UICardWrapper.sortKey(this_card, 2)
        self.key3 = UICardWrapper.sortKey(this_card, 3)
        self.key4 = UICardWrapper.sortKey(this_card, 4)
        # todo: consider making above a method instead of defining all keys in init...
        # pro - seems more elegant, con -- you sort the same card over and over, so above might be more efficient.

    @staticmethod
    def getImage(card, card_scaling):
        """Helper to fetch correct image for a card"""
        suit_letter = 'N'  # this doesn't distinguish between red & black Jokers
        if card.suit is not None:
            suit_letter = card.suit[0]
        image_index = str(card.number) + suit_letter
        img = UIC.card_images[image_index]
        img = pygame.transform.rotozoom(img, 0, card_scaling)
        return img

    def sortKey(this_card, sort_option=1):
        """ Calculate score for sorting cards.

        Calculates value for sorting cards. Option 1 optimized  for Hand & Foot game.
        For Bridge or other games different sorting would probably be preferred, and
        could create multiple buttons so that user could sort it how they wanted.
        """
        arank = this_card.number
        asuit = this_card.suit
        key4sorting = arank
        if sort_option == 1 or sort_option == 2:     # by number, aces high or low
            if sort_option == 1 and arank == 1:
                arank = 14                           # make aces high
            key4sorting = 4 * arank
            if asuit == 'Clubs':
                key4sorting = key4sorting - 3
            elif asuit == 'Diamonds':
                key4sorting = key4sorting - 2
            elif asuit == 'Spades':
                key4sorting = key4sorting - 1
        elif sort_option == 3 or sort_option == 4:    # by suit, aces high or low
            if sort_option == 3 and arank == 1:
                arank = 14
            if asuit == 'Clubs':
                key4sorting = arank
            if asuit == 'Diamonds':
                key4sorting = 15 + arank
            elif asuit == 'Spades':
                key4sorting = 30 + arank
            elif asuit == 'Hearts':
                key4sorting = 45 + arank
        else:
            print('only sorting option currently supported are 1 to 4')
        return key4sorting