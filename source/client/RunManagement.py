from common.Card import Card

# This file contains methods used in processing runs for Liverpool or other Rummy games.

def processRuns(card_group, wild_numbers):
    """ handle sorting of run, including placement of wilds.  Handles minor rule checking.

    processRuns does not check length requirement or that all cards are in same suit.
    it DOES:
          require that if Aces are not wild, then they are hi or low, but not both.
          require that there must be two naturals between wild cards in runs.
    To preserve info on whether Ace is assigned hi or low, if Ace is assigned low, then tempnumber is set to -1.
    IF ACE CAN BE HIGH OR LOW (very unusual) THAN AUTOMATICALLY MAKING IT LOW.
    """
    # sort card_group by tempnumber and initialize variables.
    card_group.sort(key=lambda wc: wc.tempnumber)
    groups_wilds = []
    temp_run_group = []
    aces_list =[]
    # Separate wilds & Aces that have NOT been assigned from other cards (do wilds before Aces in case Aces are wild).
    for card in card_group:
        if card.tempnumber in wild_numbers:
            groups_wilds.append(card)
        elif card.tempnumber == 1 and card.number == 1:
            aces_list.append(card)
        else:
            temp_run_group.append(card)
    # first pass on run -- check sequence and place or remove wilds.
    card_group, groups_wilds, gap_flag = buildBaseRun(temp_run_group, groups_wilds, wild_numbers)
    # Check if new Aces will free up additional wild cards.
    if len(aces_list) > 0:
        card_group, groups_wilds = acesFreeWilds(card_group, groups_wilds, wild_numbers)
    # second pass on run -- if there were any gaps, see if wilds can fill them in.
    if gap_flag:
        if len(groups_wilds) > 0:
            card_group, groups_wilds = fillGaps(card_group, groups_wilds)
        else:
            text = 'There is a gap between numbers in run beginning with ' + str(card_group[0])
            raise Exception(text)
    # Now assign Aces that were not previously assigned (Aces cannot be moved once assigned).
    if len(aces_list) > 2:
        raise Exception('Cannot play more than 2 Aces in a single run.')
    # Aces can go high or low.  If single Ace can be played in either location (rare) then play it Low.
    elif len(aces_list) > 0:
        lowAceOK = lowAceChk(card_group, groups_wilds, wild_numbers)
        hiAceOK =  hiAceChk(card_group, groups_wilds, wild_numbers)
        if len(aces_list) == 1:
            if hiAceOK and not lowAceOK:
                card_group, groups_wilds, aces_list = appendAce(card_group, groups_wilds, aces_list)
            elif lowAceOK:
                card_group, groups_wilds, aces_list = insertAce(card_group, groups_wilds, aces_list)
            else:
                text = 'Cannot play ' + str(aces_list[0])
                raise Exception(text)
        if len(aces_list) == 2:
            if hiAceOK and lowAceOK:
                card_group, groups_wilds, aces_list = appendAce(card_group, groups_wilds, aces_list)
                card_group, groups_wilds, aces_list = insertAce(card_group, groups_wilds, aces_list)
            else:
                text = 'Cannot play ' + str(aces_list[0])
                raise Exception(text)
   # Check if wild cards can be played  - only possible remaining slots for wilds are at the ends of the current run.
    num_remaining_wilds = len(groups_wilds)
    possible_wild_assignments = []
    if not num_remaining_wilds == 0:
        # are there options on where to assign wilds?
        if num_remaining_wilds > 2:
            raise Exception('You cannot play all the wild cards.')
        if lowWildChk(card_group, wild_numbers):
            runslot = card_group[0].tempnumber - 1
            possible_wild_assignments.append(runslot)
        if hiWildChk(card_group, wild_numbers):
            runslot = card_group[-1].tempnumber + 1
            possible_wild_assignments.append(runslot)
        # If wilds can be automatically assigned, do it.
        if num_remaining_wilds > len(possible_wild_assignments):
            raise Exception('you cannot play all the wild cards.')
        if num_remaining_wilds == len(possible_wild_assignments):
            for this_wild in groups_wilds:
                this_wild.tempnumber = possible_wild_assignments.pop(0)
                card_group.append(this_wild)
            card_group.sort(key=lambda wc: wc.tempnumber)
            groups_wilds=[]
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
            if card_group[0].number in wild_numbers:
                card_group[0].assignWild(card_group[1].tempnumber - 1)
            elif card_group[0].number == 1:
                card_group[0].assignWild(-1)
    return cardgroup_dictionary


def isWild(card, wild_numbers):
    """returns true if a card is a wild"""
    if card.number in wild_numbers:
        return True
    else:
        return False

