import pygame
from common.Card import Card
import client.UIConstants as UIC

class UICardWrapper():     
    """GUI needs image and position of card. """

    def __init__(self, this_card, loc_xy, img):
\        self._card = this_card
        self._img = UICardWrapper.get_image(self._card)
        self._xy = loc_xy
        self._selected = False
    def get_image(one_card):
        temp = one_card._suit
        if(temp is not None):
            temp = temp[0] # this doesn't distinguish between red & black Jokers
        else:
            temp = 'N'
        image_file_name='client\cardimages\card'+str(one_card._number)+ temp + '.png'
        img = pygame.image.load(image_file_name)
        return(img)
