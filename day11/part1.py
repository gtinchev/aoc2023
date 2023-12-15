"""
Day 11: Cosmic Expansion

Part 1: Seems straightforward:
  1. record the location of the galaxies.
  2. detect any rows/columns that do not have any galaxies.
  3. insert a row/column above those detected in step 2.
  4. compute the number of pairs, accordinting to combinations formula:
        n! / (2! * (n-2)!)
  5. For each pair, compute the shortest distance between the two galaxies by the Pythagorean theorem, where we need to compute c:

        c = sqrt(a^2 + b^2)

    Note: It's not the Pythagoren theorem, but the Manhattan distance, since we can only travel in 4 directions, not 8.
    Thus the distance is:

    abs(a[0] - b[0]) + abs(a[1] - b[1]) 
    
    OR

    min(a, b) * 2 + max(a, b) - min(a, b)

    ---------       ---------------------
        A                     B

    Where A is the diagonal distance and B is the lateral distance.
    A is taken twice, since you need two steps in the diagonal direction to travel one step in the lateral direction.

  6. Sum the distances for all pairs.
"""

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, help="Path to the input file.")
    return parser.parse_args()

def parse_galaxies(input_file):
    """
    Parse the input file and return a list of tuples containing the coordinates of the galaxies, as well as the number of rows and columns in the universe.
    """
    galaxies = []
    num_rows = 0
    with open(input_file, "r") as file:
        for row_idx, line in enumerate(file):
            num_rows += 1
            num_cols = 0
            for col_idx, tile in enumerate(line.strip()):
                if tile == "#":
                    galaxies.append((row_idx, col_idx))
                num_cols += 1
        
    return galaxies, num_rows, num_cols

def expand_galaxies(galaxies, empty_rows, empty_cols):
    result = []
    for galaxy in galaxies:
        row, col = galaxy
        row_increment, col_increment = 0, 0
        for empty_row in empty_rows:
            if row >= empty_row:
                row_increment += 1
        for empty_col in empty_cols:
            if col >= empty_col:
                col_increment += 1
        result.append((row+row_increment, col+col_increment))

    return result

def test_expansion():
    galaxies = [(0, 3), (1, 7), (2, 0), (4, 6), (5, 1), (6, 9), (8, 7), (9, 0), (9, 4)]
    expected_galaxies = [(0, 4), (1, 9), (2, 0), (5, 8), (6, 1), (7, 12), (10, 9), (11, 0), (11, 5)]

    computed_galaxies = expand_galaxies(galaxies, [3,7], [2, 5, 8])

    assert computed_galaxies == expected_galaxies

def main():
    args = parse_arguments()

    # 0. Parse the input file as galaxies
    galaxies, num_rows, num_cols = parse_galaxies(args.input_file)

    # 1. Detect rows/columns that do not have any galaxies.
    empty_rows = []
    empty_cols = []
    for row_idx in range(num_rows):
        if not any(galaxy[0] == row_idx for galaxy in galaxies):
            empty_rows.append(row_idx)

    for col_idx in range(num_cols):
        if not any(galaxy[1] == col_idx for galaxy in galaxies):
            empty_cols.append(col_idx)

    print(f"Empty rows: {empty_rows}")
    print(f"Empty cols: {empty_cols}")

    num_rows += len(empty_rows)
    num_cols += len(empty_cols)

    # 2. Increment the ids of the rows/columns that are larger than the empty rows/columns.
    expanded_galaxies = expand_galaxies(galaxies, empty_rows, empty_cols)

    # 3. Compute the distance
    total_distance = 0
    for galaxy_idx in range(len(expanded_galaxies)):
        galaxy = expanded_galaxies[galaxy_idx]
        for other_galaxy_idx in range(galaxy_idx + 1, len(expanded_galaxies)):
            other_galaxy = expanded_galaxies[other_galaxy_idx]
            # (2, 0) and (7, 12) -> distance: 17
            # (0, 4) and (7, 12) -> distance: 15
            a = abs(galaxy[0] - other_galaxy[0])
            b = abs(galaxy[1] - other_galaxy[1])
            # Since it takes 2 steps to travel diagonally, we need to account for that
            diagonal_steps = min(a, b) * 2 # shortest distance is either going to cols or rows, whichever is smaller
            lateral_steps = max(a, b) - min(a, b) # the remaining distance is lateral
            distance = diagonal_steps + lateral_steps
            total_distance += distance
            # print(f"Galaxy: {galaxy}, Other galaxy: {other_galaxy}, Distance: {distance}")
            
    print(f"Total distance: {total_distance}")

if __name__ == "__main__":
    test_expansion()
    print("Successfully passed expansion unit test.")
    main()