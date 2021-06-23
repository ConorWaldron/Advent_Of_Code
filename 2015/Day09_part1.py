"""
Travelling salesman problem without returning to starting city

Brute Force Solution - works well for <20 cities but O(n!)

Sorry I didnt have time to try anything clever!
"""

import time
from itertools import permutations


def instruction_parser(list_strings):
    parsed_instructions = []
    set_cities = set()
    for single_string in list_strings:
        words = single_string.split()
        parsed_instructions.append([words[0], words[2], int(words[4])])
        set_cities.update([words[0], words[2]])
    return parsed_instructions, set_cities


def single_move_distance(city1, city2, distance_map):
    distance = 0
    for entry in distance_map:
        if entry[0] == city1:
            if entry[1] == city2:
                distance = entry[2]

        # if order of cities is not the same as in instructions
        elif entry[1] == city1:
            if entry[0] == city2:
                distance = entry[2]
    if distance == 0:
        print('error could not calculate distance between 2 cities {} and {}'.format(city1, city2))
    return distance


def route_calculator(distance_map, route):
    zipped = zip(route, route[1:])
    total_distance = 0
    for pair in zipped:
        total_distance += single_move_distance(pair[0], pair[1], distance_map)
    return total_distance


def brute_force(distance_map, set_cities):
    """
    The brute force method gives an exact solution but the time required to
    solve it scales with O(n!), therefore it should only be used when
    the number of cities is small (<20)
    """
    possible_distances = []
    possible_orders = permutations(set_cities)
    for route in possible_orders:
        if route[0] < route[-1]:  # only checks A -> B -> C, not C-> B -> A
            route_distance = route_calculator(distance_map, route)
            possible_distances.append(route_distance)
    optimal = min(possible_distances)
    return optimal


if __name__ == "__main__":
    start_time = time.time()

    # Import instructions
    with open('Day9_input.txt', "r") as myfile:
        instructions = myfile.readlines()
    distance_info, locations = instruction_parser(instructions)

    solution = brute_force(distance_info, locations)

    end_time = time.time()
    duration = end_time - start_time
    print('The shortest distance is {}'.format(solution))
    print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
