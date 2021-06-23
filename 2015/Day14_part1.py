"""
Reindeer Olympics
"""
import time
import sys


def instruction_parser(single_line):
    words = single_line.split()
    name = words[0]
    speed = int(words[3])
    duration = int(words[6])
    rest_time = int(words[-2])
    return [name, speed, duration, rest_time]


def distance_tracker(time, speed, duration, rest_time):
    cycle_time = duration + rest_time
    distance_per_cycle = speed * duration
    num_full_cycles = time//cycle_time  # Floor division
    remaining_time = time % cycle_time
    if remaining_time <= duration:
        distance = distance_per_cycle*num_full_cycles + speed * remaining_time
    else:
        distance = distance_per_cycle*(num_full_cycles+1)
    return distance


def main(duration, filepath):
    furthest_distance = 0
    winning_reindeer = 'nobody :('
    with open(filepath, "r") as myfile:
        for instruction in myfile:
            parsed_instruction = instruction_parser(instruction)
            current_distance = distance_tracker(competition_time, parsed_instruction[1],
                                                parsed_instruction[2], parsed_instruction[3])
            if current_distance > furthest_distance:
                winning_reindeer = parsed_instruction[0]
                furthest_distance = current_distance
    return furthest_distance, winning_reindeer


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Correct usage is python file.py puzzle_input.txt')

    else:
        start_time = time.time()

        competition_time = 2503
        distance, winner = main(competition_time, sys.argv[1])
        print('The winning reindeer {} travelled {} km'.format(winner, distance))

        end_time = time.time()
        duration = end_time - start_time
        print('The code took {:.2f} milliseconds to execute'.format(duration*1000))
