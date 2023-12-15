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

Part 2:
Here we adopt the scanline algorithm - we start from the top left corner and go right, i.e. read character by character left to right.
We have a switch that determines whether we're inside the loop made by rope or not.
If we're inside the loop, we need to check if the current character is a pipe tile or not.
If not - we increment the counter.

At the end - we report the counter.
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
            - The maze
            - Distances (initialized to -inf)
            - starting row
            - starting column
            - number of rows
            - number of columns
    """
    maze = {} # (r,c) -> tile.
    distances = {} # (r,c) -> distance from starting point.
    starting_r, starting_c = None, None
    num_rows = 0
    for row_idx, line in enumerate(file):
        num_rows += 1
        num_cols = 0
        for col_idx, tile in enumerate(line.strip()):
            maze[(row_idx, col_idx)] = tile
            distances[(row_idx, col_idx)] = -float("inf") # Initialize all distances to infinity.
            if tile == "S":
                starting_r, starting_c = row_idx, col_idx
            num_cols += 1
    return maze, distances, starting_r, starting_c, num_rows, num_cols


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

def swap_tiles(maze, distances, num_rows, num_cols):
    """
    Given the maze - swapping the tiles in accordance to being part of the loop or not.
    """

    result = {}
    for r in range(num_rows):
        for c in range(num_cols):
            if distances[r, c] == -float("inf"):
                result[(r, c)] = "."
            else:
                result[(r, c)] = maze[(r, c)]

                # special case where there's an S tile - we need to substitute it with the correct tile.
                if maze[(r, c)] == "S":

                    north, south, east, west = False, False, False, False
                    # check if we can go north
                    if maze.get((r-1,c), "Invalid") in "|7F":
                        north = True
                    # check if we can go south
                    if maze.get((r+1,c), "Invalid") in "|JL":
                        south = True
                    # check if we can go west
                    if maze.get((r,c-1), "Invalid") in "-FL":
                        west = True
                    # check if we can go east
                    if maze.get((r,c+1), "Invalid") in "-J7":
                        east = True

                    if north and south:
                        result[(r,c)] = "|"
                    elif east and west:
                        result[(r,c)] = "-"
                    elif north and east:
                        result[(r,c)] = "L"
                    elif north and west:
                        result[(r,c)] = "J"
                    elif south and west:
                        result[(r,c)] = "7"
                    elif south and east:
                        result[(r,c)] = "F"
                    else:
                        raise ValueError("Invalid Starting position!")
                    
                    print(f"Swapped S for {result[(r,c)]} as starting tile.")
                
    return result

def print_maze(maze, num_rows, num_cols):
    for row_idx in range(num_rows):
        for col_idx in range(num_cols):
            print(maze[(row_idx, col_idx)], end="")
        print()

def main():
    args = parse_arguments()

    with open(args.input_file, "r") as file:
        maze, distances, starting_r, starting_c, num_rows, num_cols = create_maze(file)

    # 1. Find the tiles that are part of the loop (i.e. where distances are not inf)
    distances[starting_r, starting_c] = 0

    found_end = False
    current_r, current_c = [starting_r], [starting_c]
    while not found_end:
        # traverse the maze until you reach a point where there are already distances recorded, meaning we've encountered a loop.
        next_r, next_c, distances = find_directions(current_r, current_c, maze, distances)

        if current_r == next_r and current_c == next_c:
            found_end = True

        current_r, current_c = next_r, next_c

    # 2. Traverse the maze again, this time substituting the tiles with the correct tiles.
    swapped_maze = swap_tiles(maze, distances, num_rows, num_cols)
    
    # 3. Traverse the maze a third time, counting the number of tiles inside the loop.
    inside_counter = 0
    substituted_maze = {}
    for row_idx in range(num_rows):
        # reset variables each time we hit a new row
        inside = False # switcher to determine if we're inside the loop or not.
        found_top_left = False # if we find top left tile - record it as we need to swap the inside/outside condition of both top left and bottom right are found
        found_bottom_left = False # if we find bottom left - record it, as we need to swap inside/outside condition if both bottom left and top right are found

        for col_idx in range(num_cols):

            # either inside or outside the loop
            if swapped_maze[(row_idx, col_idx)] == ".":
                if inside:
                    inside_counter += 1
                    substituted_maze[(row_idx, col_idx)] = "I"
                else:
                    substituted_maze[(row_idx, col_idx)] = "O"

            # met a wall - swap inside and outside
            elif swapped_maze[(row_idx, col_idx)] == "|":
                inside = not inside
                substituted_maze[(row_idx, col_idx)] = "|"
            
            # met a top left corner, record it
            elif swapped_maze[(row_idx, col_idx)] == "F":
                found_top_left = True
                substituted_maze[(row_idx, col_idx)] = "┌"
            
            # met a bottom left corner, record it
            elif swapped_maze[(row_idx, col_idx)] == "L":
                found_bottom_left = True
                substituted_maze[(row_idx, col_idx)] = "┕"

            # met a top right corner, check if we have bottom left and swap if so
            elif swapped_maze[(row_idx, col_idx)] == "7":
                if found_bottom_left:
                    inside = not inside
                    found_bottom_left = False
                if found_top_left:
                    found_top_left = False
                substituted_maze[(row_idx, col_idx)] = "┐"

            # met a bottom right corner, check if we have top left and swap if so
            elif swapped_maze[(row_idx, col_idx)] == "J":
                if found_top_left:
                    inside = not inside
                    found_top_left = False
                if found_bottom_left:
                    found_bottom_left = False
                substituted_maze[(row_idx, col_idx)] = "┚"

            # just record - don't do anything else
            elif swapped_maze[(row_idx, col_idx)] == "-":
                substituted_maze[(row_idx, col_idx)] = "-"

    print("Final maze:")
    print_maze(substituted_maze, num_rows, num_cols)

    print(f"The number of tiles inside the loop is: {inside_counter}.")

if __name__ == '__main__':  
    main()