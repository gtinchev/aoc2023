""" Description: Day 4: Scratch cards
The idea is to store the winning numbers (as they are fewer) in a dictionary, and then check the numbers in the input file against the dictionary. 
If the number is in the dictionary, then it is a winning number. Otherwise, it is not.
We then calculate the points of a card by computing the amount of winning numbers on the card and applying the formula:

floor [2 ^ (number of winning numbers - 1)]

The above formula takes care of the case where the number of winning numbers is 0, in which case the formula returns 0 points.
"""

import math
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def main():
    args = parse_arguments()
    total_points = 0

    # Use args.input_file to access the path of the input file
    with open(args.input_file, 'r') as file:
        for line in file:
            line = line.split(":")[1].strip()
            all_numbers = line.split("|")
            winning_numbers = set([int(n) for n in all_numbers[0].strip().split(" ") if n.strip() != ""]) # replace spaces where we have single digit numbers
            our_numbers = [int(n) for n in all_numbers[1].strip().split(" ") if n.strip() != ""] # replace spaces where we have single digit numbers

            total_matches = 0
            for number in our_numbers:
                if number in winning_numbers:
                    total_matches +=1

            card_points = math.floor(2 ** (total_matches - 1))

            total_points += card_points

    print(f"Total points from all cards: {total_points}")

if __name__ == "__main__":
    main()