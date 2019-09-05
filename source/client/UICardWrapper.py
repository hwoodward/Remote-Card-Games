import pygame
import os
from common.Card import Card
import client.UIConstants as UIC

class UICardWrapper():     
    """GUI needs image and position of card. """

    def __init__(self, this_card, loc_xy):
        self.card = this_card
        self.img = UICardWrapper.getImage(self.card)
        self.xy = loc_xy
        self.selected = False

    def getImage(card):
        """Helper to fetch correct image for a card"""
        suit_letter = 'N' # this doesn't distinguish between red & black Jokers
        if(card.suit is not None):
            suit_letter = card.suit[0]

        image_file = os.path.join('client','cardimages','card' + str(card.number) + suit_letter + '.png')
        img = pygame.image.load(image_file)
        return(img)
