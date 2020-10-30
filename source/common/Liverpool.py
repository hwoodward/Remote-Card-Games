"""This is the ruleset reference for Liverpool

It defines:
- all the constants needed to set up and render the game for the server and client
- all the rule checking methods necessary for the client to play the game
"""
from common.Card import Card

import math

Game_Name = "Liverpool"

Shared_Board = True
Draw_Size = 1
Pickup_Size = 1
Discard_Size = 1
play_pick_up = False # False because picking up the pile doesn't force cards to be played.
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


# Review note: below is for checking on sets in HandAndFoot (not needed for Liverpool sets)
#  In Liverpool wild will need to be (MIN-1 or MAX+1). That still needs to be implmented.
#  Keeping code here (commented out) until I know whether or not we'll use it.
# todo: implment ability to choose if Aces and Wilds are hi or lo in runs.
'''
def getKeyOptions(card):
    """returns the possible keys for the groups the card can go in"""
    if not isWild(card):
        return [card.number]
    else:
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
'''

def canPlayGroup(key, card_group, this_round):
    """checks if a group can be played
    
    For runs this assumes card_group has already been processed (sorted with Aces and Wilds assigned
    appropriate tempnumber).
    returns True if it can, otherwise raises an exception with an explanation.
    In dictionary key of prepared (=assigned) cards = key of button = (based on (player index, card group index))
    """
    # todo: delete this Review Note:
    # Lefotover remnant from HandAndFoot,
    # don't do this in Liverpool.py because meld requirement is so different.:
    #   if len(card_group) == 0:
    #       return True  # In liverpool do NOT want to count empty groups.
    if key[1] < Meld_Threshold[this_round][0]:   # then this is a set.
        # check if this is a valid set.
        if len(card_group) < 1:
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
        if len(card_group) < 2:
            # todo:  for debugging only require  < 2, will need to change that to 4 later.
            raise Exception("Too few cards in run - minimum is 2 (for now) 4 (final version)")
        suits_in_run = []
        for card in card_group:
            if not isWild(card):
                suits_in_run.append(card.suit)
        unique_suits = list(set(suits_in_run))
        if len(unique_suits) > 4:
            #todo: for testing not requiring one suit.  Fix this later.
            raise Exception("Cards in a run must all have the same suit (except wilds).")
    return True

def processRuns(card_group):
    # handle sorting of run, including placement of wilds.  Handles some rules checking.

    # processRuns does not presume length requirement or that all cards are in same suit.
    # it DOES presume that if Aces are not wild, then they are hi or low, but not both.
    card_group.sort(key=lambda wc: wc.tempnumber)
    first_card = True
    groups_wilds = []
    temp_run_group = []
    aces_list =[]
    for card in card_group:                    # separate unassigned wilds and Aces from rest of run.
        if card.tempnumber in wild_numbers:
            groups_wilds.append(card)
        elif card.tempnumber == 1:
            aces_list.append(card)
        else:
            temp_run_group.append(card)
    card_group  = []                         # rebuild card_group below
    for card in temp_run_group:
        if first_card:
            first_card = False
            if card.tempnumber == 2 and len(aces_list) > 0:
                this_ace = aces_list.pop(0)
                card_group.append(this_ace)
            card_group.append(card)
        else:
            if card.tempnumber == (card_group[-1].tempnumber + 1):
                card_group.append(card)
            elif card.tempnumber == (card_group[-1].tempnumber + 2) and len(groups_wilds) > 0:
                this_wild = groups_wilds.pop(0)
                this_wild.tempnumber = card_group[-1].tempnumber + 1
                card_group.append(this_wild)
                card_group.append(card)
            elif card.tempnumber == card_group[-1].tempnumber:
                if isWild(card):
                    card.tempnumber = card.number
                    groups_wilds.append(card)
                elif isWild(card_group[-1]):
                    this_wild = card_group.pop(-1)
                    this_wild.tempnumber = this_wild.number
                    groups_wilds.append(card)
                else:
                    raise Exception('Card value already in the run.')
            else:
                raise Exception('too big a gap between numbers')
    if len(aces_list) > 0 and card_group[-1].tempnumber == 13:
        this_ace = aces_list.pop(0)
        this_ace.tempnumber = 14
        card_group.append(this_ace)
    if len(aces_list) > 0:
        raise Exception('Cannot play Ace in designated run')
    while len(groups_wilds) > 0 :
        # todo: handle jokers properly -- ask if high or low when both are an option.
        this_wild = groups_wilds.pop(0)
        if card_group[-1].tempnumber < 14 and not isWild(card_group[-1]):
            this_wild.tempnumber = card_group[-1].tempnumber + 1
            card_group.append(this_wild)
        elif card_group[0].tempnumber > 1 and not isWild(card_group[0]):
            this_wild.tempnumber = card_group[0].tempnumber - 1
            card_group.insert(0, this_wild)
        else:
            raise Exception('you have too many jokers in a single Run')
    last_card_wild = False
    second2last_card_wild = False
    for card in card_group:
        if (isWild(card) and last_card_wild) or (isWild(card) and second2last_card_wild):
            raise Exception('Must have two natural cards between wild cards in runs')
        second2last_card_wild = last_card_wild
        last_card_wild = isWild(card)
    return card_group

