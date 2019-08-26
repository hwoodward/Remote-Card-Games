""" These are the constants for the UI

Defines sizing, colors, font, and constant strings
Has methods for importing and fetching images.
"""
import pygame
from common.Card import Card
from client.HandView import cardAndImage

#TODO: finalized choices are in Upper_Case, unfinalized may be lowercase

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
displayWidth = 1200
displayHeight = 600
handColumnFraction = 0.3
publicPrivateBoundary = displayWidth * (1-handColumnFraction)


# fonts
pygame.font.init()
smallText = pygame.font.Font("freesansbold.ttf",14)
bigText = pygame.font.Font("freesansbold.ttf",20)
bigFontSz = 20
bigText = pygame.font.Font("freesansbold.ttf",bigFontSz)
text_feed = int(bigFontSz * 1.5)
Wrap_Width = int(handColumnFraction * displayWidth / (bigFontSz * 0.5))

# load image of back of card.
backImg = pygame.image.load('client\card_images\cardBack.png')


# Need card for testing.
# for simplicity make it 3C (0 points), then change image to
# backImg
facedown=Card(3,'Clubs')
card4guiTests = cardAndImage(facedown,(10,10),UIC.backImg)
card4guiTests._img = UIC.backImg


