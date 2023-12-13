""" Day 5: If You Give A Seed A Fertilizer, Part 2

We need to parse the input file to get the seeds and the map of the corresponding locations.
We create a function of the map that takes the coordinates of the seed and returns the location.

This function is a bit tricky, because we need to keep track the seed's location as we explore other in-between components (such as temperature, humidity, etc.).

We change our function to read (seed, range) and iterate over it to receive all the seeds.
We then find the lowest location.


The above solution would work, but it has increased complexity, since we're not checking 20 seed numbers, but over 2 billion seed numbers.
We can do better by using a different approach.

We can simplify and lower the number of seeds we need to look for by limiting the search space by only choosing a single location (instead of the whole range).
We can do this by going backwards - we start from the lowest location range and go backwards to find the seeds that are mapped to them.
This will go from 2 billion to 170 million seed numbers.


We can do even better by using a different approach.
We can make use of the range of the seed numbers.



"""

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input file')
    parser.add_argument('--input_file', type=str, help='Path to the input file')
    return parser.parse_args()

def parse_input_file(input_file):

    seeds = [] # list of seeds
    seeds_to_soil = [] # list of tuples (destination, source, num_seeds)
    soil_to_fertilizer = [] # list of tuples (destination, source, num_seeds)
    fertilizer_to_water = [] # list of tuples (destination, source, num_seeds)
    water_to_light = [] # list of tuples (destination, source, num_seeds)
    light_to_temperature = [] # list of tuples (destination, source, num_seeds)
    temperature_to_humidity = [] # list of tuples (destination, source, num_seeds)
    humidity_to_location = [] # list of tuples (destination, source, num_seeds)

    reader_state = "seeds"
    with open(input_file, "r") as file:
        for line in file:
            line_tokens = line.split(":")

            if line_tokens[0] == "seeds":
                seeds_pairs = [int(seed) for seed in line_tokens[1].strip().split(" ")]
                for seed_idx, seed in enumerate(seeds_pairs[0::2]):
                    seeds.append((range(seed, seed+seeds_pairs[2*seed_idx+1])))                
            elif line_tokens[0] == "seed-to-soil map":
                reader_state = "seed_to_soil"
            elif line_tokens[0] == "soil-to-fertilizer map":
                reader_state = "soil_to_fertilizer"
            elif line_tokens[0] == "fertilizer-to-water map":
                reader_state = "fertilizer_to_water"
            elif line_tokens[0] == "water-to-light map":
                reader_state = "water_to_light"
            elif line_tokens[0] == "light-to-temperature map":
                reader_state = "light_to_temperature"
            elif line_tokens[0] == "temperature-to-humidity map":
                reader_state = "temperature_to_humidity"
            elif line_tokens[0] == "humidity-to-location map":
                reader_state = "humidity_to_location"
            else:
                # skip lines that are not needed
                if line.strip() == "":
                    continue

                destination, source, num_seeds = [int(token) for token in line.strip().split()]
                # based on the reader state, we add the line to the corresponding map
                if reader_state == "seed_to_soil":
                    seeds_to_soil.append((destination, source, num_seeds))
                elif reader_state == "soil_to_fertilizer":
                    soil_to_fertilizer.append((destination, source, num_seeds))
                elif reader_state == "fertilizer_to_water":
                    fertilizer_to_water.append((destination, source, num_seeds))
                elif reader_state == "water_to_light":
                    water_to_light.append((destination, source, num_seeds))
                elif reader_state == "light_to_temperature":
                    light_to_temperature.append((destination, source, num_seeds))
                elif reader_state == "temperature_to_humidity":
                    temperature_to_humidity.append((destination, source, num_seeds))
                elif reader_state == "humidity_to_location":
                    humidity_to_location.append((destination, source, num_seeds))
                else:
                    raise Exception(f"Invalid reader state: {reader_state}")

        return seeds, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location

def get_location(seed, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location):
    """ Based on the seed number we find the location of the seed.
    To do this we track it through soil, fertilizer, etc.
    To track it we gather the lower bound of the source number of the corresponding component (soil, fertilizer, etc).
    Then we use this lower bound to find the corresponding destination number.
    We repeat this for all components until we reach the location.
    """

    # First we need to find the soil
    soil = None
    for destination, source, num_seeds in seeds_to_soil:
        if seed >= source and source+num_seeds > seed:
            soil = destination + (seed - source)
            break

    # number is not mapped - we assume it is corresponding to the seed
    if soil is None:
        soil = seed

    # Now we need to find the fertilizer
    fertilizer = None
    for destination, source, num_seeds in soil_to_fertilizer:
        if soil >= source and source+num_seeds > soil:
            fertilizer = destination + (soil - source)
            break
    
    # number is not mapped - we assume it is corresponding to the soil
    if fertilizer is None:
        fertilizer = soil

    # Now we need to find the water
    water = None
    for destination, source, num_seeds in fertilizer_to_water:
        if fertilizer >= source and source+num_seeds > fertilizer:
            water = destination + (fertilizer - source)
            break

    # number is not mapped - we assume it is corresponding to the fertilizer
    if water is None:
        water = fertilizer

    # Now we need to find the light
    light = None
    for destination, source, num_seeds in water_to_light:
        if water >= source and source+num_seeds > water:
            light = destination + (water - source)
            break

    # number is not mapped - we assume it is corresponding to the water
    if light is None:
        light = water
    
    # Now we need to find the temperature
    temperature = None
    for destination, source, num_seeds in light_to_temperature:
        if light >= source and source+num_seeds > light:
            temperature = destination + (light - source)
            break

    # number is not mapped - we assume it is corresponding to the light
    if temperature is None:
        temperature = light

    # Now we need to find the humidity
    humidity = None
    for destination, source, num_seeds in temperature_to_humidity:
        if temperature >= source and source+num_seeds > temperature:
            humidity = destination + (temperature - source)
            break

    # number is not mapped - we assume it is corresponding to the temperature
    if humidity is None:
        humidity = temperature

    # Now we need to find the location
    location = None
    for destination, source, num_seeds in humidity_to_location:
        if humidity >= source and source+num_seeds > humidity:
            location = destination + (humidity - source)
            break

    # number is not mapped - we assume it is corresponding to the humidity
    if location is None:
        location = humidity

    return location