def canMeld(prepared_cards, round_index, player_index):
    """Determines if a set of card groups is a legal meld, called from canPlay."""
    #
    # This section differs from HandAndFoot.
    required_groups =  Meld_Threshold[round_index][0] + Meld_Threshold[round_index][1]
    valid_groups = 0
    for key, card_group in prepared_cards.items():
        if key[0] == player_index:
            if key[1] >= Meld_Threshold[round_index][0]:
                processed_group = processRuns(card_group)  # process runs from prepared_cards
            else:
                processed_group = card_group
            if canPlayGroup(key, processed_group, round_index):
                valid_groups = valid_groups + 1
    if required_groups > valid_groups :
        raise Exception("Must have all the required sets and runs to meld")
    return True

def canPickupPile(top_card, prepared_cards, played_cards, round_index):
    """Determines if the player can pick up the pile with their suggested play-always True for Liverpool"""
    return True

def canPlay(prepared_cards, played_cards_dictionary, player_index, round_index):

    """Confirms if playing the selected cards is legal"""

    played_groups = []      # Need to know if group has already been started on the board.
    for key, cards in played_cards_dictionary.items():
        if len(cards) > 0:
            played_groups.append(key)
    for key, cards in prepared_cards.items():
        if len(cards) > 0:
            group_key = key
            if not group_key[0] == player_index and group_key not in played_groups:
                raise Exception("You are not allowed to begin another player's sets or runs.")
    # if a player has already melded than key = (player_index,0) will have dictionary entry with cards.
    if (player_index,0) not in played_groups:
        return canMeld(prepared_cards, round_index, player_index)
    # gathering all played and prepared_cards into single dictionary (needed for rule checking).
    combined_cards = combineCardDicts(played_cards_dictionary, prepared_cards)
    for k_group, card_group in combined_cards.items():
        if k_group[1] >= Meld_Threshold[round_index][0]:
            processed_group = processRuns(card_group)               # process runs from combined_cards
        else:
            processed_group = card_group
            # todo: decide when to sort sets.
        canPlayGroup(k_group, processed_group, round_index)
    # todo: debug next line:
    # return combined_cards  < caused an unexpected error...see notes in ClientState.py.
    return True

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

def restoreRunAssignment(visible_scards_dictionary, round_index):
    """ assign values to Wild cards and Aces in runs from server.

    Needed to maintain integrity of Wilds' assigned values in runs.  Server does not know tempnumbers """

    # todo: this does not assign tempnumber for wilds in middle of run.  processRuns should work regardless of
    #  whether those wilds have tempnumbers already assigned or not.  Debating whether code below -
    #  would be more efficient if simply set tempnumber for all wilds here?
    if len(visible_scards_dictionary) == 0:
        return(visible_scards_dictionary)
    cardgroup_dictionary = {}
    for key, scard_group in visible_scards_dictionary.items():
        card_group = []
        for scard in scard_group:
            card = Card(scard[0], scard[1], scard[2])
            card_group.append(card)
        cardgroup_dictionary[key] = card_group
    for k_group, card_group in cardgroup_dictionary.items():
        if k_group[1] >= Meld_Threshold[round_index][0]:       # check if this is a run.
            if card_group[-1].number in wild_numbers:    # reset tempnumber for Wilds/Aces if they are at the end.
                card_group[-1].assignWild(card_group[-2].tempnumber + 1)
            elif card_group[-1].number == 1:
                card_group[-1].assignWild(14)
            if card_group[0].number in wild_numbers:    # reset tempnumber for wild cards if they are at the beginning.
                card_group[0].assignWild(card_group[1].tempnumber - 1)
        return cardgroup_dictionary

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
