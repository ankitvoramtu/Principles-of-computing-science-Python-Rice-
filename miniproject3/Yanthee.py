"""
Planner for Yahtzee
"""

"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set



def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    counted_item = []
    hand_score = []
    if len(hand) == 0:
        return 0
    else:
        for item in hand:
            if item not in counted_item:
                counted_item.append(item)
                hand_score.append(item * hand.count(item))
        return max(hand_score)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = [dummy_i + 1 for dummy_i in range(num_die_sides)]
    free_dice = gen_all_sequences(outcomes, num_free_dice)
    all_dice = [list(held_dice) + list(dummy_dice) for dummy_dice in free_dice]
    return sum([score(dummy_dice) for dummy_dice in all_dice])*1.0/len(free_dice)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    repeated_set = []    
    sub_hands = []
    for dummy_i in range(len(hand) + 1):
       sub_hands += gen_all_sequences(hand,dummy_i)
    sub_answer = list(set([tuple(sorted(item)) for item in sub_hands]))
    for dummy_n in hand:
        for dummy_j in sub_answer:
            if hand.count(dummy_n) < dummy_j.count(dummy_n):
                repeated_set.append(dummy_j)
    for item in repeated_set:
        if item in sub_answer:
            sub_answer.remove(item)
    return set(sub_answer)



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_hold = list(gen_all_holds(hand))
    maxi_exp_val = 0
    print all_hold
    for hold in all_hold:
        if expected_value(hold, num_die_sides, len(hand) - len(hold)) >= maxi_exp_val:
            maxi_exp_val = expected_value(hold, num_die_sides, len(hand) - len(hold))
            maxi_hold = hold
    print maxi_exp_val, maxi_hold
    return (maxi_exp_val, maxi_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

"""
Test suite for gen_all_holds in "Yahtzee"
"""


    
    
    



