'''Day 17 Advent of Code, ways to add to 150'''

import sys
import time
import itertools


def parse(file_loc):
    '''
    read input to list

    :param file_loc: file path to AOC input.txt
    :return list_containers: list of container sizes
    '''
    list_containers = []
    with open(file_loc, "r") as myfile:
        for line in myfile:
            value = int(line)
            list_containers.append(value)
    return sorted(list_containers)


def max_and_min(list_containers, target):
    '''
    :param list_containers: list of container sizes
    :param target: the target value we are trying to reach
    :return max_number: the maximum number of containers that can be used to reach 150 wihtout going over
    :return min_number: the minimum number of containers that can be used to reach 150 wihtout being too few
    '''
    num_containers = len(list_containers)

    for i, value in enumerate(list_containers):
        if sum(list_containers[0:i+1]) > target:
            break
    max_number = i

    for i, value in enumerate(list_containers):
        if sum(list_containers[num_containers-i-1:]) >= target:
            break
    min_number = i+1

    return max_number, min_number


def combo_generator(list_containers, max_number, min_number):
    '''
    Generates all the possible way of choosing n containers from a set of containers
    repeated for different values of n as our solution may use 7 or 12 buckets etc

    :param list_containers: list of container sizes
    :param max_number: the maximum number of containers that can be used to reach 150 without going over
    :param min_number: the minimum number of containers that can be used to reach 150 without being too few
    :return: generator with all combinations that could possibly be a solution
    '''
    for num_containers_in_sol in range(min_number, max_number+1):
        combo_level = itertools.combinations(list_containers, num_containers_in_sol)
        for combo in combo_level:
            yield combo


def checker(some_combo, target):
    sum_to_target = False
    if sum(some_combo) == target:
        sum_to_target = True
    return sum_to_target


def main(file_loc, target, part_num):
    my_containers = parse(file_loc)
    max_containers, min_containers = max_and_min(my_containers, target)

    if part_num == 1:
        possible_sol_generator = combo_generator(my_containers, max_containers, min_containers)
        num_correct_combos = 0
        for candidate_combo in possible_sol_generator:
            if checker(candidate_combo, target):
                num_correct_combos += 1
        return num_correct_combos

    if part_num == 2:
        num_correct_combos = 0
        possible_minimum_number = min_containers
        while num_correct_combos == 0:
            possible_sol_generator = combo_generator(my_containers, possible_minimum_number, possible_minimum_number)
            for candidate_combo in possible_sol_generator:
                if checker(candidate_combo, target):
                    num_correct_combos += 1
            possible_minimum_number += 1
        print('The minimum number of containers required is {}'.format(possible_minimum_number-1))
        return num_correct_combos


if __name__ == '__main__':
    start_time = time.time()
    input_file = 'Day17_input.txt'
    total = 150
    part = 1

    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
    if len(sys.argv) == 3:
        part = int(sys.argv[2])

    print(input_file, part)
    num_possible_correct_combos = main(input_file, total, part)
    print('For part {}, the number of correct combinations is {}'.format(part, num_possible_correct_combos))

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} seconds to execute'.format(duration))
