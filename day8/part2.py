"""Day 8: Haunted Wasteland

Part 1: The idea is to start at AAA, follow the input instructions and keep track of how many times you jumped until you reach the end of the desert (ZZZ).
If by the time you have exhausted your moves (input instructions) and you are not at ZZZ, then you repeat the instructions from the beginning.

Part 2: The idea is to simultaneously start at all nodes that end with A (e.g. XXA, YZA, etc.) and follow the input instructions.
Keep track of how many times you jumped until all processes reach end nodes, that is nodes that end with Z (e.g. XXZ, YZZ, 11Z, etc.).
To do that, we can record the number of steps needed by each process to arrive via the L and R instructions.
We can then check the lowest common multiple of all the processes to find the number of steps needed for all processes to reach their end nodes.
"""

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def find_lcm(num1, num2):
    """Find the lowest common multiple of two numbers.
    Leveraged from https://www.geeksforgeeks.org/lcm-of-given-array-elements/?ref=lbp
    """
    if(num1>num2):
        num = num1
        den = num2
    else:
        num = num2
        den = num1
    rem = num % den
    while(rem != 0):
        num = den
        den = rem
        rem = num % den
    gcd = den
    lcm = int(int(num1 * num2)/int(gcd))
    return lcm

def main():
    args = parse_arguments()

    states = {}

    starting_states = []
    ending_states = []
    
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

                if state.endswith("A"):
                    starting_states.append(state)
                elif state.endswith("Z"):
                    ending_states.append(state)

    assert len(starting_states) == len(ending_states)

    num_simultaneous_traversals = len(starting_states)

    step_mapping = {
        "L": 0,
        "R": 1
    }

    # count the number of steps needed for each process to reach the end
    num_steps_per_traversal = [0] * num_simultaneous_traversals

    # for each starting traversal
    for traversal_id in range(num_simultaneous_traversals):
        current_step = 0
        num_steps = 0

        state = starting_states[traversal_id]
        reached_end = False
        while not reached_end:
            state = states[state][step_mapping[instructions[current_step]]]
            current_step = (current_step + 1) % len(instructions)
            num_steps += 1

            if state in ending_states:
                reached_end = True

        num_steps_per_traversal[traversal_id] = num_steps

    # find the lowest common multiple of all the processes
    lcm = find_lcm(num_steps_per_traversal[0], num_steps_per_traversal[1])
    
    for i in range(2, len(num_steps_per_traversal)):
        lcm = find_lcm(lcm, num_steps_per_traversal[i])

    print(f"Took {lcm} to find the end of the desert.")

if __name__ == '__main__':
     main()