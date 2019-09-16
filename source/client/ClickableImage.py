import pygame
import client.UIConstants as UIC


class ClickableImage:
    """This class draws an image which can be used as a button to initiate actions.

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
        display.blit(self.image, (self.x, self.y))

    def isOver(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False
