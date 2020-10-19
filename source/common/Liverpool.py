"""This is the ruleset reference for Liverpool

It defines:
- all the constants needed to set up and render the game for the server and client
- all the rule checking methods necessary for the client to play the game
"""
from common.Card import Card

import math

Game_Name = "Liverpool"

Draw_Size = 1
Pickup_Size = 1
Discard_Size = 1
play_pick_up = False # picking up the pile doesn't force cards to be played.
# isWild method not working in TableView so added wildnumbers. this statement
#todo: figure out issue with TableView.
wild_numbers = [0]

# Liverpool: number of sets and runs required to meld.
# first element below is temporary (for testing).
Meld_Threshold = [(1,1), (2,0), (1,1), (0,2), (3,0), (2,1), (1,2), (0,3)]
Number_Rounds = len(Meld_Threshold)  # For convenience

Deal_Size = 11
Hands_Per_Player = 1
notes = ["You can only pick up the pile at the start of your turn (buying not yet implemented)."]


def numDecks(numPlayers):
    """Specify how many decks of cards to put in the draw pile"""
    return math.ceil(numPlayers*0.6)


def singleDeck(n):
    """return a single deck of the correct type, n designates which deck of the numDecks to be used"""
    return Card.getJokerDeck(n)


def isWild(card):
    """returns true if a card is a wild"""
    if card.number in wild_numbers:
        return True
    else:
        return False


# todo below is for checking on sets, but for liverpool will also have runs.
# player will probably have to state which set a card goes with, so this may be extraneous.
#  FOR LIVERPOOL KEY SHOULD NOT BE RANK, BUT POSSIBLE VALUE GIVEN
#  INDEX OF BUTTON USED TO PREPARE CARD.  FOR SETS THIS WILL BE RANK CARD.NUMBER FOR
#  EXISTING SET, AND FOR RUN IT WILL BE PLACE IN
#  RUN=(NUMBER BETWEEN MIN-1 AND MAX+1) THAT HASN'T BEEN TAKEN.
def getKeyOptions(card):
    """returns the possible keys for the groups the card can go in"""
    if not isWild(card):
        return [card.number]
    else:
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


def canPlayGroup(key, card_group, this_round=0):
    """checks if a group can be played
    
    returns True if it can, otherwise raises an exception with an explanation.
    In Liverpool key of prepared (=assigned) cards = key of button = (name, button #)
    """
    if len(card_group) == 0:
        return True  # Need to allow empty groups to be "played" due to side-effects of how we combined dictionaries
    print('line 71 in Liverpool.py')
    print(key)
    if key[1] < Meld_Threshold[this_round][0]:   # then this is a set.
        print('in canPlayGroup')
        print(key)
        # check if this is a valid set.
        if len(card_group) < 3:
            raise Exception("Too few cards in set - minimum is 3")
        # check that group contains only wilds and one card_number.
        card_numbers = []
        print('in Liverpool.py')
        for card in card_group:
            print(card)
            print(card.number)
            if not isWild(card):
                print('debug - point A')
                print(card_numbers)
                card_numbers.append(card.number)
                print(card_numbers)
                print(card.number)
            else:
                print(card)
                print('debug - at point B, thinks this card is Wild')
        unique_numbers = list(set(card_numbers))
        if len(unique_numbers) > 1:
            raise Exception("Cards in a set must all have the same rank (except wilds).")
        # check that have more naturals than wilds.
        typeDiff = 0
        unique_number = unique_numbers[0]
        for card in card_group:
            if isWild(card):
                typeDiff -= 1
            elif card.number == unique_number:
                typeDiff += 1
    else:
        print('not checking runs')
        return True
    '''
        # check that this is a valid run.
        if len(card_group) < 4:
            raise Exception("Too few cards in run - minimum is 4")
    typeDiff = 0
    for card in card_group:
        if isWild(card):
            typeDiff -= 1
        elif card.number == unique_number: # < not used for runs
            typeDiff += 1
        else:
            raise Exception("Illegal card in group: {0} is not wild and is not part of the {1} group".format(card, key))
    if typeDiff > 0:
        return True
    raise Exception("Too many wilds in {0} group.".format(key))
    '''


