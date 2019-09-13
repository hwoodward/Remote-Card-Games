import pygame
# import client.UIConstants as UIC
# import UIConstants as UIC < running test case from client directory...

# TODO:
# (i) scale images,
# (ii) set width/height = dimensions of scaled images
# (iii) put border around images and have them change color when clicked on.
# (iv) Currently stand alone -- remove test code, integrate with HandView and UIConstants.

# (ivb) Make certain this is style compliant.
# (v)  Make clicking on card back image (=draw-pile) replace pressing 9 as event.
# (vi) Have clicking on other cards toggle whether they are selected or not.
# (vii) Create button to play selected cards
# (viii) Consult on how we want to initiate picking-up the pile (have to select cards to meld to do it).

pygame.init()

# load image of back of card -- this is in UIConstants.
Back_Img = pygame.image.load('cardimages/cardBack.png')

display = pygame.display.set_mode((1200,600))
display.fill((255,255,255))

# class button():
class ClickableImage:
    """This class draws an image which can be used as a button (e.g. to initiate actions).

    Edited code for class button found on-line at
    https://www.youtube.com/watch?v=4_9twnEduFA
    to create this.
    """
    def __init__(self, image, x, y, width, height, text=''):
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.outlineColor = (0,255,0)

    def draw(self, display, outline=None):
        # Call this method to draw the ClickableImage on the screen,
        # TODO currently outline is 2 pixels wide - move that to UIConstants.
        if outline:
            pygame.draw.rect(display, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        # pygame.draw.rect(display, (40,40,40), (self.x, self.y, self.width, self.height), 0)
        # display.blit(self.image, self.x, self.y)
        display.blit(self.image, (self.x,self.y))

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            display.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def redrawWindow():
    """ this section is to test code above - remove later"""
    display.fill((255,255,255))
    # greenButton.draw(display, (0,0.,0))  < Later can put outline around image.
    greenButton.draw(display)
run = True
greenButton = ClickableImage(Back_Img, 155, 255, 250, 100,'Click Me:)')
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
            if greenButton.isOver(pos):
                print('clicked the button')

        if event.type == pygame.MOUSEMOTION:
            if greenButton.isOver(pos):
                greenButton.color = (255,0,0)
            else:
                greenButton.color = (0,255,0)
