import pygame
import os
# Next two imports flagged by pyCharm, but may want them later.
# from common.Card import Card
import client.UIConstants as UIC
import client.ClickableImage as Cli


class UICardWrapper:
    """GUI needs image and position of card. """

    def __init__(self, this_card, loc_xy):
        self.card = this_card
        self.img = UICardWrapper.getImage(self.card)
        self.img_clickable = Cli.ClickableImage \
            (self.img, loc_xy[0], loc_xy[1], self.img.get_width(), self.img.get_height(), 0)
        self.xy = loc_xy
        self.selected = False
        self.outline_indx = self.img_clickable.outline_index


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
