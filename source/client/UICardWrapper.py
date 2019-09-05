import pygame
import os

from common.Card import Card
import client.UIConstants as UIC

class UICardWrapper():     
    """GUI needs image and position of card.

    Do this when card is drawn.
    Do NOT re-wrap card in render loop -- that will reset "selected" status
    and reload image file.
    """

    def __init__(self, this_card, loc_xy, img):
        # should we check that card is in deck?
        self._card = this_card
        self._img = UICardWrapper.getImage(self._card)
        self._xy = loc_xy
        self._selected = False

    def getImage(card):
        """Helper to fetch correct image for a card"""
        suit_letter = 'N' # this doesn't distinguish between red & black Jokers
        if(card.suit is not None):
            suit_letter = card.suit[0]

        image_file = os.path.join('client','cardimages','card' + str(card.number) + suit_letter + '.png')
        img = pygame.image.load(image_file)
        return(img)
