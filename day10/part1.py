"""Day 10: Pipe Maze

This looks like edges on a graph.
The solution seems straightforward, record each state as (r,c, tile) in a matrix.
We then find the START tile and start traversing the graph by counting the number of edges it's connected to.
It can only be orthogonally connected to 2 other tiles, so we can use that to find the next tile.

Part 1:
The idea is to traverse starrting from the S tile, in two possible directions.
When you traverse save the distance in a separate dictionary.
At every tile you always have 2 possible directions to move - one explored, where you have the distance, and one unexplored where distance is infinity.
You continue until you reach a point of explored distance - that's your last tile.
"""

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def create_maze(file):
    """Create a maze from the input file.
    Tiles can be:
        | is a vertical pipe connecting north and south.
        - is a horizontal pipe connecting east and west.
        L is a 90-degree bend connecting north and east.
        J is a 90-degree bend connecting north and west.
        7 is a 90-degree bend connecting south and west.
        F is a 90-degree bend connecting south and east.
        . is ground; there is no pipe in this tile.
        S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

        Returns:
            - The maze, distances, starting row and starting column.
            The distances are initialized to infinity, the starting row and column are set to the location of "S".
    """
    maze = {} # (r,c) -> tile.
    distances = {} # (r,c) -> distance from starting point.
    starting_r, starting_c = None, None
    for row_idx, line in enumerate(file):
        for col_idx, tile in enumerate(line.strip()):
            maze[(row_idx, col_idx)] = tile
            distances[(row_idx, col_idx)] = -float("inf") # Initialize all distances to infinity.
            if tile == "S":
                starting_r, starting_c = row_idx, col_idx
    return maze, distances, starting_r, starting_c


def get_valid_directions(r, c, maze, distances):
    """ Given coordinates (r, c), the maze and distances, return the valid directions to traverse (r,c), and the updated distances.
    Valid directions are determined by the tile type.
    This function is used to determine the next tile to traverse.
    """
    next_r, next_c = None, None

    found_end_counter = 0
    found_end_distance = []

    # based on the type of current tile, we can only go in certain directions.

    # can only go south and east
    if maze.get((r,c)) == "F":
        
        if distances.get((r+1,c), None) == -float("inf"):
            distances[r+1,c] = distances[r,c] + 1
            next_r, next_c = r+1, c
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r+1,c])
        if distances.get((r,c+1), None) == -float("inf"):
            distances[r,c+1] = distances[r,c] + 1
            next_r, next_c = r, c+1
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r,c+1])
    # can only go south and west
    elif maze.get((r,c)) == "7":
        if distances.get((r+1,c), None) == -float("inf"):
            distances[r+1,c] = distances[r,c] + 1
            next_r, next_c = r+1, c
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r+1,c])
        if distances.get((r,c-1), None) == -float("inf"):
            distances[r,c-1] = distances[r,c] + 1
            next_r, next_c = r, c-1
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r,c-1])
    # can only go north and west
    elif maze.get((r,c)) == "J":
        if distances.get((r-1,c), None) == -float("inf"):
            distances[r-1,c] = distances[r,c] + 1
            next_r, next_c = r-1, c
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r-1,c])
        if distances.get((r,c-1), None) == -float("inf"):
            distances[r,c-1] = distances[r,c] + 1
            next_r, next_c = r, c-1
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r,c-1])
    # can only go north and east
    elif maze.get((r,c)) == "L":
        if distances.get((r-1,c), None) == -float("inf"):
            distances[r-1,c] = distances[r,c] + 1
            next_r, next_c = r-1, c
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r-1,c])
        if distances.get((r,c+1), None) == -float("inf"):
            distances[r,c+1] = distances[r,c] + 1
            next_r, next_c = r, c+1
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r,c+1])
    # can only go north and south
    elif maze.get((r,c)) == "|":
        if distances.get((r-1,c), None) == -float("inf"):
            distances[r-1,c] = distances[r,c] + 1
            next_r, next_c = r-1, c
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r-1,c])
        if distances.get((r+1,c), None) == -float("inf"):
            distances[r+1,c] = distances[r,c] + 1
            next_r, next_c = r+1, c
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r+1,c])
    # can only go east and west
    elif maze.get((r,c)) == "-":
        if distances.get((r,c-1), None) == -float("inf"):
            distances[r,c-1] = distances[r,c] + 1
            next_r, next_c = r, c-1
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r,c-1])
        if distances.get((r,c+1), None) == -float("inf"):
            distances[r,c+1] = distances[r,c] + 1
            next_r, next_c = r, c+1
        else:
            found_end_counter += 1
            found_end_distance.append(distances[r,c+1])

    if found_end_counter == 2:
        assert len(found_end_distance) == found_end_counter
        return r, c, distances # the current coordinates - can't move anywhere else.

    # print(f"Found valid directions: ({next_r}, {next_c}), with distances: {distances[next_r, next_c]} and current coordinates ({r},{c})  have distance {distances[r,c]}.")
    return next_r, next_c, distances

