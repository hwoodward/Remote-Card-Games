import pygame
import os
# Next two imports flagged by pyCharm, but may want them later.
# from common.Card import Card
import client.UIConstants as UIC
from client.ClickableImage import ClickableImage as ClickImg


class UICardWrapper:
    """GUI needs image and position of card. """

    def __init__(self, this_card, loc_xy):
        self.card = this_card
        self.img = UICardWrapper.getImage(self.card)
        self.img_clickable = ClickImg(self.img, loc_xy[0], loc_xy[1], self.img.get_width(), self.img.get_height(), 0)
        self.xy = loc_xy
        print(self.xy)
        self.selected = False
        self.key = UICardWrapper.sortKey(this_card)
        print(self.key)

    @staticmethod
    def getImage(card):
        """Helper to fetch correct image for a card"""
        suit_letter = 'N'  # this doesn't distinguish between red & black Jokers
        if card.suit is not None:
            suit_letter = card.suit[0]

        image_file = os.path.join('client', 'cardimages', 'card' + str(card.number) + suit_letter + '.png')
        img = pygame.image.load(image_file)
        img = pygame.transform.rotozoom(img, 0, UIC.scale)
        return img

    def sortKey(this_card, sort_option=1):
        """ Calculate score for sorting cards.

        Calculates value for sorting cards. Option 1 optimized  for Hand & Foot game.
        For Bridge or other games different sorting would probably be preferred, and
        could create multiple buttons so that user could sort it how they wanted.
        """
        if (sort_option == 1):
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
