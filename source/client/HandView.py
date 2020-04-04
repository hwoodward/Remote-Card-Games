import pygame
import textwrap
import client.Button as Btn
from client.ClickableImage import ClickableImage as ClickImg
from client.CreateDisplay import CreateDisplay
import client.HandAndFootButtons as HandAndFootButtons
import client.HandManagement as HandManagement
from client.UICardWrapper import UICardWrapper
import client.UIConstants as UIC
from common.Card import Card
from common.HandAndFoot import Deal_Size
from common.HandAndFoot import Meld_Threshold


class HandView:
    """This class handles player's cards and enables actions.

    Actions are primarily performed using buttons, since these need to somewhat customized by game
    the buttons are in HandAndFootButtons.py (it is Hand And Foot Specific).
    Management of displaying the hand's cards is not game specific, and methods that help with that
    are in HandManagement.py

    Player can arrange their own hand, and prepare to play cards during other players' turns.
    """
    def __init__(self, controller, display):
        self.controller = controller
        self.display = display
        self.deal_size = Deal_Size
        self.hand_scaling = (UIC.scale, UIC.Card_Spacing)
        self.refresh_flag = False
        self.current_hand = []
        self.last_hand = []
        self.hand_info = []          # will contain UICardWrapped elements of current_hand
        self.prepared_cards = []     # will contain list of prepared cards from controller
        self.discards = []
        self.discard_confirm = False
        self.num_wilds = 0
        self.wild_cards = []
        self.selected_list = []
        self.round_index = 0
        self.round_advance = False
        self.round_meld = Meld_Threshold  # [50,90,120,150]
        self.ready_color_idx = 2
        self.not_ready_color_idx = 6
        # --- Hand And Foot Specific:
        self.betweenrounds = ['Welcome to a new game.  This is the round of ' + str(Meld_Threshold[0]) + '.',
                              'To draw click on the deck of cards (upper left).',
                              'To discard select ONE card & double click on discard button. ',
                              'To pick up pile PREPARE necessary cards & then click on discard pile. ',
                              "Cumulative score will display beneath player's cards",
                              'When ready to start playing click on the YES button on the lower right.']
        self.draw_pile = ClickImg(UIC.Back_Img, 10, 25, UIC.Back_Img.get_width(), UIC.Back_Img.get_height(), 0)
        # discard info
        discard_info = self.controller.getDiscardInfo()
        self.top_discard = discard_info[0]  
        self.pickup_pile_sz = discard_info[1]
        if self.pickup_pile_sz > 0:
            self.top_discard_wrapped = UICardWrapper(self.top_discard, (100, 25), UIC.scale)
            self.pickup_pile = self.top_discard_wrapped.img_clickable
            self.labelMedium(str(self.pickup_pile_sz), 150, 35)
        HandAndFootButtons.CreateButtons(self)

    def update(self):
        """This updates the view of the hand, between rounds it displays a message. """

        if self.controller._state.round == -1:
            self.mesgBetweenRounds(self.betweenrounds)
            if self.round_advance:
                self.round_index = self.round_index + 1
                if self.round_index < len(self.round_meld):
                    self.betweenrounds[0] = 'This is the round of ' + str(self.round_meld[self.round_index]) + ' ! '
                else:
                    self.betweenrounds = 'Game has concluded.         ', \
                                    'Score can be found in command window.'
                    # todo: Create better display for final results.
                self.round_advance = False
        else:
            self.round_advance = True
            # reset colors to what they need to be at the start of the "between rounds" state.
            self.ready_color_idx = 2
            self.not_ready_color_idx = 6
        self.last_hand = self.current_hand
        self.current_hand = self.controller.getHand()
        if len(self.current_hand) == 0:
            self.hand_info = []
        elif not self.last_hand == self.current_hand:
            self.hand_info = HandManagement.wrapHand(self, self.current_hand, self.hand_info)
        HandManagement.showHolding(self, self.hand_info)  # displays hand
        if self.refresh_flag:  # if needed to rescale card size, then refreshXY again.
            self.hand_info = HandManagement.refreshXY(self, self.hand_info)
        HandAndFootButtons.ButtonDisplay(self)

    def nextEvent(self):
        """This submits the next user input to the controller,

        key strokes don't do anything unless designating values for prepared wild cards,
        at which time the mouse is ignored unless you want to clear the prepared cards."""

        for self.event in pygame.event.get():
            if self.num_wilds > 0:
                wild_instructions = 'Use the keyboard to designate your prepared wild cards \r\n '
                wild_instructions = wild_instructions + '(use 0 for 10 and J, Q, or K for facecards).'
                self.controller.note = wild_instructions
            pos = pygame.mouse.get_pos()

            if self.event.type == pygame.QUIT:
                # The window crashed, we should handle this
                print("pygame crash, AAAHHH")
                pygame.quit()
                quit()

            if self.event.type == pygame.MOUSEBUTTONDOWN:
                HandAndFootButtons.ClickedButton(self, pos)
                # ---  make below a generic helper function 'CardSelection' ----
                for element in self.hand_info:
                    # cannot select prepared cards, so not included in logic below.
                    if element.img_clickable.isOver(pos):
                        if element.status == 1:
                            element.status = 0
                            element.img_clickable.changeOutline(0)
                        elif element.status == 0:
                            element.status = 1
                            element.img_clickable.changeOutline(2)

            elif self.event.type == pygame.MOUSEMOTION:
                HandAndFootButtons.MouseHiLight(self, pos)
                # next section should go in card highlighting function -- generic, not HandAndFoot specific.
                for element in self.hand_info:
                    color_index = element.img_clickable.outline_index
                    if element.img_clickable.isOver(pos):
                        # Brighten colors that mouse is over.
                        # Odd colors are bright, even show status.
                        if (color_index % 2) == 0:
                            color_index = element.img_clickable.outline_index + 1
                            element.img_clickable.changeOutline(color_index)
                    else:
                        color_index = element.img_clickable.outline_index
                        if (color_index % 2) == 1:
                            color_index = color_index - 1
                            element.img_clickable.changeOutline(color_index)
            # This next section has player enter desired values for wild cards.
            elif self.event.type == pygame.KEYDOWN and self.num_wilds > 0:
                self.assignWilds()

    def assignWilds(self):
        textnote = "Designate one of " + str(self.num_wilds) + "  wildcard(s)"
        textnote = textnote + " enter value by typing:  1-9, 0 (for ten), j, q, k or a. "
        acceptable_keys = self.wild_cards[0][1]
        self.controller.note = textnote
        this_wild = self.wild_cards[0][0]
        if self.event.key == pygame.K_a:
            wild_key = 1
        elif self.event.key == pygame.K_0:
            wild_key = 10
        elif self.event.key == pygame.K_j:
            wild_key = 11
        elif self.event.key == pygame.K_q:
            wild_key = 12
        elif self.event.key == pygame.K_k:
            wild_key = 13
        elif self.event.unicode in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            wild_key = int(self.event.unicode)
        else:
            self.controller.note = 'invalid key:' + textnote
            wild_key = 666
        if wild_key in acceptable_keys:
            self.controller.note = str(this_wild) + ' will be a ' + str(wild_key)
            icount = 0
            for wrappedcard in self.wrapped_cards_to_prep:
                if wrappedcard.card == this_wild and icount == 0 and wrappedcard.status == 1:
                    icount = 1
                    wrappedcard.status = 2
                    wrappedcard.img_clickable.changeOutline(4)
            self.controller.prepareCard(wild_key, this_wild)
            if self.num_wilds > 0:
                self.wild_cards = self.wild_cards[1:]
            self.num_wilds = len(self.wild_cards)

    def gatherSelected(self):
        # in order to take action on selected cards (either discarding them or preparing them) this method gathers them.
        self.selected_list = []
        for element in self.hand_info:
            if element.status == 1:
                self.selected_list.append(element)
        return self.selected_list

    def discardConfirmation(self, confirmed, wrapped_discards):
        # Confirm a user is sure about a discard and then perform it once confirmed.
        discards = []
        for element in wrapped_discards:
            discards.append(element.card)
        if self.discards != discards:
            confirmed = False
            self.discards = discards
        if not confirmed:
            self.controller.note = "Please confirm - discard  " + "{0}".format(self.discards)
            return True  # ask for confirmation
        else:
            # confirmed is True, performing discard and removing discarded wrapped cards from hand_info.
            if self.discard_confirm:
                controller_response = self.controller.discard(self.discards)
                if controller_response:
                    for element in wrapped_discards:
                        self.hand_info.remove(element)
            return False  # now that this is done, we don't have anything waiting on confirmation

    def mesgBetweenRounds(self, results):
        # print results where cards usually go until Ready button is clicked for next round.
        font = UIC.Medium_Text
        y_offset = (UIC.Disp_Height * (1 - (UIC.Hand_Row_Fraction * 0.8)))
        for result_string in results:
            text_surface = font.render(result_string, True, UIC.Black)
            text_rect = text_surface.get_rect()
            text_rect.center = ((UIC.Disp_Width * 0.5),  y_offset)
            y_offset = y_offset + UIC.Medium_Text_Feed
            self.display.blit(text_surface, text_rect)

    def labelMedium(self, labelstr, x_offset, y_offset):
        font = UIC.Medium_Text
        text_surface = font.render(labelstr, True, UIC.Bright_Blue)
        text_rect = text_surface.get_rect()
        text_rect.center = (x_offset, y_offset)
        self.display.blit(text_surface, text_rect)
