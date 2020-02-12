import pygame
import UIConstants as UIC


class Button():
    """This class draws an rectangle with internal text that can trigger actions
    when clicked on.

        Lightly edited code for class button found on-line at
        https://www.youtube.com/watch?v=4_9twnEduFA
        to create this.
        """
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.outline_color = UIC.no_outline_color

    def draw(self, win, outline=UIC.no_outline_color):
        #Call this method to draw the button on the screen
        if not outline == UIC.no_outline_color:
            pygame.draw.rect(win, outline,
                             (self.x-UIC.outline_width,
                              self.y-UIC.outline_width,
                              self.width+2*UIC.outline_width,
                              self.height+2*UIC.outline_width),
                             0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False