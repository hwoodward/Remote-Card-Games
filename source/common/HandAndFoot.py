"""This is the ruleset reference for HandAndFoot (hand and foot)

It defines:
- all the constants needed to set up and render the game for the server and client
- all the rule checking methods necessary for the client to play the game
"""
from common.Card import Card

import math

Game_Name = "Hand and Foot"

def Num_Decks(numPlayers):
    """Specify how many decks of cards to put in the draw pile"""
    return math.ceil(numPlayers*1.5)

def Single_Deck():
    """return a single deck of the correct type"""
    return Card.GetJokerDeck()

Draw_Size = 2
Pickup_Size = 8
Discard_Size = 1

def isWild(card):
    """returns true if a card is a wild"""
    if card._number in [0,2]:
        return True
    else:
        return False

def getKeyOptions(card):
    """returns the possible keys for the groups the card can go in"""
    if not isWild(card):
        if card._number == 3:
            raise Exception("Cannot play 3s")
        return [card._number]
    else:
        return [1,4,5,6,7,8,9,10,11,12,13]

def canPlayGroup(key, cardGroup):
    """returns true if a group of cards can be played"""
    if key == 3:
        return Exception("Illegal key - cannot play 3s")
    typeDiff = 0
    for card in cardGroup:
        if isWild(card):
            typeDiff -= 1
        if card._number == key:
            typeDiff += 1
        else:
            raise Exception("Illegal card in group: {0} is not wild and is not part of the {1} group".format(card, key))
    if typeDiff > 0:
        return True
    raise Exception("Too many wilds in {0} group.".format(key))

def cardValue(card):
    """Returns the point value for a card"""
    if card._number in [4,5,6,7,8,9]:
        return 5
    if card._number in [10,11,12,13]:
        return 10
    if card._number == 1:
        return 15
    if card._number == 2:
        return 20
    if card._number == 0:
        return 50
    if card._number == 3:
        if card.GetColor() == 'Black':
            return 0
        if card.GetColor() == 'Red':
            return 500
    raise ValueError("Card submitted is not a legal playing card option")


#TODO: Fill in other constants and methods
"""
- score calculator for a given set of cards
- meld allowability (NOTE: caniesta points don't count for meld)
- score calculation at the end of a round (caniestas do count and you have to cancel points in the hand)
- round list
- pile pickup allowability
- more
"""
