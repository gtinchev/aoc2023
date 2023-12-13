"""Day 7: Camel Cards

Part 1: We are given a list of poker hands, each consisting of with 5 cards, as well as the bid amount of each hand. 
We need to calculate the strength of the hands.
"""

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def calculate_strength(hand):
    """ Calculate the strength of a hand, which is the number of unique cards in the hand"""
    initial_guess = len(set(hand))

    # now based of the initial guess - we sometimes need to adjust the strength
    # if the initial guess is 1, then we know it's five of a kind
    if initial_guess == 1:
        return 1
    # if the initial guess is 2, then we know it's either four of a kind or a full house
    if initial_guess == 2:
        for card in set(hand):
            if hand.count(card) == 4 or hand.count(card) == 1:
                return 2
            else:
                return 3
    # if the initial guess is 3, then we know it's either three of a kind or two pair
    if initial_guess == 3:
        for card in set(hand):
            if hand.count(card) == 3:
                return 4
            elif hand.count(card) == 2:
                return 5
    # if the initial guess is 4, then we know it's either one pair
    if initial_guess == 4:
        return 6
    # if the initial guess is 5, then we know it's a high card
    if initial_guess == 5:
        return 7
    
def test_calculate_strength():
    cards = ["KKKKK", "KKKKQ", "JJK82", "JJKKT", "AK248", "AAA72", "77788"]
    expected_strength = [1, 2, 6, 5, 7, 4, 3]

    for card, strength in zip(cards, expected_strength):
        assert calculate_strength(card) == strength

def calc_num_hands(input_file):
    """ Calculate how many hands we have, which is equal to the number of lines in our input file """
    with open(input_file, "r") as input_file:
        return len(input_file.readlines())

def sort_by_first_letter(keys):
    """Ordering the hands by the first letter of the hand, where A is the strongest and 2 is the weakest"""
    hierarchy = {'A': 13, 'K': 12, 'Q': 11, 'J': 10, 'T': 9, '9': 8, '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}
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