import pygame
# import client.UIConstants as UIC
# import UIConstants as UIC < running test case from client directory...

# TODO:
#  done (i) scale images,
#  done (ii) get width & height = dimensions of scaled images
#  done (iii) put border around images and have them change color when clicked on.
# (iv) Currently stand alone -- remove test code, integrate with HandView and UIConstants.

# (ivb) Make certain this is style compliant.
# (v)  Make clicking on card back image (=draw-pile) replace pressing 9 as event.
# (vi) Have clicking on other cards toggle whether they are selected or not.
# (vii) Create button to play selected cards
# (viii) Consult on how we want to initiate picking-up the pile (have to select cards to meld to do it).

pygame.init()

# load image of back of card -- this is in UIConstants.
Back_Img = pygame.image.load('cardimages/cardBack.png')

# Temporary notes for SLW:
# To set new width and height to be (50, 30).
# Back_Img = pygame.transform.scale(IMAGE, (50, 30))
# to rotate by 0 degrees, and multiply size by scale.
scale=0.5
Back_Img = pygame.transform.rotozoom(Back_Img, 0, scale)
no_outline_color = (-1, -1, -1)
isOver_outline_color = (255,255,0)
isClicked_outline_color = (255,0,0)

display = pygame.display.set_mode((1200,600))
display.fill((255,255,255))
outline_color = no_outline_color

# class button():
class ClickableImage:
    """This class draws an image which can be used as a button (e.g. to initiate actions).

    Edited code for class button found on-line at
    https://www.youtube.com/watch?v=4_9twnEduFA
    to create this.
    """
    def __init__(self, image, x, y, width, height, outline_color):
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outline_color = outline_color

    def draw(self, display, outline_color):
        # Call this method to draw the ClickableImage on the screen,
        # TODO currently outline is 6 pixels wide - move that to UIConstants.
        if not outline_color[0] == -1:
            pygame.draw.rect(display, outline_color, (self.x - 6, self.y - 6, self.width + 12, self.height + 12), 0)
        display.blit(self.image, (self.x,self.y))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def redrawWindow():
    """ this section is to test code above - remove later"""
    display.fill((255,255,255))
    drawPile.draw(display,outline_color)
    # drawPile.draw(display)  < no outline on image
run = True
drawPile = ClickableImage(Back_Img, 10, 255, Back_Img.get_width(), Back_Img.get_height(), outline_color)
while run:
    redrawWindow()
    pygame.display.update()

    for event in pygame.event.get():
        pos=pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if drawPile.isOver(pos):
                outline_color = isClicked_outline_color
                print('clicked the draw pile ! ')

        if event.type == pygame.MOUSEMOTION:
            if drawPile.isOver(pos):
                outline_color = isOver_outline_color
            else:
                outline_color = no_outline_color
