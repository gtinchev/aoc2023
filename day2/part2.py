#/usr/bin/env python3

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def get_max_per_game(line):
    """ Returns the maximum number of cubes in this game given a line. """

    all_cube_numbers = {
        "red": 0,
        "green": 0,
        "blue": 0
    }
    iterations = line.split(";")
    for iteration in iterations:
        cubes = iteration.split(",")
        for cube in cubes:
            number, color = cube.strip().split(" ")
            if color in all_cube_numbers:
                all_cube_numbers[color] = max(all_cube_numbers[color], int(number))

    return all_cube_numbers

def test_get_max_per_game():
    game = "4 blue, 4 red, 16 green; 14 green, 5 red; 1 blue, 3 red, 5 green"
    expected_result = {
        "red": 5,
        "green": 16,
        "blue": 4
    }
    actual_result = get_max_per_game(game)

    assert expected_result == actual_result

def parse_game_id(line):
    """ Returns the game id given a line. """

    return int(line.split(":")[0].strip().split(" ")[1])

def main():
    args = parse_arguments()
    max_cubes = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    possible_games_sum = 0

    # Use args.input_file to access the path of the input file
    with open(args.input_file, 'r') as file:
        for line in file:
            line = line.strip()

            game_id = parse_game_id(line)

            line_with_cubes_only = line.split(":")[1].strip()
            get_number_of_cubes = get_max_per_game(line_with_cubes_only)

            total_cubes_per_game = get_number_of_cubes["red"] * get_number_of_cubes["green"] * get_number_of_cubes["blue"]

            possible_games_sum += total_cubes_per_game

            # if get_number_of_cubes["red"] <= max_cubes["red"] and get_number_of_cubes["green"] <= max_cubes["green"] and get_number_of_cubes["blue"] <= max_cubes["blue"]:
            #     possible_games_sum += game_id
            # else:
            #     continue

    print(f"Sum of max possible red*green*blue games: {possible_games_sum}")

if __name__ == "__main__":
    main()