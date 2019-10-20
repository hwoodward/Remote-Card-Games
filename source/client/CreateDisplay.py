import pygame
import textwrap
import client.UIConstants as UIC
# from client.UICardWrapper import UICardWrapper
# from client.ClickableImage import ClickableImage as ClickImg
# import client.Button as Btn
# import client.TableView as TableView
# from common.Card import Card
# from PodSixNet.Connection import connection, ConnectionListener


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
        self.notification = "Notification in CreateDisplay."
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

    def render(self):
        """This updates the display

        latest views of hand and table are created in HandView and TableView,
         which are called just prior to this 'render'
         """
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

    def discardLogic(self):
        if self.discard_confirm == 1:
            self.discards = []
            for element in self.hand_info:
                if element.selected:
                    self.discards.append(element.card)
            if self.discards == self.discards_confirm:
                self.controller.discard(self.discards)
                note = "It's someone's turn. "
            else:
                note = "Discard selection changed, discard canceled. "
            self.discard_confirm = 0
            self.discards = []
        else:
            self.discards = []
            if len(self.current_hand) == 0:
                print('Program currently crashes if Zaephod and hit discard')
                self.controller.discard(self.discards)
                note = "Zaephod - no discard required, turn is over"
            else:
                for element in self.hand_info:
                    if element.selected:
                        self.discards.append(element.card)
                if len(self.discards) == 1:
                    note = "Please confirm - discard  " + "{0}".format(self.discards)
                    self.discards_confirm = self.discards
                    self.discard_confirm = 1  # ask for confirmation
                else:
                    note = "Precisely one card must be selected to discard. "
        return note



