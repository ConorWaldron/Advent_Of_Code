"""
Reindeer Olympics
"""
import time
import numpy as np
import sys

def instruction_parser(single_line):
    '''
    Expects input to be of the form
    Dasher can fly 4 km/s for 16 seconds, but then must rest for 55 seconds.
    so that we can extract names and numbers by word positions
    '''
    words = single_line.split()
    name = words[0]
    speed = int(words[3])
    go_duration = int(words[6])
    rest_time = int(words[-2])
    return [name, speed, go_duration, rest_time]


def distance_tracker(time, speed, go_duration, rest_time):
    '''returns distance of a single reindeer at a given time'''
    cycle_time = go_duration + rest_time
    num_full_cycles, remaining_time = divmod(time, cycle_time)
    distance = (go_duration * num_full_cycles + min(remaining_time, go_duration) ) * speed
    return distance


def points_at_time_t(reindeer_details, time):
    '''
    calculates which reindeer (or plural if tie) get points at given time (required for part 2)
    also returns the maximum distance at that time (required for part 1)
    '''
    num_reindeer = len(reindeer_details)
    distances = np.zeros(num_reindeer)
    for count, deer_details in enumerate(reindeer_details):
        distances[count] = distance_tracker(time, deer_details[1], deer_details[2], deer_details[3])
    max_distance = distances.max()
    winner_indicies = np.zeros(num_reindeer)
    for count, distance in enumerate(distances):
        if distance == max_distance:
            winner_indicies[count] = 1
    return winner_indicies, max_distance


def point_tracker(reindeer_details, finish_time):
    '''just repeat previous function for each second in the race'''
    num_reindeer = len(reindeer_details)
    points = np.zeros(num_reindeer)
    for time in range(1, finish_time):
        points += points_at_time_t(reindeer_details, time)[0]
    return points


def main(race_duration, filepath):
    parsed_instructions = []
    with open(filepath, "r") as myfile:
        for instruction in myfile:
            parsed_instructions.append(instruction_parser(instruction))

    # Part 1 Solution
    winner_vector, longest_distance = points_at_time_t(parsed_instructions, race_duration)
    furthest_reindeer = parsed_instructions[np.argmax(winner_vector)][0]

    # Part 2 Solution
    final_points = point_tracker(parsed_instructions, race_duration)
    winning_index = np.argmax(final_points)
    winning_points = max(final_points)
    winning_reindeer = parsed_instructions[winning_index][0]
    return winning_points, winning_reindeer, longest_distance, furthest_reindeer


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Correct usage is python file.py puzzle_input.txt')

    else:
        start_time = time.time()

        competition_time = 2503
        points, winner_part2, max_distance, winner_part1 = main(competition_time, sys.argv[1])
        print('By the rules of part 1, the winning reindeer {} had travelled {} km'.format(winner_part1, max_distance))
        print('By the rules of part 2, the winning reindeer {} had {} points'.format(winner_part2, points))

        end_time = time.time()
        code_run_duration = end_time - start_time
        print('The code took {:.2f} milliseconds to execute'.format(code_run_duration*1000))
