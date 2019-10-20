import pygame
import textwrap
import client.UIConstants as UIC


class CreateDisplay:
    """Initialize Display

    Initialize display and other variables used by BOTH HandView and TableView.
    CreateDisplay.render does stuff common to BOTH HandView and TableView
    """
    def __init__(self, controller):
        self.controller = controller
        # initialize pygame modules
        pygame.init()
        # initialize variables
        self.notification = "Waiting for notification from game controller."
        # Set up user display.
        self.display = pygame.display.set_mode((UIC.Disp_Width, UIC.Disp_Height))
        pygame.display.set_caption(self.controller.getName() + " View")
        self.display.fill(UIC.White)
        # self.tableView = TableView(self.display)         # displays public info.
        # render starting window
        self.refresh()

    def refresh(self):
        """This refreshes the display """
        self.display.fill(UIC.White)

    def render(self, notification):
        """This updates the display

        latest views of hand and table are created in HandView and TableView,
         which are called just prior to this 'render'
         """
        self.notification = notification
        self.printText(self.notification, (5, UIC.Table_Hand_Border))
        pygame.display.update()

    def printText(self, text_string, start_xy):
        """print the text_string in a text box starting on the top left.

        This wraps the text_string, so it is all displayed.
        """
        word_list = textwrap.wrap(text=text_string, width=UIC.Wrap_Width)
        start_xy_wfeed = start_xy  # 'wfeed' -> "with line feed"
        for element in word_list:
            text = UIC.Big_Text.render(element, True, UIC.Blue, UIC.White)
            text_rect = text.get_rect()
            text_rect.topleft = start_xy_wfeed
            self.display.blit(text, text_rect)
            start_xy_wfeed = (start_xy_wfeed[0], start_xy_wfeed[1] + UIC.Text_Feed)