def canMeld(prepared_cards, round_index, player_index):
    """Determines if a set of card groups is a legal meld"""
    #
    # This section differs from HandAndFoot.
    print('canMeld--return True no matter what.')
    # debugging - still need to debug canMeld routine, but want to get past it for now....
    if True:
        return True
    required_groups =  Meld_Threshold[round_index][0] + Meld_Threshold[round_index][1]
    valid_groups = 0
    print(prepared_cards)
    for key, card_group in prepared_cards.items():
        print('in liverpool.py canMeld')
        print(key)
        if canPlayGroup(key, card_group, round_index) and key[0] == player_index:
            print('in if canPlayGroup indent')
            valid_groups = valid_groups + 1
            print(key, required_groups, valid_groups)
    if required_groups > valid_groups :
        raise Exception("Must have all the required sets and runs to meld")
    return True


def canPickupPile(top_card, prepared_cards, played_cards, round_index):
    """Determines if the player can pick up the pile with their suggested play-always True for Liverpool"""
    return True

def canPlay(prepared_cards, visible_cards, player_index, round_index):
    """Confirms if playing the selected cards is legal"""
    # Has player already melded -- if so visible_cards[player_index] will NOT be empty and
    #
    print('current state: rules are not checked, '
          'but cards are played, disappear from hand, but only first one is displayed on board.'
          'Unfortunately, when you try to play on another player the cards appear on your board'
          ' (need to fix indexing bug)')
    # if not visible_cards[player_index]:   # empty dicts evaluate to false (as does None)
    #     return canMeld(prepared_cards, round_index, player_index)
    # Combine dictionaries to get the final played cards if suggest cards played
    # in Liverpool.
    # prepared cards is a dictionary where key = tuple. ( player index, group number)
    # (where a group is a set or run) on that player's board.
    # visible cards is a list of dictionaries. List index is player index
    # and key in dictionary is group number.
    i_tot = len(visible_cards)
    all_visible_one_dictionary = {}
    for idx in range(i_tot):
        temp_dictionary_v = visible_cards[idx]
        # gathering all of prepared_cards for player idx's groups into single dictionary.
        temp_dictionary = all_visible_one_dictionary
        all_visible_one_dictionary = (combineCardDicts(temp_dictionary, temp_dictionary_v))
    combined_cards = combineCardDicts(all_visible_one_dictionary, prepared_cards)
    for key, card_group in combined_cards.items():
        canPlayGroup(key, card_group)
    return True

def combineCardDicts(dict1, dict2):
    """Combine two dictionaries of cards, such as played and to be played cards"""
    combined_cards = {}
    for key in set(dict1).union(dict2):
        combo_list = []
        for card in dict1.setdefault(key, []):
            combo_list.append(card)
        for card in dict2.setdefault(key, []):
            combo_list.append(card)
        combined_cards[key] = combo_list
    return combined_cards


def cardValue(card):
    """Returns the point value for a card"""
    if card.number in [2, 3, 4, 5, 6, 7, 8, 9]:
        return 5
    if card.number in [10, 11, 12, 13]:
        return 10
    if card.number == 1:
        return 15
    if card.number == 0:
        return 20
    raise ValueError("Card submitted is not a legal playing card option")


def goneOut(played_cards):
    """Returns true if the played set of cards meets the requirements to go out

    This DOES NOT confirm that a player has no cards, that is the controllers job
    For Liverpool if the player has no cards, then they've gone out.
    Need to let server know, but no additional requirements.
    Might not even need this function...
    """
    return True


def scoreGroup(card_group):
    """Scores a group of cards for raw value"""
    score = 0
    for card in card_group:
        score += cardValue(card)
    return score


def scoreRound(irrelevant1, unplayed_cards, irrelevant2):
    """Calculates the score for a player for a round"""
    score = scoreGroup(unplayed_cards)
    return score
