from common.Card import Card

"""This file contains methods used in processing runs for Liverpool.

Some Liverpool specific stuff:
it assumes that Aces can be Hi or Low but not both (K,A,2 not allowed).
Enforces rule that you must have two natural cards between wilds in a run.

In order to preserve backwards compatibility with June 2020 distribution, it assumes that card.tempnumber is
not passed back and forth between the client and server. This only causes ambiguity in wilds and 
Aces at the ends of runs.   Method restoreRunAssignment takes care of this by assigning
wilds and Aces on ends of runs the appropriate tempnumber before processRuns is called.
To preserve info on whether Ace is assigned hi or low, if Ace is assigned low, then tempnumber is set to -1.
"""

def processRuns(card_group, wild_numbers):
    """ handle sorting of run, including placement of wilds.  Handles minor rule checking.

    # processRuns does not presume length requirement or that all cards are in same suit.
    # it DOES presume that if Aces are not wild, then they are hi or low, but not both.
    # IF ACE CAN BE HIGH OR LOW (very unusual) THAN AUTOMATICALLY MAKING IT LOW.
    """
    # print("in RunManagement, processRuns")
    # print(card_group)
    card_group.sort(key=lambda wc: wc.tempnumber)
    # print(card_group)
    first_card = True
    groups_wilds = []
    temp_run_group = []
    aces_list =[]
    gap_flag = False
    for card in card_group:                    # separate unassigned wilds and Aces from rest of run.
        # pull out wilds that have not been assigned (do this before Aces, in case rules changed so that Aces are wild).
        if card.tempnumber in wild_numbers:
            groups_wilds.append(card)
            # pull out Aces that have not been assigned hi or low, but don't pull out Wilds assigned to low Ace slot.
        elif card.tempnumber == 1 and card.number == 1:
            aces_list.append(card)
        else:
            temp_run_group.append(card)
    card_group  = []                         # rebuild card_group below
    for card in temp_run_group:
        if first_card:
            first_card = False
            card_group.append(card)
        else:
            abs_temp_number = abs(card_group[-1].tempnumber)  # Aces designated to be low have tempnumber = -1.
            if card.tempnumber == (abs_temp_number + 1):
                card_group.append(card)
            elif card.tempnumber == (abs_temp_number + 2) and len(groups_wilds) > 0:
                this_wild = groups_wilds.pop(0)
                this_wild.tempnumber = abs_temp_number + 1
                card_group.append(this_wild)
                card_group.append(card)
            elif card.tempnumber == abs_temp_number:
                if isWild(card, wild_numbers):
                    card.tempnumber = card.number  # reset Wild card back to original value (0 for Jokers)
                    groups_wilds.append(card)
                elif isWild(card_group[-1], wild_numbers):
                    this_wild = card_group.pop(-1)
                    this_wild.tempnumber = this_wild.number
                    groups_wilds.append(this_wild)
                    card_group.append(card)
                else:
                    raise Exception('Card value already in the run.')
            elif card.tempnumber > (abs_temp_number + 2):
                raise Exception('too big a gap between numbers')
            else:
                # gap must be 1 card. It's possible to free up a wild later in run then gap of 1 can be closed.
                gap_flag =True
    if gap_flag and len(groups_wilds) > 0:
        temp_run_group = card_group
        card_group = []
        card_group.append(temp_run_group[0])
        for indx in range(len(temp_run_group)-1):
            card = temp_run_group[indx+1]
            if temp_run_group[indx].tempnumber == card.tempnumber + 1:
                card_group.append(card)
            elif temp_run_group[indx].tempnumber == card.tempnumber + 2:
                if len(groups_wilds) > 0:
                    this_wild.pop(groups_wilds[0])
                    card_group.append(this_wild)
                    card_group.append(card)
                else:
                    raise Exception('too big a gap between numbers')

    #  Review note - Handle Aces after other cards, else ran into problem when wanted Ace, Joker, 3...
    # Rare for Ace Hi and Ace low to both be options. If they are, does it make a difference which one they are?
    # If run is A?,2,Wild,4...J,Q,K,A? then it does (wild could still be played above King, but not below 2).
    if len(aces_list) > 0:
        if len(aces_list) > 2:
            raise Exception('Cannot play more than 2 Aces in a single run.')
        # Possible Ace(s) replacing a wild card with tempnumber 13 or -1.
        # If have wild in Ace slot then remove it from run.  It will be placed back in run after Aces placed.
        if isWild(card_group[0], wild_numbers) and abs(card_group[0].tempnumber) == 1:
            this_wild = card_group.pop(0)
            groups_wilds.append(this_wild)
        if isWild(card_group[-1], wild_numbers) and card_group[-1].tempnumber == 13:
            this_wild = card_group.pop(-1)
            groups_wilds.append(this_wild)
        # Can Ace go high but not low?
        if card_group[-1].tempnumber == 13 and not card_group[0].tempnumber == 2:
            this_ace = aces_list.pop(0)
            this_ace.tempnumber = 14
            card_group.append(this_ace)
            # Can Ace go low but not high?
        elif not card_group[-1].tempnumber == 13 and card_group[0].tempnumber == 2:
            this_ace = aces_list.pop(0)
            this_ace.tempnumber = -1
            card_group.insert(0, this_ace)
        elif card_group[-1].tempnumber == 13 and card_group[0].tempnumber == 2:
            if len(aces_list) == 1:
                print("IF ACE CAN BE HIGH OR LOW THAN AUTOMATICALLY MAKING IT LOW, RATHER THAN HANDLING CORNER CASE.")
                this_ace = aces_list.pop(0)
                this_ace.tempnumber = -1
                card_group.insert(0, this_ace)
            elif len(aces_list) == 2:
                this_ace = aces_list.pop(0)
                this_ace.tempnumber = -1
                card_group.insert(0, this_ace)
                this_ace = aces_list.pop(0)
                this_ace.tempnumber = 14
                card_group.append(0, this_ace)
    if len(aces_list) > 0 and len(groups_wilds) > 0:
        # Can Aces that previously could not be played now be played?
        if len(aces_list) == 2:
            if len(groups_wilds) >= 2 and card_group[0].tempnumber == 3 and card_group[-1].tempnumber == 12:
                this_wild = groups_wilds.pop(0)
                this_wild.tempnumber = 2
                card_group.insert(0, this_wild)
                aces_list[0].tempnumber = -1
                card_group.insert(0, aces_list[0])
                this_wild = groups_wilds.pop(0)
                this_wild.tempnumber = 13
                card_group.append(this_wild)
                aces_list[1].tempnumber = 14
                card_group.append(aces_list[1])
                aces_list = []
                # will check that don't have jokers too close together later.
        elif len(aces_list) == 1:
            if card_group[0].tempnumber == 3 and not isWild(card_group[0], wild_numbers) \
                    and not isWild(card_group[1], wild_numbers):
                this_wild = groups_wilds.pop(0)
                this_wild.tempnumber = 2
                card_group.insert(0, this_wild)
                aces_list[0].tempnumber = -1
                card_group.insert(0, aces_list[0])
                aces_list = []
            elif card_group[-1].tempnumber == 12 and not isWild(card_group[-1], wild_numbers) \
                    and not isWild(card_group[-2], wild_numbers):
                this_wild = groups_wilds.pop(-1)
                this_wild.tempnumber = 13
                card_group.append(this_wild)
                aces_list[0].tempnumber = 14
                card_group.append(aces_list[0])
                aces_list = []
    if len(aces_list) > 0:
        raise Exception('Ace cannot be played')
   # Calculate if wild cards can be played  - only possible remaining slots for wilds are at the ends of the current run.
    num_remaining_wilds = len(groups_wilds)
    possible_wild_assignments = []
    if not num_remaining_wilds == 0:
        # are there options on where to assign wilds?
        if num_remaining_wilds > 2:
            raise Exception('You cannot play all the wild cards.')
        if card_group[0].tempnumber > 1 and not isWild(card_group[0], wild_numbers) \
                and not isWild(card_group[1], wild_numbers):
            runslot = card_group[0].tempnumber - 1
            possible_wild_assignments.append(runslot)
        if card_group[-1].tempnumber < 14 and not isWild(card_group[-1], wild_numbers) \
                and not isWild(card_group[-2], wild_numbers):
            runslot = card_group[-1].tempnumber + 1
            possible_wild_assignments.append(runslot)
        # Can wilds be played?
        if num_remaining_wilds > len(possible_wild_assignments):
            raise Exception('you cannot play all the wild cards.')
        num_remaining_wilds = len(groups_wilds)
        # Can wilds be automatically played?
        if num_remaining_wilds == 2:
            groups_wilds[0].tempnumber = possible_wild_assignments[0]
            groups_wilds[1].tempnumber = possible_wild_assignments[1]
            card_group.insert(0, groups_wilds[0])
            card_group.append(groups_wilds[1])
            groups_wilds=[]
            possible_wild_assignments=[]
        elif num_remaining_wilds == 1 and len(possible_wild_assignments) == 1:
            groups_wilds[0].tempnumber = possible_wild_assignments[0]
            if possible_wild_assignments[0] < card_group[0].tempnumber:
                card_group.insert(0, groups_wilds[0])
            else:
                card_group.append(groups_wilds[0])
            groups_wilds=[]
            possible_wild_assignments=[]
        num_remaining_wilds = len(groups_wilds)
        if num_remaining_wilds == 0:
            possible_wild_assignments = []
        # if num_remaining_wilds == 1 and len(possible_wild_assignments) == 2:
        # Will need to ask player whether to play high or low, controller handles that.
    # Final rules check in processRuns: double check that wilds are not placed too close together.
    # (Note that in creating possible_wild_assignments checked that assignments won't violate this rule, but didn't
    # check this everywhere).
    last_card_wild = False
    second2last_card_wild = False
    for card in card_group:
        if (isWild(card, wild_numbers) and last_card_wild) or (isWild(card, wild_numbers) and second2last_card_wild):
            raise Exception('Must have two natural cards between wild cards in runs')
        second2last_card_wild = last_card_wild
        last_card_wild = isWild(card, wild_numbers)
    return card_group, possible_wild_assignments, groups_wilds

