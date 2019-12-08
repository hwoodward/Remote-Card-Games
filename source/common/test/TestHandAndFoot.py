from common.Card import Card
import common.HandAndFoot as Rules
import unittest

class TestHandAndFoot(unittest.TestCase):
            
    def test_PickupCheck(self):
        """Confirm that canPickup works"""
        played_cards = {}
        prepared_cards = {}
        
        #confirm with meld and valid cards, works
        played_cards[1] = [Card(1, 'Clubs'), Card(1, 'Clubs'), Card(1, 'Clubs')]
        played_cards[4] = [Card(4, 'Clubs'), Card(4, 'Clubs'), Card(0, None)]
        prepared_cards[5] = [Card(5, 'Clubs'), Card(5, 'Clubs')]
        self.assertTrue(Rules.canPickupPile(Card(5, 'Hearts'), prepared_cards, played_cards, 0))
        
        #confirm without valid cards, fails
        prepared_cards[5] = [Card(5, 'Clubs')]
        with self.assertRaises(Exception):
            Rules.canPickupPile(Card(5, 'Hearts'), prepared_cards, played_cards, 0)
        
        prepared_cards[5] = [Card(5, 'Clubs'), Card(2, 'Clubs')]
        with self.assertRaises(Exception):
            Rules.canPickupPile(Card(5, 'Hearts'), prepared_cards, played_cards, 0)
        
        #confirm without meld, need to meet meld requirement
        prepared_cards[5] = [Card(5, 'Clubs'), Card(5, 'Clubs')]
        played_cards = {}
        with self.assertRaises(Exception):
            Rules.canPickupPile(Card(5, 'Hearts'), prepared_cards, played_cards, 0)

        #confirm meld requirement can INCLUDE top card
        prepared_cards[6] = [Card(2, 'Clubs'), Card(6, 'Diamonds'), Card(6, 'Diamonds'), Card(6, 'Diamonds')]
        self.assertTrue(Rules.canPickupPile(Card(5, 'Hearts'), prepared_cards, played_cards, 0))

        #confirm 3s can't be picked up
        with self.assertRaises(Exception):
            Rules.canPickupPile(Card(3, 'Hearts'), prepared_cards, played_cards, 0)

        #confirm wilds can't be picked up
        with self.assertRaises(Exception):
            Rules.canPickupPile(Card(0, None), prepared_cards, played_cards, 0)
      
    def test_PlayCheck(self):
        """Confirm canPlay works"""
        played_cards = {}
        prepared_cards = {}
        
        #confirm initial meld requires minimum point score
        prepared_cards[1] = [Card(1, 'Hearts'), Card(1, 'Hearts'), Card(1, 'Hearts')]
        with self.assertRaises(Exception):
            Rules.canPlay(prepared_cards, played_cards, 0)

        #confirm that incomplete sets rejected from meld
        prepared_cards[5] = [Card(5, 'Spades'), Card(5, 'Spades')] 
        with self.assertRaises(Exception):
            Rules.canPlay(prepared_cards, played_cards, 0)
         
        #confirm too many wilds are rejected from meld   
        prepared_cards[5].append(Card(5, 'Hearts'))
        prepared_cards[10] = [Card(10, 'Clubs'), Card(10, 'Clubs'), Card(0, None), Card(2,'Diamonds')]
        with self.assertRaises(Exception):
            Rules.canPlay(prepared_cards, played_cards, 0)

        prepared_cards[10].remove(Card(0, None))
        self.assertTrue(Rules.canPlay(prepared_cards, played_cards, 0))
        played_cards = Rules.combineCardDicts(played_cards, prepared_cards)
        prepared_cards = {}
        
        #confirm that incomplete sets rejected from add ons
        prepared_cards[6] = [Card(6,'Spades'), Card(6, 'Spades')]
        with self.assertRaises(Exception):
            Rules.canPlay(prepared_cards, played_cards, 0)
        
        prepared_cards[6].append(Card(6, 'Clubs'))
        self.assertTrue(Rules.canPlay(prepared_cards, played_cards, 0))
        played_cards = Rules.combineCardDicts(played_cards, prepared_cards)
        prepared_cards = {}
                         
        #confirm that threes can't be played
        prepared_cards[3] = [Card(3,'Spades'), Card(3, 'Diamonds'), Card(0, None)]
        with self.assertRaises(Exception):
            Rules.canPlay(prepared_cards, played_cards, 0)
        prepared_cards = {}
        
        #confirm too many wilds total rejected from add ons
        prepared_cards[10]=[Card(2, 'Clubs')]
        with self.assertRaises(Exception):
            Rules.canPlay(prepared_cards, played_cards, 0)
        
        prepared_cards[10].append(Card(10, 'Clubs'))
        self.assertTrue(Rules.canPlay(prepared_cards, played_cards, 0))
        played_cards = Rules.combineCardDicts(played_cards, prepared_cards)
        prepared_cards = {}
        
        #confirm wild only additions work
        prepared_cards[5] = [Card(0, None)]
        self.assertTrue(Rules.canPlay(prepared_cards, played_cards, 0))
    
    def test_GoneOut(self):
        """Confirm detection of going out works
        
        remember goneOut only called when player has no cards
        """
        played_cards = {}
        
        #confirm no caniestas doesn't go out
        played_cards[1] = [Card(1,'Spades'), Card(1, 'Spades'), Card(1, 'Spades'), Card(1, 'Spades'), Card(1,'Hearts'), Card(1, 'Spades')]
        played_cards[11] = [Card(11,'Clubs'), Card(11, 'Clubs'), Card(11, 'Clubs'), Card(11, 'Clubs'), Card(11, 'Clubs'), Card(11, 'Clubs')]
        
        self.assertFalse(Rules.goneOut(played_cards))
        
        #confirm multiple cleans doesn't go out
        played_cards[1].append(Card(1, 'Diamonds'))
        played_cards[11].append(Card(11, 'Spades'))
        self.assertFalse(Rules.goneOut(played_cards))
        
        #confirm multiple dirties doesn't go out
        played_cards[1].append(Card(0, None))
        played_cards[11].append(Card(0, None))
        self.assertFalse(Rules.goneOut(played_cards))

        #confirm clean and dirty is out
        played_cards[1].remove(Card(0, None))
        self.assertTrue(Rules.goneOut(played_cards))

    def test_Score(self):
        """Confirm scoring works"""
        played_cards = {}
        hand_cards = []
        went_out = True

        #confirm that a set of played cards that went out is correct
        played_cards[1] = [Card(1,'Spades'), Card(1, 'Spades'), Card(1, 'Spades'), Card(1, 'Spades'), Card(1,'Hearts'), Card(1, 'Spades')]
        played_cards[11] = [Card(11,'Clubs'), Card(11, 'Clubs'), Card(11, 'Clubs'), Card(11, 'Clubs'), Card(11, 'Clubs'), Card(11, 'Clubs')]
        self.assertEqual(Rules.scoreRound(played_cards, hand_cards, went_out), 250)
        
        #confirm that a same set of cards and a hand of just black threes is only different by went_out bonus
        went_out = False
        hand_cards = [Card(3, 'Clubs')]
        self.assertEqual(Rules.scoreRound(played_cards, hand_cards, went_out), 150)
        
        #confirm cards left in hand are counted against properly
        hand_cards = [Card(5, 'Spades'), Card(0, None), Card(10, 'Clubs')]
        self.assertEqual(Rules.scoreRound(played_cards, hand_cards, went_out), 85)
        
        #confirm caniesta bonuses are correct:
        #confirm clean bonus is 500 and still counts cards in caniesta
        played_cards[1].append(Card(1, 'Clubs'))
        self.assertEqual(Rules.scoreRound(played_cards, hand_cards, went_out), 600)
        #confirm dirty bonus is 300 and counts cards in caniesta
        played_cards[11].append(Card(2, 'Hearts'))
        self.assertEqual(Rules.scoreRound(played_cards, hand_cards, went_out), 920)
        
        #confirm that red 3 penalty is 500
        hand_cards.append(Card(3, 'Diamonds'))
        self.assertEqual(Rules.scoreRound(played_cards, hand_cards, went_out), 420)

if __name__ == '__main__':
    unittest.main()
