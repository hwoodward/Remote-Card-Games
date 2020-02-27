import pygame
import os
import client.UIConstants as UIC
from client.ClickableImage import ClickableImage as ClickImg


class UICardWrapper:
    """GUI needs image and position of card. """

    def __init__(self, this_card, loc_xy):
        self.card = this_card
        self.img = UICardWrapper.getImage(self.card)
        self.img_clickable = ClickImg(self.img, loc_xy[0], loc_xy[1], self.img.get_width(), self.img.get_height(), 0)
        self.status = 0     # 0 = not selected or prepared, 1 = selected, 2 = prepared (ready for play)
        self.key = UICardWrapper.sortKey(this_card)

    @staticmethod
    def getImage(card):
        """Helper to fetch correct image for a card"""
        suit_letter = 'N'  # this doesn't distinguish between red & black Jokers
        if card.suit is not None:
            suit_letter = card.suit[0]
        image_index = str(card.number) + suit_letter
        img = UIC.card_images[image_index]
        img = pygame.transform.rotozoom(img, 0, UIC.scale)
        return img

    def sortKey(this_card, sort_option=1):
        """ Calculate score for sorting cards.

        Calculates value for sorting cards. Option 1 optimized  for Hand & Foot game.
        For Bridge or other games different sorting would probably be preferred, and
        could create multiple buttons so that user could sort it how they wanted.
        """
        if sort_option == 1:
            key4sorting = this_card.number
            if key4sorting == 1:
                key4sorting = 14
            asuit = this_card.suit
            key4sorting = 2 * key4sorting
            if asuit == 'Hearts' or asuit == 'Diamonds':
                key4sorting = key4sorting - 1
        else:
            print('only 1 sorting option currently supported')
        return key4sorting