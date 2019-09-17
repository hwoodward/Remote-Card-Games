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
Yellow = (255,255,0)
Blue = (0,0,200)
Bright_Red = (255,0,0)
Bright_Green = (0,255,0)
Bright_Blue = (0,0,255)

# Set display size
# (below good for my laptop, screen resolution: 3840x2160, display set to 300%)
Disp_Width = 1200
Disp_Height = 600
Hand_Col_Fraction = 0.3
Table_Hand_Border = Disp_Width * (1 - Hand_Col_Fraction)

# fonts
pygame.font.init()
Small_Text = pygame.font.Font("freesansbold.ttf", 14)
# Big_Text = pygame.font.Font("freesansbold.ttf",20)
Big_Font_Sz = 20
Big_Text = pygame.font.Font("freesansbold.ttf", Big_Font_Sz)
Text_Feed = int(Big_Font_Sz * 1.5)
Wrap_Width = int(Hand_Col_Fraction * Disp_Width / (Big_Font_Sz * 0.5))

# card display
scale = 0.7
outline_width = 6
no_outline_color = (-1, -1, -1)  # flags there is no outline.
outline_colors=(no_outline_color, Yellow, Green, Bright_Green, Red, Bright_Red)
# even elements show status, odd elements indicate same status, but mouse is over
# clickable image.
vertical_offset = 30  # used to further flag selected cards.

# load image of back of card, and scale it.
Back_Img = pygame.image.load(os.path.join('client', 'cardimages', 'cardBack.png'))
Back_Img = pygame.transform.rotozoom(Back_Img, 0, scale)
# Temporary notes for SLW:
# To set new width and height to be (50, 30).
# Back_Img = pygame.transform.scale(IMAGE, (50, 30))
# to rotate by 0 degrees, and multiply size by scale.
# Back_Img = pygame.transform.rotozoom(Back_Img, 0, UIC.scale)
