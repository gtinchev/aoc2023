"""Day 8: Haunted Wasteland

Part 1: The idea is to start at AAA, follow the input instructions and keep track of how many times you jumped until you reach the end of the desert (ZZZ).
If by the time you have exhausted your moves (input instructions) and you are not at ZZZ, then you repeat the instructions from the beginning.
"""

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def main():
    args = parse_arguments()

    states = {}
    
    with open(args.input_file, "r") as file:
        for line_idx, line in enumerate(file):
            line = line.strip()
            if line == "":
                continue
            if line_idx == 0:
                instructions = list(line.strip())
            else:
                state, actions = line.split("=")
                state = state.strip()
                actions = actions.strip()[1:-1].split(",")
                actions[0] = actions[0].strip()
                actions[1] = actions[1].strip()

                states[state] = actions

    num_steps = 0
    current_step = 0
    step_mapping = {
        "L": 0,
        "R": 1
    }

    # start here
    state = "AAA"
    reached_end = False
    while not reached_end:
        state = states[state][step_mapping[instructions[current_step]]]
        current_step = (current_step + 1) % len(instructions)
        num_steps += 1

        if state == "ZZZ":
            reached_end = True

    print(f"Took {num_steps} to find the end of the desert.")

if __name__ == '__main__':
     main()