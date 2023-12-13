""" Description: Day 4: Scratch cards, Part 2
The idea is to store the winning numbers (as they are fewer) in a dictionary, and then check the numbers in the input file against the dictionary. 
If the number is in the dictionary, then it is a winning number. Otherwise, it is not.
We create a dictionary where the keys are the cards the values are the number of instances.
Crucially, we need to multiply the values by the number of instances of the card that we are processing, since we need to account for the fact that we can have multiple instances of the same card.
We then sum the number of instances to get the total number of scratch cards.
"""

import math
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def get_number_of_cards(input_file):
    """ Returns the number of lines in the file as how many cards there are """

    with open(input_file, 'r') as file:
        return len(file.readlines())

def main():
    args = parse_arguments()

    num_cards = get_number_of_cards(args.input_file)
    card_instances = {}
    for i in range(1, num_cards+1):
        card_instances[i] = 1 # as we process each one of them at least one

    # At this point, we need to count how many instances we have in each card
    with open(args.input_file, 'r') as file:
        for line in file:
            card_idx, line = line.strip().split(":")
            card_idx = int(card_idx.split()[1].strip())
            line = line.strip()
            all_numbers = line.split("|")
            winning_numbers = set([int(n) for n in all_numbers[0].strip().split(" ") if n.strip() != ""]) # replace spaces where we have single digit numbers
            our_numbers = [int(n) for n in all_numbers[1].strip().split(" ") if n.strip() != ""] # replace spaces where we have single digit numbers

            total_matches = 0
            for number in our_numbers:
                if number in winning_numbers:
                    total_matches +=1

            for next_card_idx in range(1, total_matches+1):
                card_instances[card_idx+next_card_idx] += (1 * card_instances[card_idx])

    total_scratch_cards = 0
    for card_idx, num_instances in card_instances.items():
        total_scratch_cards += num_instances

    print(f"Total number of scratch cards: {total_scratch_cards}")

if __name__ == "__main__":
    main()