""" Day 5: If You Give A Seed A Fertilizer

We need to parse the input file to get the seeds and the map of the corresponding locations.
We create a function of the map that takes the coordinates of the seed and returns the location.

This function is a bit tricky, because we need to keep track the seed's location as we explore other in-between components (such as temperature, humidity, etc.).

We do this for all seeds, and find the lowest location.
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
                seeds = [int(seed) for seed in line_tokens[1].strip().split(" ")]
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

def main():
    args = parse_arguments()
    seeds, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location = parse_input_file(args.input_file)

    # Now we need to find the lowest location
    lowest_location = None
    for seed in seeds:
        # we need to find the location of the seed
        location = get_location(seed, seeds_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location)
        
        if lowest_location is None or location < lowest_location:
            lowest_location = location

    print(f"Lowest location: {lowest_location}")

if __name__ == "__main__":
    main()