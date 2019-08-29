import pygame
from common.Card import Card
import client.UIConstants as UIC

class UICardWrapper():     
        """GUI needs image and position of card.  Do this when card is drawn.
        Do NOT re-wrap card in render loop -- that will reset "selected" status
        and reload image file.
        """

        def __init__(self, thiscard, loc_xy, img):
                # should we check that card is in deck?
                self._card = thiscard
                self._img = UICardWrapper.get_image(self._card)
                self._xy = loc_xy
                self._selected = False
        def get_image(onecard):
                temp = onecard._suit
                if(temp is not None):
                        temp = temp[0]
                else:
                        temp = 'N'
                imageFileName='client\card_images\card'+str(onecard._number)+ temp + '.png'
                print(imageFileName)
                img = pygame.image.load(imageFileName)
                return(img)
