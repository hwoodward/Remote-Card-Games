import pygame
import textwrap
import client.UIConstants as UIC
from common.Card import Card
class ShowTable:
    """This class displays the public information -- cards melded, etc,...    """

    def __init__(self,win):

        self.display = win
        # TODO: replace example values with data from server.
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

    def playerByPlayer(self):
        self.Compress_Sets(self.visible_cards)
        num_players = len(self.hand_stats)
        # currently set-up with one player per column. May need to change that for more players.
        players_sp_w = UIC.Disp_Width / num_players
        players_sp_top = UIC.Disp_Height / 5
        players_sp_h = UIC.Disp_Height / 2
        color_index = 2
        bk_grd_rect = (0, players_sp_top, players_sp_w, players_sp_h)
        for card_holder in self.hand_stats:            
            # plan to move below to a helper function...
            player_name = card_holder[0]
            melded_summary = self.compressed_info[player_name]
            print(player_name)
            print(melded_summary)
            pygame.draw.rect(self.display, UIC.outline_colors[color_index], bk_grd_rect,0)
            player_text = player_name + '\r'
            for key in melded_summary:
                player_text = player_text + ' ' + str(melded_summary[key])
                print(player_text)
            text_surface, text_rect = self.text_objects(player_text, UIC.Small_Text)
            text_rect.center = ((bk_grd_rect[0] + 0.5 * players_sp_w), (bk_grd_rect[1] + 0.05 * UIC.Disp_Height))
            self.display.blit(text_surface, text_rect)
            print('made it to here')
            # Move to next players rectangle and color:
            bk_grd_rect = (bk_grd_rect[0] + players_sp_w, bk_grd_rect[1], bk_grd_rect[2], bk_grd_rect[3])
            color_index = (color_index + 3) % 6

    ''' Screen is no longer rendered in TableView.
    def render(self):
        """This should render the actual UI, for now it just prints the hand"""
        # TODO render the table view showing the visible cards
        print("draw visible cards")
    '''

    def Compress_Sets(self, v_cards):
        """ Don't have space to display every card. Summarize sets here. """

        print("In Compress_Sets")
        self.compressed_info = {}
        for element in v_cards:
            summary = {}
            key_player = element[0]
            melded = dict(element[1])
            for key in melded:
                set = melded[key]
                l = len(set)
                wild_count = 0
                for s_card in set:
                    # Need to change below to: if s_card.number == 0 or s_card.number == 2:
                    if s_card[0] == 0 or s_card[0] == 2:
                        wild_count = wild_count + 1
                summary[key]=(l, wild_count)

            self.compressed_info[key_player] = summary
        print(self.compressed_info)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, UIC.Black)
        return textSurface, textSurface.get_rect()