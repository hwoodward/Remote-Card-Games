import pygame
import client.UIConstants as UIC


class ClickableImage:
    """This class draws an image which can be used as a button to initiate actions.

    Edited code for class button found on-line at
    https://www.youtube.com/watch?v=4_9twnEduFA
    to create this.
    """
    def __init__(self, image, x, y, width, height, outline_index):
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outline_index = outline_index
        self.outline_color = UIC.outline_colors[outline_index]

    def draw(self, display, loc_xy, outline_choice):
        # Call this method to draw the ClickableImage on the screen
        if not outline_choice[0] == -1:
            pygame.draw.rect(display, outline_choice,
                             (self.x - UIC.outline_width, self.y - UIC.outline_width,
                              self.width + 2 * UIC.outline_width, self.height + 2 * UIC.outline_width), 0)
        self.x = loc_xy[0]
        self.y = loc_xy[1]
        display.blit(self.image, (self.x, self.y))

    def changeOutline(self, outline_idx):
        self.outline_index = outline_idx
        self.outline_color = UIC.outline_colors[outline_idx]

    def isOver(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
