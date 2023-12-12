#/usr/bin/env python3

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def main():
    args = parse_arguments()

    total_sum = 0

    # Use args.input_file to access the path of the input file
    with open(args.input_file, 'r') as file:
        for line in file:
            line = line.strip()
            first_digit = None
            last_digit = None
            new_number = 0

            # Iterate through each digit in the line
            for current_pointer in range(len(line)):

                if line[current_pointer].isdigit() and first_digit is None:
                    first_digit = int(line[current_pointer])

                # Find the last digit
                if line[-current_pointer-1].isdigit() and last_digit is None:
                    last_digit = int(line[-current_pointer-1])

                # Combine and break if both digits are found
                if first_digit is not None and last_digit is not None:
                    new_number = f"{first_digit}{last_digit}"
                    new_number = int(new_number)
                    break
            
            # Collect the sum of all digits
            total_sum += new_number

    # Print the sum
    print(f"Sum of all digits: {total_sum}")

if __name__ == "__main__":
    main()
