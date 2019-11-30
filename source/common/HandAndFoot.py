"""This is the ruleset reference for HandAndFoot (hand and foot)

It defines:
- all the constants needed to set up and render the game for the server and client
- all the rule checking methods necessary for the client to play the game
"""
from common.Card import Card

import math

Game_Name = "Hand and Foot"

Draw_Size = 2
Pickup_Size = 8
Discard_Size = 1

Meld_Threshold = [50, 90, 120, 150]
Number_Rounds = len(Meld_Threshold) #For convenience

Deal_Size = 11
Hands_Per_Player = 2

def numDecks(numPlayers):
    """Specify how many decks of cards to put in the draw pile"""
    return math.ceil(numPlayers*1.5)

def singleDeck():
    """return a single deck of the correct type"""
    return Card.getJokerDeck()

def isWild(card):
    """returns true if a card is a wild"""
    if card.number in [0,2]:
        return True
    else:
        return False

def getKeyOptions(card):
    """returns the possible keys for the groups the card can go in"""
    if not isWild(card):
        if card.number == 3:
            raise Exception("Cannot play 3s")
        return [card.number]
    else:
        return [1,4,5,6,7,8,9,10,11,12,13]

def canPlayGroup(key, card_group):
    """checks if a group can be played
    
    returns True if it can, otherwise raises an exception with an explanation
    """
    if len(card_group) == 0:
        return True # Need to allow empty groups to be "played" due to some side-effects of how we combined dictionaries
    if key == 3:
        raise Exception("Illegal key - cannot play 3s")
    if len(card_group) < 3: 
        raise Exception("Too few cards in group - minimum is 3");
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
    score = 0
    for key, card_group in prepared_cards.items():
        if canPlayGroup(key, card_group):
            score += scoreGroup(card_group)
    min_score = Meld_Threshold[round_index]
    if score < min_score:
        raise Exception("Meld does not meat round minimum score or {0}".format(min_score))
    return True


def canPickupPile(top_card, prepared_cards, played_cards, round_index):
    """Determines if the player can pick up the pile with their suggested play"""
    top_key = None
    try:
        key_opts = getKeyOptions(top_card)
    except:
        raise Exception("Cannot pickup the pile on 3s because you cannot play 3s")
    else:
        if len(key_opts) > 1:
            raise Exception("Cannot pickup the pile on wilds")
        top_key = key_opts[0]
    #check suggested play contains 2 cards matching the top card
    top_group = prepared_cards[top_key]
    total = 0
    for card in top_group:
        if not isWild(card):
            total += 1
    if total < 2:
        raise Exception("Cannot pickup the pile without 2 cards matching the top card of the discard pile")
    #check suggested play is legal (using adjusted deep copy of prepared cards)
    temp_prepared = {}
    for key, card_group in prepared_cards.items():
        temp_prepared[key] = [x for x in card_group]
        if key == top_key:
            temp_prepared[key].append(top_card)
    return canPlay(temp_prepared, played_cards, round_index)

def canPlay(prepared_cards, played_cards, round_index):
    """Confirms if playing the selected cards is legal"""
    if not played_cards: #empty dicts evaluate to false (as does None)
        return canMeld(prepared_cards, round_index)
    #Combine dictionaries to get the final played cards if suggest cards played
    combined_cards = combineCardDicts(prepared_cards, played_cards)
    #Confirm each combined group is playable
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
    if card.number in [4,5,6,7,8,9]:
        return 5
    if card.number in [10,11,12,13]:
        return 10
    if card.number == 1:
        return 15
    if card.number == 2:
        return 20
    if card.number == 0:
        return 50
    if card.number == 3:
        if card.getColor() == 'Black':
            return 0
        if card.getColor() == 'Red':
            return 500
    raise ValueError("Card submitted is not a legal playing card option")

def goneOut(played_cards):
    """Returns true if the played set of cards meets the requirements to go out
    
    This DOES NOT confim that a player has no cards, that is the controllers job
    Needs to have 1 clean and 1 dirty caniesta (set of 7)
    """
    clean = False
    dirty = False
    for card_group in played_cards.values():
        caniesta_status = caniestaHelper(card_group)
        if caniesta_status == 'Clean':
            clean = True
        if caniesta_status == 'Dirty':
            dirty = True
    if clean and dirty:
        return True
    return False

def caniestaHelper(card_group):
    """Returns a constant indicating canista status for the set
    
    options are:
    None for sets under 7
    'Clean' for clean caniestas
    'Dirty' for dirty caniestas
    """
    if len(card_group) >= 7:
        isDirty = False
        for card in card_group:
            if isWild(card):
                isDirty = True
        if isDirty:
            return 'Dirty'
        else:
            return 'Clean'
    return None

def calculateBonuses(played_cards, went_out):
    """Scores a card_group, including Caniesta bonuses"""
    bonus = 0
    if went_out:
        bonus += 100
    for card_group in played_cards.values():
        caniesta_status = caniestaHelper(card_group)
        if caniesta_status == 'Clean':
            bonus += 500
        if caniesta_status == 'Dirty':
            bonus += 300
    return bonus

def scoreGroup(card_group):
    """Scores a group of cards for raw value"""
    score = 0
    for card in card_group:
        score += cardValue(card)
    return score

def scoreRound(played_cards, unplayed_cards, went_out):
    """Calculates the score for a player for a round"""
    score = 0
    score += calculateBonuses(played_cards, went_out)
    score -= scoreGroup(unplayed_cards)
    for card_group in played_cards.values():
        score += scoreGroup(card_group)
    return score
