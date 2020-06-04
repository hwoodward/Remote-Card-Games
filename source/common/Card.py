class Card():
    """ This defines a playing card for use in the game

    Every card is an integer number and a suit (jokers have suit None and number 0)
    A card can tell you its color for rule checking
    """
    def __init__(self, number, suit, deck):
        if suit not in [None, 'Spades', 'Hearts', 'Diamonds', 'Clubs']:
            raise ValueError("Invalid Suit")
        self.suit = suit

        if suit is None:
            self.number = 0 #Jokers are always 0
        elif number not in range(1,14): #range includes start but not stop number
            raise ValueError("Invalid card number")
        else:
            self.number = number

        self.deck = int(deck)

    def getColor(self):
        if self.suit in ['Spades', 'Clubs']:
            return 'Black'
        if self.suit in ['Hearts', 'Diamonds']:
            return 'Red'
        return None #For jokers

    def serialize(self):
        """translate into a format podsixnet can translate"""
        return (self.number, self.suit, self.deck)

    @staticmethod
    def deserialize(representation):
        """create a card object from the podsixnet transportable serialization"""
        return Card(representation[0], representation[1], representation[2])

    def __str__(self):
        if self.suit is None:
            return "Joker"
        if self.number > 10:
            if self.number == 11:
                return "Jack of " + self.suit
            if self.number == 12:
                return "Queen of " + self.suit
            if self.number == 13:
                return "King of " + self.suit
        if self.number == 1:
            return "Ace of " + self.suit
        return "{0} of {1}".format(self.number, self.suit)

    def __repr__(self):
        return "({0}, {1})".format(self.number, self.suit)

    def __eq__(self, other):
        return (self.number == other.number) and (self.suit == other.suit) and (self.deck == other.deck)

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def getStandardDeck(num):
        """Provides a standard 52 card deck"""
        return [Card(1, 'Spades', num),
                Card(2, 'Spades', num),
                Card(3, 'Spades', num),
                Card(4, 'Spades', num),
                Card(5, 'Spades', num),
                Card(6, 'Spades', num),
                Card(7, 'Spades', num),
                Card(8, 'Spades', num),
                Card(9, 'Spades', num),
                Card(10, 'Spades', num),
                Card(11, 'Spades', num),
                Card(12, 'Spades', num),
                Card(13, 'Spades', num),
                Card(1, 'Hearts', num),
                Card(2, 'Hearts', num),
                Card(3, 'Hearts', num),
                Card(4, 'Hearts', num),
                Card(5, 'Hearts', num),
                Card(6, 'Hearts', num),
                Card(7, 'Hearts', num),
                Card(8, 'Hearts', num),
                Card(9, 'Hearts', num),
                Card(10, 'Hearts', num),
                Card(11, 'Hearts', num),
                Card(12, 'Hearts', num),
                Card(13, 'Hearts', num),
                Card(1, 'Diamonds', num),
                Card(2, 'Diamonds', num),
                Card(3, 'Diamonds', num),
                Card(4, 'Diamonds', num),
                Card(5, 'Diamonds', num),
                Card(6, 'Diamonds', num),
                Card(7, 'Diamonds', num),
                Card(8, 'Diamonds', num),
                Card(9, 'Diamonds', num),
                Card(10, 'Diamonds', num),
                Card(11, 'Diamonds', num),
                Card(12, 'Diamonds', num),
                Card(13, 'Diamonds', num),
                Card(1, 'Clubs', num),
                Card(2, 'Clubs', num),
                Card(3, 'Clubs', num),
                Card(4, 'Clubs', num),
                Card(5, 'Clubs', num),
                Card(6, 'Clubs', num),
                Card(7, 'Clubs', num),
                Card(8, 'Clubs', num),
                Card(9, 'Clubs', num),
                Card(10, 'Clubs', num),
                Card(11, 'Clubs', num),
                Card(12, 'Clubs', num),
                Card(13, 'Clubs', num)]

    @staticmethod
    def getJokerDeck(num):
        """Provides a deck with jokers based on the standard deck"""
        return Card.getStandardDeck(num) + [Card(0, None, num), Card(0, None, num)]
