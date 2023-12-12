#/usr/bin/env python3

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def is_valid_symbol(text):
    """ Returns True if the given text is a valid symbol, False otherwise. """

    return text not in [".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

def get_matrix_dimensions(file):
    """ Returns the dimensions of the matrix stored in the given file. """

    num_rows = len(file.readlines())  # Count the lines in the file
    
    # Reset the file pointer to the beginning of the file
    file.seek(0)

    num_cols = len(file.readline().strip()) # Count the number of symbols in the line

    # Reset the file pointer to the beginning of the file
    file.seek(0)

    return num_rows, num_cols

def main():
    args = parse_arguments()

    total_sum = 0
    all_gears_found = {}

    # Use args.input_file to access the path of the input file
    with open(args.input_file, 'r') as file:
        num_rows, num_cols = get_matrix_dimensions(file)
        lines = file.readlines()

    prev_line = None # hold the last line, so we can easily check for symbols
    for row_idx, line in enumerate(lines):
        line = line.strip()

        digit_start = None
        digit_end = None
        number = ""
        number_added = False
        for character_idx, character in enumerate(line):
            if character.isdigit():
                number += character

                # record the start and end of the number
                if digit_start is None:
                    digit_start = character_idx

                # record the current digit as the end digit (until we see more digits)
                digit_end = character_idx

                # skip this iteration if we encountered a digit already, and it's not the end of the line
                # at the end of the line, we want to check the number
                if character_idx != num_cols - 1:
                    continue
                
            # if the current character is not a digit, but we have a number already drawn
            if digit_start is not None and digit_end is not None:
                symbols_to_check = []
                ids_to_check = [] # (r,c) for each symbol

                # record the symbols in the previous line
                if prev_line is not None:
                    for number_idx in range(digit_start, digit_end + 1):
                        if number_idx != 0:
                            symbols_to_check.append(prev_line[number_idx-1]) # top left
                            ids_to_check.append((row_idx-1, number_idx-1))

                        symbols_to_check.append(prev_line[number_idx])       # top
                        ids_to_check.append((row_idx-1, number_idx))

                        if number_idx != num_cols - 1:
                            symbols_to_check.append(prev_line[number_idx+1]) # top right
                            ids_to_check.append((row_idx-1, number_idx+1))
                
                # record the symbols in the current line
                if digit_start != 0:
                    symbols_to_check.append(line[digit_start-1]) # left
                    ids_to_check.append((row_idx, digit_start-1))
                if digit_end != num_cols - 1:
                    symbols_to_check.append(line[digit_end+1])   # right
                    ids_to_check.append((row_idx, digit_end+1))

                # record the symbols in the next line 
                if row_idx < num_rows - 1:
                    next_line = lines[row_idx + 1].strip()

                    # there will be a duplication, but for the sake of simplicity, we'll keep it
                    for number_idx in range(digit_start, digit_end + 1):
                        if number_idx != 0:
                            symbols_to_check.append(next_line[number_idx-1]) # bottom left
                            ids_to_check.append((row_idx+1, number_idx-1))

                        symbols_to_check.append(next_line[number_idx])       # bottom
                        ids_to_check.append((row_idx+1, number_idx))

                        if number_idx != num_cols - 1:
                            symbols_to_check.append(next_line[number_idx+1]) # bottom right
                            ids_to_check.append((row_idx+1, number_idx+1))

                # check for the actual symbol
                for symbol_idx, symbol in enumerate(symbols_to_check):
                    if is_valid_symbol(symbol):
                        if symbol == "*":
                            if ids_to_check[symbol_idx] not in all_gears_found:
                                all_gears_found[ids_to_check[symbol_idx]] = [int(number)]
                            else:
                                all_gears_found[ids_to_check[symbol_idx]].append(int(number))
                        total_sum += int(number)
                        number_added = True
                        break
                if not number_added:
                    print(f"Number {number} is not valid, line {row_idx}.")

                # reset the number
                digit_start = None
                digit_end = None
                number = ""
                number_added = False
            
        prev_line = line

    print(f"Total sum: {total_sum}")

    missing_gear = 0
    for gear, numbers in all_gears_found.items():
        if len(numbers) == 2:
            missing_gear += numbers[0] * numbers[1]

    print(f"Missing gear: {missing_gear}")

if __name__ == '__main__':
    main()