def get_seed(location, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location):
    """ Based on the location range we find the seed range."""
    
    # First we need to find the humidity
    humidity = None
    for source, destination, num_seeds in humidity_to_location:
        if location >= source and source+num_seeds > location:
            humidity = destination + (location - source)
            break

    # number is not mapped - we assume it is corresponding to the location
    if humidity is None:
        humidity = location

    # Now we need to find the temperature
    temperature = None
    for source, destination, num_seeds in temperature_to_humidity:
        if humidity >= source and source+num_seeds > humidity:
            temperature = destination + (humidity - source)
            break

    # number is not mapped - we assume it is corresponding to the humidity
    if temperature is None:
        temperature = humidity

    # Now we need to find the light
    light = None
    for source, destination, num_seeds in light_to_temperature:
        if temperature >= source and source+num_seeds > temperature:
            light = destination + (temperature - source)
            break

    # number is not mapped - we assume it is corresponding to the temperature
    if light is None:
        light = temperature

    # Now we need to find the water
    water = None
    for source, destination, num_seeds in water_to_light:
        if light >= source and source+num_seeds > light:
            water = destination + (light - source)
            break

    # number is not mapped - we assume it is corresponding to the light
    if water is None:
        water = light

    # Now we need to find the fertilizer
    fertilizer = None
    for source, destination, num_seeds in fertilizer_to_water:
        if water >= source and source+num_seeds > water:
            fertilizer = destination + (water - source)
            break

    # number is not mapped - we assume it is corresponding to the water
    if fertilizer is None:
        fertilizer = water

    # Now we need to find the soil
    soil = None
    for source, destination, num_seeds in soil_to_fertilizer:
        if fertilizer >= source and source+num_seeds > fertilizer:
            soil = destination + (fertilizer - source)
            break

    # number is not mapped - we assume it is corresponding to the fertilizer
    if soil is None:
        soil = fertilizer
    
    # Now we need to find the seed
    seed = None
    for source, destination, num_seeds in seeds_to_soil:
        if soil >= source and source+num_seeds > soil:
            seed = destination + (soil - source)
            break

    # number is not mapped - we assume it is corresponding to the soil
    if seed is None:
        seed = soil

    return seed

def valid_seed(seed, seeds):
    """ Check if the seed is valid - it should be in the seeds list."""
    for seed_range in seeds:
        if seed in seed_range:
            return True

    return False

def test_get_seed_function(args):
    """We test whether we have correctly mapped the input."""

    seeds, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location = parse_input_file(args.input_file)

    locations = [529571705, 3374647, 386490336]
    expected_seeds = [280775197, 7535297, 3229061264]

    for idx, location in enumerate(locations):
        seed = get_seed(location, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location)
        assert expected_seeds[idx] == seed, f"Expected seed: {expected_seeds[idx]}, got: {seed}"

def test_get_location_function(args):
    """We test whether we have correctly mapped the input."""

    seeds, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location = parse_input_file(args.input_file)

    seeds = [280775197, 7535297, 3229061264]
    expected_location = [529571705, 3374647, 386490336]

    for idx, seed in enumerate(seeds):
        location = get_location(seed, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location)
        assert expected_location[idx] == location, f"Expected location: {expected_location[idx]}, got: {location}"

def main(args):
    seeds, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location = parse_input_file(args.input_file)


    # Order the location list by destination to start from the lowest location
    humidity_to_location.sort(key=lambda x: x[0])
    # We can do the reverse approach - we start from the location and go backwards
    for location_start, _, location_end in humidity_to_location:

        # perform binary search to find the range of the lowest location
        end_location_seed = get_seed(location_end, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location)

        # Check the location end - if it's not in the seed number - continue to the next
        if not valid_seed(end_location_seed, seeds):
            continue

        for location in range(location_start, location_end):
            found_seed = get_seed(location, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location)

            if valid_seed(found_seed, seeds):
                print(f"Lowest location found: {location}, seed: {found_seed}")
                exit(0)


if __name__ == "__main__":
    args = parse_arguments()
    test_get_location_function(args)
    print("Successfully passed get_location function unit test.")
    test_get_seed_function(args)
    print("Successfully passed get_seed function unit test.")
    main(args)