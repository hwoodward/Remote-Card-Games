"""This is the ruleset reference for Liverpool

It defines:
- all the constants needed to set up and render the game for the server and client
- all the rule checking methods necessary for the client to play the game
"""
from common.Card import Card
from client.RunManagement import processRuns

import math

Game_Name = "Liverpool"

Shared_Board = True  # once you meld you can play on other players set/runs
Buy_Option = True  # in Liverpool you can purchase top discard.
purchase_time = 3.0 # time players have to request top discard (in seconds).
play_pick_up = False # False because picking up the pile doesn't force cards to be played.
Draw_Size = 1
Pickup_Size = 1
Discard_Size = 1
wild_numbers = [0]

# Liverpool: number of sets and runs required to meld.  Order is important! (code relies on sets being first).
# first element below is temporary (for testing).
# todo: on server side enable starting game in later rounds.
Meld_Threshold = [(3,0), (2,0), (1,1), (0,2), (3,0), (2,1), (1,2), (0,3)]
Number_Rounds = len(Meld_Threshold)  # For convenience
Deal_Size = 11
Hands_Per_Player = 1
notes = ["Clicking on pile only works on your turn. If you are eligible to buy a card, then click on y (for yes)."]
help_text = ['Welcome to a Liverpool!  Meld requirement will display when round begins ',
                              ' (at beginning usually 2 sets, no runs). # decks = ceil(# players *0.6).',
                              'To draw click on the deck of cards (upper left). To discard select ONE card & double click on discard button. ',
                              'To prepare cards click on appropriate Run/Set button (buttons will appear after you click OK)',
                              'To pick up discarded card click on discard pile, to attempt to BUY discard type y.',
                              "Cumulative score will display beneath player's cards.",
                              'When ready to start playing click on the YES button on the lower right.']


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

def canPlayGroup(key, card_group, this_round):
    """checks if a group can be played
    
    For runs this assumes card_group has already been processed (sorted with Aces and Wilds assigned
    appropriate tempnumber).
    returns True if it can, otherwise raises an exception with an explanation.
    In dictionary key of prepared (=assigned) cards = key of button = (based on (player index, card group index))
    """

    if key[1] < Meld_Threshold[this_round][0]:   # then this is a set.
        # check if this is a valid set.
        if len(card_group) < 3:
            raise Exception("Too few cards in set - minimum is 1 (will change to 3 later)")
        # check that group contains only wilds and one card_number.
        card_numbers = []
        num_cards = len(card_group)
        for card in card_group:
            if not isWild(card):
                card_numbers.append(card.number)
        num_naturals = len(card_numbers)
        unique_numbers = list(set(card_numbers))
        if len(unique_numbers) > 1:
            raise Exception("Cards in a set must all have the same rank (except wilds).")
        # check that have more naturals than wilds.
        unique_number = unique_numbers[0]
        if num_naturals <= (num_cards - num_naturals):
            text = "Too many wilds in set of " + str(unique_number) + "'s"
            raise Exception(text)
    else:
        # check that this processed run follows rules
        # Note processRuns also has rule checking (rules around assigning Wilds and placing
        # Aces hi/lo are done in that method).
        if len(card_group) < 4:
            raise Exception("Too few cards in run - minimum is 4")
        suits_in_run = []
        for card in card_group:
            if not isWild(card):
                suits_in_run.append(card.suit)
        unique_suits = list(set(suits_in_run))
        if len(unique_suits) > 1:
            raise Exception("Cards in a run must all have the same suit (except wilds).")
    return True

def canMeld(prepared_cards, round_index, player_index):
    """This insures that all required groups are present, but the legality of the groups is not checked until later. """
    #
    required_groups =  Meld_Threshold[round_index][0] + Meld_Threshold[round_index][1]
    valid_groups = 0
    for key, card_group in prepared_cards.items():
        if key[0] == player_index and len(card_group) > 0:
            valid_groups = valid_groups + 1
    if required_groups > valid_groups :
        raise Exception("Must have all the required sets and runs to meld")
    return True

def canPickupPile(top_card, prepared_cards, played_cards, round_index):
    """Determines if the player can pick up the pile with their suggested play-always True for Liverpool"""
    return True

def canPlay(processed_full_board, round_index):
    """Confirms each group to be played meets Liverpool requirements.

    Some rule checking (such as have enough groups to meld) were checked when processed_full_board was created."""
    for k_group, card_group in processed_full_board.items():
        canPlayGroup(k_group, card_group, round_index)
    return

def combineCardDicts(dict1, dict2):
    """Combine two dictionaries of cards, such as played and to be played cards.

    This should work for both cards and serialized cards."""
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
    Review note: For Liverpool if the player has no cards, then they've gone out.
    Need to let server know, but no additional requirements.
    Function needed for HandAndFoot, so keep it here as well.
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
