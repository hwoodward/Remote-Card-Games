import pygame
import textwrap
from PodSixNet.Connection import connection, ConnectionListener
import client.UIConstants as UIC
from common.Card import Card

class TableView(ConnectionListener):
    """ This displays publicly available info on all the players.
    """

    def __init__(self, display):
        self.display = display
        self.player_names = []
        self.visible_cards = []
        self.hand_status = []
        self.compressed_info = {}
        self.playerByPlayer()

    def playerByPlayer(self):
        self.compressSets(self.visible_cards)
        num_players = len(self.player_names)
        # currently set-up with one player per column. May need to change that for more players.
        if num_players > 1:
            players_sp_w = UIC.Disp_Width / num_players
        else:
            players_sp_w = UIC.Disp_Width
        players_sp_top = UIC.Disp_Height / 5
        players_sp_h = UIC.Disp_Height / 2
        color_index = 0
        bk_grd_rect = (0, players_sp_top, players_sp_w, players_sp_h)
        for idx in range(len(self.hand_status)):
            player_name = self.player_names[idx]
            # plan to move below to a helper function...
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
        for idx in range(len(v_cards)):
            summary = {}
            key_player = self.player_names[idx]
            melded = dict(v_cards[idx])
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

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_publicInfo(self, data):

        #Todo update example below.  False should be a play state, not True/False
        '''
        example of data (json structure) with two players, 'hhh' and 'sss' : 
        {'action': 'publicInfo', 'player_names': ['hhh', 'sss'], 'visible_cards': [{}, {}], 'hand_status': [[False, 12, 1], [True, 14, 1]]}
        '''
        self.player_names = data["player_names"]
        self.visible_cards = data["visible_cards"]
        self.hand_status = data["hand_status"]
        self.playerByPlayer()
