from common.Card import Card
import common.HandAndFoot as Rules
import unittest

class TestCardMethods(unittest.TestCase):
    
    def test_MeldCheck(self):
        """Confirm that canMeld works"""
        #TODO: confirm illegal sets rejected
        #TODO: confirm low point score rejected
        #TODO: confirm legal meld allowed
        
    def test_PickupCheck(self):
        """Confirm that canPickup works"""
        #TODO: confirm too small pile rejected
        #TODO: confirm illegal cards rejected
        #TODO: confirm two naturals required
        #TODO: confirm meld required
        
    def test_PlayCheck(self):
        """Confirm canPlay works"""
        #TODO: confirm that incomplete sets rejected
        #TODO: confirm too many wilds total rejected
        #TODO: confirm wild only additions work
    
    def test_GoneOut(self):
        """Confirm detection of going out works
        
        remember goneOut only called when player has no cards
        """
        #TODO: confirm no caniestas doesn't go out
        #TODO: confirm multiple cleans doesn't go out
        #TODO: confirm multiple dirties doesn't go out
        #TODO: confirm clean and dirty is out

    def test_Score(self):
        """Confirm scoring works"""
        #TODO: confirm that a set of played cards that went out is correct
        #TODO: confirm that a same set of cards and a hand of 0 is only different by went_out bonus
        #TODO: confirm cards left in hand are counted against properly
        #TODO: confirm caniesta bonuses are correct (add a joker and then ten point card to make caniestas)
        #TODO: confirm that red 3 penalties are correct
        
if __name__ == '__main__':
    unittest.main()
