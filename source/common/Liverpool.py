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

# Meld_Threshold = [50, 90, 120, 150]  # from Hand and Foot example
# first element below is for testing only.
Meld_Threshold = [(2,1), (2,0), (1,1), (0,2), (3,0), (2,1), (1,2), (0,3)]  # Liverpool need this to be number of sets and runs.
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
    if card.number in [0]:
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


def canPlayGroup(key, card_group):
    """checks if a group can be played
    
    returns True if it can, otherwise raises an exception with an explanation
    """
    if len(card_group) == 0:
        return True  # Need to allow empty groups to be "played" due to side-effects of how we combined dictionaries
    if key == 3:
        raise Exception("Illegal key - cannot play 3s")
    if len(card_group) < 3: 
        raise Exception("Too few cards in group - minimum is 3")
    typeDiff = 0
    for card in card_group:
        if isWild(card):
            typeDiff -= 1
        elif card.number == key:
            typeDiff += 1
        else:
            raise Exception("Illegal card in group: {0} is not wild and is not part of the {1} group".format(card, key))
    if typeDiff > 0:
        return True
    raise Exception("Too many wilds in {0} group.".format(key))


def canMeld(prepared_cards, round_index):
    """Determines if a set of card groups is a legal meld"""
    # todo: rewrite to see if have legal set/run for each one required in meld threshold.
    print('Liverpool does not currently check that meld is legal.  Must edit Liverpool.canMeld')
    '''
    # This section is from HandAndFoot.
    score = 0
    for key, card_group in prepared_cards.items():
        if canPlayGroup(key, card_group):
            score += scoreGroup(card_group)
    min_score = Meld_Threshold[round_index]
    if score < min_score:
        raise Exception("Meld does not meet round minimum score or {0}".format(min_score))
    '''
    return True


def canPickupPile(top_card, prepared_cards, played_cards, round_index):
    """Determines if the player can pick up the pile with their suggested play-always True for Liverpool"""
    return True

def canPlay(prepared_cards, played_cards, round_index):
    """Confirms if playing the selected cards is legal"""
    if not played_cards:   # empty dicts evaluate to false (as does None)
        return canMeld(prepared_cards, round_index)
    # Combine dictionaries to get the final played cards if suggest cards played
    combined_cards = combineCardDicts(prepared_cards, played_cards)
    # Confirm each combined group is playable
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
