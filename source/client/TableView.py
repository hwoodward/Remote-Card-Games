import pygame
import textwrap
from PodSixNet.Connection import connection, ConnectionListener
import client.UIConstants as UIC
from common.Card import Card


class TableView(ConnectionListener):
    """This class handles letting players actualy input information

    It handles the entire turn cycle
    """

    def __init__(self, display):
        """This currently does nothing"""
        # TODO: set up any member variables here
        self.display = display
        self.compressed_info = {}
        self.notification = "Beginning game, it is someone's turn"
        # TODO: replace example values with data from server.
        # TODO:  currently have wrong format for visible_cards both here and in compressSets method.
        self.visible_cards = (('Ted', {1: ((1, 'Hearts'), (1, 'Hearts'), (1, 'Spades'), (0, 'None')),
                                       4: ((4, 'Diamonds'), (4, 'Clubs'), (4, 'Clubs')),
                                       13: ((13, 'Hearts'), (13, 'Hearts'), (2, 'Hearts'))}),
                              ('Sheri', {}),
                              ('Helen', {}),
                              ('Miriam', {}))
        self.hand_stats = [('Ted', [12, True]), ('Sheri', [20, False]), ('Helen', [10, False]),
                           ('Miriam', [15, False])]
        print(self.visible_cards)
        print(self.hand_stats)
        self.playerByPlayer()

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_publicInfo(self, data):
        print("Recieved an update about cards on the table")
        # TODO either:
        # a) copy the data to the internal save you are keeping and
        #    i) rerender immediately
        #    ii) rerender when explicitly told to
        # b) call Render with the provided data and only ever rerender on new broadcast

    def playerByPlayer(self):
        self.compressSets(self.visible_cards)
        num_players = len(self.hand_stats)
        # currently set-up with one player per column. May need to change that for more players.
        players_sp_w = UIC.Disp_Width / num_players
        players_sp_top = UIC.Disp_Height / 5
        players_sp_h = UIC.Disp_Height / 2
        color_index = 0
        bk_grd_rect = (0, players_sp_top, players_sp_w, players_sp_h)
        for card_holder in self.hand_stats:
            # plan to move below to a helper function...
            player_name = card_holder[0]
            melded_summary = self.compressed_info[player_name]
            pygame.draw.rect(self.display, UIC.table_grid_colors[color_index], bk_grd_rect, 0)
            player_text = player_name + '\n'
            # TODO: get carriage return working
            for key in melded_summary:
                player_text = player_text + ' ' + str(key) + ': ' + str(melded_summary[key]) + '\n'
            text_surface, text_rect = self.textObjects(player_text, UIC.Small_Text)
            text_rect.center = ((bk_grd_rect[0] + 0.5 * players_sp_w), (bk_grd_rect[1] + 0.05 * UIC.Disp_Height))
            self.display.blit(text_surface, text_rect)
            # Move to next players rectangle and color:
            bk_grd_rect = (bk_grd_rect[0] + players_sp_w, bk_grd_rect[1], bk_grd_rect[2], bk_grd_rect[3])
            color_index = (color_index + 1) % len(UIC.table_grid_colors)

    def compressSets(self, v_cards):
        """ Don't have space to display every card. Summarize sets here. """

        self.compressed_info = {}
        for element in v_cards:
            summary = {}
            key_player = element[0]
            melded = dict(element[1])
            for key in melded:
                set = melded[key]
                length_set = len(set)
                wild_count = 0
                for s_card in set:
                    # Need to change below to: if s_card.number == 0 or s_card.number == 2:
                    if s_card[0] == 0 or s_card[0] == 2:
                        wild_count = wild_count + 1
                summary[key] = (length_set, wild_count)
            self.compressed_info[key_player] = summary

    def textObjects(self, text, font):
        text_surface = font.render(text, True, UIC.Black)
        return text_surface, text_surface.get_rect()
