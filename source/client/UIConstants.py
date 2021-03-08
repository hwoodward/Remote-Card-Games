""" These are the constants for the UI

Defines sizing, colors, font, and constant strings
Has methods for importing and fetching images.
"""
import pygame
import os
from common.Card import Card

# define colors (#rgb on scale of 0 to 255)
Black = (0,0,0)
Gray = (100,100,100)
White = (255,255,255)
Red = (200,0,0)
Green = (90,200,90)
Yellow = (255,255,0)
Orange = (225,130,0)
Bright_Orange = (255,200,0)
Bright_Yellow = (255,255,100)
Blue = (0,0,200)
Bright_Red = (255,0,0)
Bright_Green = (0,255,0)
Bright_Blue = (100,100,255)

# Set display size
# (below good for my laptop, screen resolution: 3840x2160, display set to 300%)
Disp_Width = 1200
Disp_Height = 600
Hand_Row_Fraction = 0.3
Hand_Col_Fraction = 1.0
Table_Hand_Border = Disp_Height * (1 - Hand_Row_Fraction)

# fonts
pygame.font.init()
# Font_File = os.path.join('bundle_data', 'freesansbold.ttf')  << does not include card suit symbols.
Font_File = os.path.join('bundle_data', 'FreeSans-LrmZ.ttf')
Small_Font_Sz = 14
Small_Text = pygame.font.Font(Font_File, Small_Font_Sz)
Small_Text_Feed = int(14* 1.3)
Medium_Text = pygame.font.Font(Font_File, 16)
Medium_Text_Feed = int(16* 1.3)
Big_Font_Sz = 20
Big_Text = pygame.font.Font(Font_File, Big_Font_Sz)
Text_Feed = int(Big_Font_Sz * 1.5)
Wrap_Width = int(Hand_Col_Fraction * Disp_Width / (Big_Font_Sz * 0.5))
table_grid_colors = ((180,199,231),(255,242,204),(197,224,180),(255,197,216),(192,192,192),(248,203,173))

# card display
scale = 0.7
Card_Spacing = 70 * scale
outline_width = 8 * scale
no_outline_color = (-1, -1, -1)  # flags there is no outline.
outline_colors = (no_outline_color, Yellow, Green, Bright_Green, Bright_Blue, Bright_Blue, Gray, Gray, Red, Bright_Red)
'''
No_outline_color indicates clickable image (usually a card) not selected or prepared.
Yellow indicates not selected, but mouse is over clickable image.
green elements indicate card is 'selected'
bright green indicates mouse is over card,
blue indicates card is prepared (for play).
Since cannot change prepared cards status with mouse, don't highlight those cards when mouse is over them...
'''
# load image of back of card, and scale it.
Back_Img = pygame.image.load(os.path.join('bundle_data', 'cardimages', 'cardBack.png'))
Back_Img = pygame.transform.rotozoom(Back_Img, 0, scale)

# Load images for full deck of cards:
suit_letter = 'N'  # this doesn't distinguish between red & black Jokers
temp_deck = Card.getStandardDeck(0)
card_images = {}
card_images['0N'] = pygame.image.load(os.path.join('bundle_data', 'cardimages', 'card0N.png'))
for card in temp_deck:
    suit_letter = card.suit[0]
    image_index = str(card.number) + suit_letter
    card_string = 'card' + image_index
    image_file = os.path.join('bundle_data', 'cardimages', card_string + '.png')
    card_images[image_index] = pygame.image.load(image_file)