def restoreRunAssignment(visible_scards_dictionary, wild_numbers, numsets):
    """ Convert scards to cards and assign values to Wild cards and Aces in runs from server.

    Needed to maintain integrity of Wilds' assigned values in runs.  Server does not know tempnumbers
    (for backwards compatability not changing json between server and client).
    There's no ambiguity except for wilds and Aces at the ends of the run (processRuns handles wilds in middle).
    """

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
        if k_group[1] >= numsets and len(card_group) > 1:       # check if this is a run.
            if card_group[-1].number in wild_numbers:    # reset tempnumber for Wilds/Aces if they are at the end.
                card_group[-1].assignWild(card_group[-2].tempnumber + 1)
            elif card_group[-1].number == 1:
                card_group[-1].assignWild(14)
            if card_group[0].number in wild_numbers:    # reset tempnumber for wild cards if they are at the beginning.
                card_group[0].assignWild(card_group[1].tempnumber - 1)
            # todo: be sure to preserve this in documentation.  If Ace is assigned low, then tempnumber is -1.
            elif card_group[0].number == 1:
                card_group[0].tempnumber = -1
        return cardgroup_dictionary


def isWild(card, wild_numbers):
    """returns true if a card is a wild"""

    # Review question -- Currently the methods in this file import minimal amount, and assume variables are passed
    # through and returned. Would it be better to import liverpool ruleset (including wild_numbers and method isWild).
    if card.number in wild_numbers:
        return True
    else:
        return False