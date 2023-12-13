"""Day 6:  Wait For It
The idea of this puzzle is to record the number of ways you can beat the boat race.

Part 2: You can improve the algorithm by just computing the intervals of how long you press the button for.
"""

import argparse
import math

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def calculate_num_ways(time, distance):
    """Given some time and some distance, calculate the number of ways to beat the boat.
    Time is measured in miliseconds, distance is measured in millimeters.
    If you hold the button for 1 milisecond, you will move 1 millimeter per milisecond.
    If you hold the button for 2 miliseconds, you will move 2 millimeters per milisecond and so on.
    The goal is to count how many ways you can go over the distance in the given time.

    The formula you need to use is:

    Time_holding_button * (Time - Time_holding_button) > Distance

    Where Time - Time_holding_buttong is the time the boat is moving (i.e. remaining time)

    Solving for Time_holding_button, you get:

    Time_holding_button^2 - Time_holding_button * Time + Distance < 0

    Using quadratic equation, and solving for Time_holding_button you get:

    0.5 * [ Time +/- sqrt (Time^2 - 4*Distance) ] 

    Therefore:

    0.5 * [ Time - sqrt (Time^2 - 4*Distance) ] < Time_holding_button < 0.5 * [ Time + sqrt (Time^2 - 4*Distance) ]

    Let's call that:
    A < Time_holding_button < B

    Thus you need to hold the button for at least A and at most B.

    Thus to calculate exact integers, we ceil(A) and floor(B), then count the difference B-A.

    """
    
    a = math.ceil(0.5 * (time - math.sqrt(time**2 - 4 * distance)))
    b = math.floor(0.5 * (time + math.sqrt(time**2 - 4 * distance)))

    return b - a + 1 # add 1 because we want to include the endpoints

def main():

    args = parse_arguments()

    with open(args.input_file, "r") as input_file:
        for line in input_file:
            if line.startswith("Time"):
                time = int("".join(line.strip().split()[1:]))
            elif line.startswith("Distance"):
                distance = int("".join(line.strip().split()[1:]))

    num_ways = calculate_num_ways(time, distance)

    print("Total number of ways to beat the boat: {}".format(num_ways))

if __name__ == "__main__":
    main()