def find_directions(r, c, maze, distances):
    """ Given an array of coordinates, retrieve the next possible tile.
    Update the distance of the next tile to be one larger than the current one.
    If the next tile's distance is already set - we have a loop and can stop traversing the maze.
    If the given coordinates are just the starting position (the S tile), then we need to check which tiles around it can be connected.
    Each tile can have connections orthogonally to it.

    Returns:
        - The updated distances matrix.
        - The next coordinates to traverse.
    """

    next_r, next_c = [], []
    if len(r) == 1:
        r = r[0]
        c = c[0]
        if maze.get((r,c), None) == "S":
            # check if we can go north
            if maze.get((r-1,c), "Invalid") in "|7F":
                distances[r-1,c] = distances[r,c] + 1
                next_r.append(r-1)
                next_c.append(c)
            # check if we can go south
            if maze.get((r+1,c), "Invalid") in "|JL":
                distances[r+1,c] = distances[r,c] + 1
                next_r.append(r+1)
                next_c.append(c)
            # check if we can go west
            if maze.get((r,c-1), "Invalid") in "-FL":
                distances[r,c-1] = distances[r,c] + 1
                next_r.append(r)
                next_c.append(c-1)
            # check if we can go east
            if maze.get((r,c+1), "Invalid") in "-J7":
                distances[r,c+1] = distances[r,c] + 1
                next_r.append(r)
                next_c.append(c+1)

            # print(f"Initially selected {r},{c} as the starting point. The next coordinates are: ({next_r[0]}, {next_c[0]}) and ({next_r[1]}, {next_c[1]})")

            return next_r, next_c, distances
    else:
        # now for each coordinate, we need to check all orthogonal squares
        # the orthogonal square, that's valid and has inf distance is the next square to traverse
        # otherwise, if it's valid and the distance is not inf - then that's the previous square and you can obtain that distance.
        for r_idx, c_idx in zip(r, c):
            next_r_idx, next_c_idx, distances = get_valid_directions(r_idx, c_idx, maze, distances)
            next_r.append(next_r_idx)
            next_c.append(next_c_idx)

        return next_r, next_c, distances

def main():
    args = parse_arguments()

    with open(args.input_file, "r") as file:
        maze, distances, starting_r, starting_c = create_maze(file)

        distances[starting_r, starting_c] = 0

        found_end = False
        current_r, current_c = [starting_r], [starting_c]
        while not found_end:
            # traverse the maze until you reach a point where there are already distances recorded, meaning we've encountered a loop.
            next_r, next_c, distances = find_directions(current_r, current_c, maze, distances)

            if current_r == next_r and current_c == next_c:
                found_end = True

            current_r, current_c = next_r, next_c

        print(f"The distance to the end is: {distances[current_r[0], current_c[0]]}")

if __name__ == '__main__':  
    main()