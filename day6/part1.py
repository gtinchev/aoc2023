"""Day 6:  Wait For It
The idea of this puzzle is to record the number of ways you can beat the boat race.
"""

import argparse

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
    """
    
    num_ways = 0

    for t in range(time):
        hold_for = t
        speed = hold_for
        distance_covered = speed * (time - hold_for)
        if distance_covered > distance:
            num_ways += 1

    return num_ways

def main():

    args = parse_arguments()

    times = []
    distances = []

    with open(args.input_file, "r") as input_file:
        for line in input_file:
            if line.startswith("Time"):
                times = [int(n) for n in line.strip().split()[1:] if n.isdigit()]
            elif line.startswith("Distance"):
                distances = [int(n) for n in line.strip().split()[1:] if n.isdigit()]

    assert len(times) == len(distances), "Times and distances need to be the same length"
    
    total_ways = 1
    for time, distance in zip(times, distances):
        num_ways = calculate_num_ways(time, distance)
        total_ways *= num_ways

    print("Total number of ways to beat the boat: {}".format(total_ways))
        


if __name__ == "__main__":
    main()