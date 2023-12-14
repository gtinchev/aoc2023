#/usr/bin/env python3
""" Day 9: Mirage Maintenance 

Part 1: This reminds me of the traingle of differences, and that you can estimate any number on any given scale of that triangle.
But I can't remember for the life of me what the formula was.
Let's do it the naive way, and perhaps I can come up with the formula in the meantime.
"""

import argparse
import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def main():
    args = parse_arguments()

    final_sum = 0
    with open(args.input_file, "r") as file:
        for line in file:
            numbers = np.array([int(x) for x in line.strip().split()], dtype=np.int64)
            found = False
            last_digits = numbers[-1]
            while not found:
                differences = np.diff(numbers)
                last_digits += differences[-1]
                if all(x == differences[0] for x in differences):
                    found = True
                    final_sum += last_digits

                numbers = differences


    print("Final sum: {}".format(final_sum))

if __name__ == '__main__':
     main()