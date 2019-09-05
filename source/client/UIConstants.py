""" These are the constants for the UI

Defines sizing, colors, font, and constant strings
Has methods for importing and fetching images.
"""
import pygame
import os

# define colors (#rgb on scale of 0 to 255)
Black = (0,0,0) 
White = (255,255,255)
Red = (200,0,0)
Green = (90,200,90)
Blue = (0,0,200)
Bright_Red = (255,0,0)
Bright_Green = (0,255,0)
Bright_Blue = (0,0,255)

# Set dislays size
# (below good for my laptop, screen resolution: 3840x2160, display set to 300%)
# displayWidth = 300  # temporary value for use while we're only running handview,
Disp_Width = 1200
Disp_Height = 600
Hand_Col_Fraction = 0.3
Table_Hand_Border = Disp_Width * (1-Hand_Col_Fraction)

# fonts
pygame.font.init()
Small_Text = pygame.font.Font("freesansbold.ttf",14)
# Big_Text = pygame.font.Font("freesansbold.ttf",20)
Big_Font_Sz = 20
Big_Text = pygame.font.Font("freesansbold.ttf",Big_Font_Sz)
Text_Feed = int(Big_Font_Sz * 1.5)
Wrap_Width = int(Hand_Col_Fraction * Disp_Width / (Big_Font_Sz * 0.5))

# load image of back of card.
Back_Img = pygame.image.load(os.path.join('client', 'cardimages', 'cardBack.png'))