def buildBaseRun(temp_run_group, groups_wilds, wild_numbers):
    # check sequence of cards, free-up and place wild cards as necesseary.
    # if there's a gap of 1 set gapflag to True (may free up wilds later to fill such a gap).
    card_group  = []                         # rebuild card_group below
    first_card = True
    gap_flag = False
    for card in temp_run_group:
        if first_card:
            first_card = False
            card_group.append(card)
        else:
            abs_temp_number = abs(card_group[-1].tempnumber)  # Aces designated to be low have tempnumber = -1.
            if card.tempnumber == (abs_temp_number + 1):
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
            elif card.tempnumber == (abs_temp_number + 2):
                if len(groups_wilds) == 0:
                    # wild cards might be freed up later.  Will check again later.
                    gap_flag = True
                    card_group.append(card)
                else:
                    this_wild = groups_wilds.pop(0)
                    this_wild.tempnumber = abs_temp_number + 1
                    card_group.append(this_wild)
                    card_group.append(card)
            else:
                text = 'There is a too big a gap between numbers in run with ' + str(card_group[0])
                raise Exception(text)
    return card_group, groups_wilds, gap_flag

def acesFreeWilds(card_group, groups_wilds, wild_numbers):
    # If wild cards are in Aces slot, then free slot and move wilds to groups_wilds.
    if isWild(card_group[0], wild_numbers) and abs(card_group[0].tempnumber) == 1:
        this_wild = card_group.pop(0)
        this_wild.tempnumber = this_wild.number
        groups_wilds.append(this_wild)
    if isWild(card_group[-1], wild_numbers) and card_group[-1].tempnumber == 14:
        this_wild = card_group.pop(-1)
        this_wild.tempnumber = this_wild.number
        groups_wilds.append(this_wild)
    return card_group, groups_wilds

def fillGaps(temp_run_group, groups_wilds):
    # fill in any remaining gaps in run with wild cards, or raise exception.
    card_group = []  # rebuild card_group below
    first_card = True
    for card in temp_run_group:
        if first_card:
            first_card = False
            card_group.append(card)
        else:
            abs_temp_number = abs(card_group[-1].tempnumber)  # Aces designated to be low have tempnumber = -1.
            if card.tempnumber == (abs_temp_number + 1):
                card_group.append(card)
            elif card.tempnumber == (abs_temp_number + 2):
                if len(groups_wilds) > 0:
                    this_wild = groups_wilds.pop(0)
                    this_wild.tempnumber = abs_temp_number + 1
                    card_group.append(this_wild)
                    card_group.append(card)
                else:
                    text = 'Not enough wilds: there is a gap between' \
                           + str(card_group[-1]) + ' and ' + str(card)
                    raise Exception(text)
    return card_group, groups_wilds

def lowWildChk(card_group, wild_numbers):
    if card_group[0].tempnumber > 1 and not isWild(card_group[0], wild_numbers) \
            and not isWild(card_group[1], wild_numbers):
        return True
    else:
        return False

def hiWildChk(card_group, wild_numbers):
    if card_group[-1].tempnumber < 14 and not isWild(card_group[-1], wild_numbers) \
            and not isWild(card_group[-2], wild_numbers):
        return True
    else:
        return False

def lowAceChk(card_group, groups_wilds, wild_numbers):
    if card_group[0].tempnumber == 2:
        return True
    elif card_group[0].tempnumber == 3 and len(groups_wilds) > 0 and lowWildChk(card_group, wild_numbers):
        return True
    else:
        return False

def hiAceChk(card_group, groups_wilds, wild_numbers):
    if card_group[-1].tempnumber == 13:
        return True
    elif card_group[-1].tempnumber == 12 and len(groups_wilds) > 0 and hiWildChk(card_group, wild_numbers):
        return True
    else:
        return False

def appendAce(card_group, groups_wilds, aces_list):
    if not card_group[-1].tempnumber == 13:
        this_wild = groups_wilds.pop(0)
        this_wild.tempnumber == 13
        card_group.append(this_wild)
    this_ace = aces_list.pop(0)
    this_ace.tempnumber = 14
    card_group.append(this_ace)
    return card_group, groups_wilds, aces_list

def insertAce(card_group, groups_wilds, aces_list):
    if not card_group[0].tempnumber == 2:
        this_wild = groups_wilds.pop(0)
        this_wild.tempnumber == 2
        card_group.insert(0, this_wild)
    this_ace = aces_list.pop(0)
    this_ace.tempnumber = -1
    card_group.insert(0, this_ace)
    return card_group, groups_wilds, aces_list
