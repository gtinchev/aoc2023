#/usr/bin/env python3

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def convert_line(line):
    """ Converts a line from text to digits from the left to right. Each line is a collection of words and digits with no space in-between. """
    digits_hash = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }

    converted_line = ""
    to_convert = ""

    # Iterate through each character in the line
    for character in line:

        # If the character is a digit, add it to the converted_line
        if character.isdigit():
            if to_convert != "":
                if len(to_convert) != 1:
                    converted_line += to_convert
                to_convert = ""
            converted_line += character


        # If the character is a letter, add the corresponding digit to the converted_line
        elif character.isalpha():
            character_l = character.lower()
            to_convert += character_l

            # attempt to replace the word with a digit
            for word, digit in digits_hash.items():
                if word in to_convert:
                    converted_result = to_convert.replace(word, str(digit))
                    converted_line += str(converted_result)
                    to_convert = to_convert[-1]
                    break

    return converted_line

def get_line_digits(line):
    """ Returns the first and last digit of a line."""

    # Substitute words with digits
    converted_line = convert_line(line)
    
    first_digit = None
    last_digit = None
    new_number = 0

    # Iterate through each digit in the converted_line
    for current_pointer in range(len(converted_line)):

        if converted_line[current_pointer].isdigit() and first_digit is None:
            first_digit = int(converted_line[current_pointer])

        # Find the last digit
        if converted_line[-current_pointer-1].isdigit() and last_digit is None:
            last_digit = int(converted_line[-current_pointer-1])

        # Combine and break if both digits are found
        if first_digit is not None and last_digit is not None:
            new_number = f"{first_digit}{last_digit}"
            new_number = int(new_number)
            break

    return new_number

def test_conversion():
    line = "zoneight234"
    actual_result = convert_line(line)
    expected_result = "z18234"

    assert actual_result == expected_result, f"Expected {expected_result}, got {actual_result}"

def test_line_digits():
    lines = ["zoneight234", "br7oneeight2", "2qlgkrbmnsgvmpninevjglsevenzdtmrqrnljthree", "ggvzvfzmmmvrsqghrbd3kninezrlftwonebms"]
    expected_results = [14, 72, 23, 31]

    for idx, word in enumerate(lines):
        actual_result = get_line_digits(word)
        expected_result = expected_results[idx]

        assert actual_result == expected_result, f"Expected {expected_result}, got {actual_result}"

def main():
    args = parse_arguments()

    total_sum = 0

    # Use args.input_file to access the path of the input file
    with open(args.input_file, 'r') as file:
        for line in file:
            line = line.strip()

            two_digit_number = get_line_digits(line)
            
            # Collect the sum of all digits
            total_sum += two_digit_number

    # Print the sum
    print(f"Sum of all digits: {total_sum}")

if __name__ == "__main__":
    test_conversion()
    test_line_digits()
    main()
