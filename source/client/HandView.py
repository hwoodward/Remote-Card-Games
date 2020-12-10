import pygame
import textwrap
import client.Button as Btn
from client.ClickableImage import ClickableImage as ClickImg
from client.CreateDisplay import CreateDisplay
import client.LiverpoolButtons as RuleSetsButtons_LP
import client.HandAndFootButtons as RuleSetsButtons_HF
import client.HandManagement as HandManagement
from client.UICardWrapper import UICardWrapper
import client.UIConstants as UIC
from common.Card import Card


class HandView:
    """This class handles player's cards and enables actions.

    Actions are primarily performed using buttons, since these need to somewhat customized by game
    the buttons are in ***.py (*** is Liverpool or HandAndFoot) and are imported as RuleSetsButtons.
    Management of displaying the hand's cards is not game specific, and methods that help with that
    are in HandManagement.py.

    Player can arrange their own hand, and prepare to play cards during other players' turns.
    """
    def __init__(self, controller, display, ruleset):
        self.controller = controller
        self.display = display
        self.ruleset = ruleset
        self.Meld_Threshold = controller._state.rules.Meld_Threshold
        self.deal_size = controller._state.rules.Deal_Size
        self.help_text = controller._state.rules.help_text
        if ruleset == 'Liverpool':
            self.buttons_per_player = self.Meld_Threshold[0][0] +  self.Meld_Threshold[0][1]
            self.RuleSetsButtons = RuleSetsButtons_LP
        elif ruleset == 'HandAndFoot':
            self.RuleSetsButtons = RuleSetsButtons_HF
        self.hand_scaling = (UIC.scale, UIC.Card_Spacing)
        self.current_hand = []
        self.last_hand = []
        self.hand_info = []          # will contain UICardWrapped elements of current_hand
        self.prepared_cards = []     # will contain list of prepared cards from controller
        self.discards = []
        self.discard_confirm = False
        # num_wilds is HandAndFoot specific, only non-zero if by prepare_card_btn in HandAndFootButtons.py is triggered.
        self.num_wilds = 0
        self.wild_cards = []
        self.selected_list = []
        self.round_index = 0
        self.player_index = 0
        self.round_advance = False
        self.num_players = 1
        # In Liverpool and other Shared_Board games:  prepare cards buttons must be updated each round
        self.need_updated_buttons = True
        self.ready_color_idx = 2
        self.not_ready_color_idx = 6
        #
        # if someone joins between rounds, then they won't know the correct meld requirement until the round begins.
        # (self.controller._state.round = -1 until play commences).
        # In HandAndFoot: Correct meld requirement will be written in lower right corner once play commences.
        # In Liverpool: Will see correct buttons once round commences.
        self.RuleSetsButtons.CreateButtons(self)

    def update(self, player_index=0, num_players=1, visible_scards = []):
        """This updates the view of the hand, between rounds it displays a message. """

        self.visible_scards = visible_scards
        self.player_index = player_index
        self.num_players = num_players
        if self.controller._state.round == -1:
            self.mesgBetweenRounds(self.help_text)
            if self.round_advance:
                self.round_index = self.round_index + 1
                if self.round_index < len(self.Meld_Threshold):
                    self.help_text[0] = 'This is the round of ' + str(self.Meld_Threshold[self.round_index]) + ' ! '
                    self.need_updated_buttons = True  # used for Liverpool.
                else:
                    self.help_text = ['Game has concluded. Scores for each round can be found in command window.']
                self.round_advance = False
        else:
            if not self.round_index == self.controller._state.round:
                # Need this to true up round_index if a player joins mid-game.
                skipped_rounds =  self.controller._state.round - self.round_index
                for idx in range(skipped_rounds):
                    #todo:  How to score latecomers should be moved to ruleset.
                    score = 0
                    self.controller.lateJoinScores(score)
                self.round_index = self.controller._state.round
            self.round_advance = True
            # reset outline colors on ready buttons to what they need to be at the start of the "between rounds" state.
            self.ready_color_idx = 2
            self.not_ready_color_idx = 6
        self.last_hand = self.current_hand
        self.current_hand = self.controller.getHand()
        if len(self.current_hand) == 0:
            self.hand_info = []
        elif not self.last_hand == self.current_hand:
            self.hand_info = HandManagement.WrapHand(self, self.current_hand, self.hand_info)
        HandManagement.ShowHolding(self, self.hand_info)  # displays hand
        self.RuleSetsButtons.ButtonDisplay(self)

    def nextEventWildsOnBoard(self):
        """This runs instead of most of nextEvent when Shared_Board is True and there are ambiguous wild cards.

        It is looking for key strokes to designate ambiguous wild cards in runs.
        The mouse is ignored until you designate all the wilds (turn phase goes back to play)."""

        if self.controller._state.rules.Shared_Board and self.num_wilds > 0:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    # The window crashed, we should handle this
                    print("pygame crash, AAAHHH")
                    pygame.quit()
                    quit()
                else:
                    # in Shared_Board games, check if there are wilds that need to be updated.
                    # All other events are ignored until play is finished.
                    HandManagement.wildsHiLo_step2(self)

    def nextEvent(self):
        """This submits the next user input to the controller,

        In games with Shared_Board = False (e.g. HandAndFoot) key strokes don't do anything
        unless designating values for prepared wild cards, at which time the mouse is ignored
        unless you want to clear the prepared cards.
        In games with Shared_Board = True  wilds on board might change designation upon other cards being played.
        IF designation cannot be handled automatically (= if wild can be at the beginning or end of a run) then
        it must be designated before play is completed.
        This is done in nextEvenWildsOnBoard.  All other events are ignored until num_wilds == 0 OR play is canceled."""

        if self.controller._state.rules.Shared_Board:
            self.num_wilds = len(self.controller.unassigned_wilds_dict.keys())
            if self.num_wilds > 0:
                self.nextEventWildsOnBoard()

        for self.event in pygame.event.get():
            if self.event.type == pygame.QUIT:
                # The window crashed, we should handle this
                print("pygame crash, AAAHHH")
                pygame.quit()
                quit()

            if not self.controller._state.rules.Shared_Board and self.num_wilds > 0:
                wild_instructions = 'Use the keyboard to designate your prepared wild cards \r\n '
                wild_instructions = wild_instructions + '(use 0 for 10 and J, Q, or K for facecards).'
                self.controller.note = wild_instructions
            pos = pygame.mouse.get_pos()

            if self.event.type == pygame.MOUSEBUTTONDOWN:
                self.RuleSetsButtons.ClickedButton(self, pos)
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
                self.RuleSetsButtons.MouseHiLight(self, pos)
                HandManagement.MouseHiLight(self.hand_info, pos)
            elif self.event.type == pygame.KEYDOWN:
                if self.controller._state.rules.Buy_Option:
                    if self.controller.buying_opportunity:
                        if self.event.key == pygame.K_y:
                            self.controller.wantTopCard(True)
                        elif self.event.key == pygame.K_n:
                            self.controller.wantTopCard(False)
                if not self.controller._state.rules.Shared_Board and self.num_wilds > 0:
                    HandManagement.ManuallyAssign(self)


    def gatherSelected(self):
        """ gathers selected cards
        in order to take action on selected cards (either discarding them or preparing them)
        """
        self.selected_list = []
        for element in self.hand_info:
            if element.status == 1:
                self.selected_list.append(element)
        return self.selected_list

    def discardConfirmation(self, confirmed, wrapped_discards):
        """ Confirm a user is sure about a discard and then perform it once confirmed."""
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

    def mesgBetweenRounds(self, message):
        """print message where cards usually displayed until Ready button is clicked for next round."""
        font = UIC.Medium_Text
        y_offset = (UIC.Disp_Height * (1 - (UIC.Hand_Row_Fraction * 0.8)))
        for message_string in message:
            text_surface = font.render(message_string, True, UIC.Black)
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
