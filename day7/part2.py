"""Day 7: Camel Cards

Part 1: We are given a list of poker hands, each consisting of with 5 cards, as well as the bid amount of each hand. 
We need to calculate the strength of the hands.

Part 2: Now we need to consider the case where the J can be any other card (lots of if statements)
In addition, it's weaker than 2 when ordering it.
"""

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def calculate_strength(hand):
    """ Calculate the strength of a hand, which is the number of unique cards in the hand"""
    initial_guess = len(set(hand))

    actual_strength = None

    # now based of the initial guess - we sometimes need to adjust the strength
    # if the initial guess is 1, then we know it's five of a kind
    if initial_guess == 1:
        actual_strength = 1
    # if the initial guess is 2, then we know it's either four of a kind or a full house
    elif initial_guess == 2:
        for card in set(hand):
            if hand.count(card) == 4 or hand.count(card) == 1:
                actual_strength = 2
                if "J" in hand:
                    actual_strength = 1
            else:
                actual_strength = 3
                if "J" in hand:
                    actual_strength = 1
    # if the initial guess is 3, then we know it's either three of a kind or two pair
    elif initial_guess == 3:
        for card in set(hand):
            if hand.count(card) == 3:
                actual_strength = 4
                if "J" in hand:
                    actual_strength = 2
            elif hand.count(card) == 2:
                actual_strength = 5
                if "J" in hand:
                    actual_strength -= (hand.count("J")+1)
    # if the initial guess is 4, then we know it's one pair
    elif initial_guess == 4:
        actual_strength = 6
        if "J" in hand:    
            actual_strength = 4 # always will have 3 of a kind if J is in the hand, regardless of whether it's the J that's the pair or not
    # if the initial guess is 5, then we know it's a high card
    elif initial_guess == 5:
        actual_strength = 7
        if "J" in hand:
            actual_strength = 6

    return actual_strength
    
def test_calculate_strength():
    cards = ["KKKKK", "KKKKQ", "JJK82", "JJKKT", "AK248", "AAA72", "77788"]
    expected_strength = [1, 2, 4, 2, 7, 4, 3]   

    for card, strength in zip(cards, expected_strength):
        assert calculate_strength(card) == strength

def calc_num_hands(input_file):
    """ Calculate how many hands we have, which is equal to the number of lines in our input file """
    with open(input_file, "r") as input_file:
        return len(input_file.readlines())

def sort_by_first_letter(keys):
    """Ordering the hands by the first letter of the hand, where A is the strongest and J is the weakest"""
    hierarchy = {'A': 13, 'K': 12, 'Q': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1}
    return sorted(keys, key=lambda x: [hierarchy[char] for char in x], reverse=True)

def main():

    args = parse_arguments()

    num_hands = calc_num_hands(args.input_file)

    # store the hands in a dictionary, where the key is the strength, and the value are the actual cards
    strength_order = {
        1: [], # 5 of a kind
        2: [], # 4 of a kind
        3: [], # full house
        4: [], # 3 of a kind
        5: [], # 2 pairs
        6: [], # 1 pair
        7: []  # high card
    }

    # holds how much each hand bids - key is the hand, value is the bid
    hands_bids = {}

    # now we need to order the hands from strongest to weakest
    with open(args.input_file, "r") as input_file:
        for line in input_file:
            hand, bid = line.strip().split(" ")
            strength = calculate_strength(hand)
            hands_bids[hand] = int(bid.strip())
            strength_order[strength].append(hand)

    # now we need to order the hands in terms of strength
    for strength, hands in strength_order.items():
        strength_order[strength] = sort_by_first_letter(hands)  # Use custom_sort method to sort each list

    # now we can calculate the total winnings
    total_winnings = 0
    for strength, hands in strength_order.items():
        for hand in hands:
            total_winnings += hands_bids[hand] * num_hands
            num_hands -= 1
        
    print(f"Total winnings: {total_winnings}")

if __name__ == "__main__":
    test_calculate_strength()
    print(f"Calculating strength test passed!")
    main()