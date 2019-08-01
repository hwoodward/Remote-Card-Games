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

#TODO: Fill in other constants and methods
"""
- score calculator for a given set of cards
- set legality checking
- unique set naming for meld dictionary
- round list
- pile pickup requirements and size
- more
"""
