''' Day 19 Advent of Code, Reindeer Chemistry '''

import sys
import time
from copy import copy


def parse(file_loc):
    """ create a dictionary with arrays of outputs for each key (1 element can undergo multiple transformations) """
    transformations_dict = {}
    with open(file_loc, "r") as myfile:
        for line in myfile:
            if '=>' in line:
                reagent, product = line.strip().split(' => ')
                if reagent in transformations_dict:  # add new product to existing list
                    transformations_dict[reagent].append(product)
                else:  # this reagents isnt in the dictionary yet
                    transformations_dict[reagent] = [product]
            else:
                target_molecule = line.strip()
    return transformations_dict, target_molecule, check_duplicates_list, check_duplicates_set


def apply_all_transformations(transformations_dict, starting_molecule):
    """ applies all possible transformations for the starting molecule and the allowed transformations """
    new_molecules = set()
    for reagent in transformations_dict:  # loop over all starting elements (H, O, F ...)
        product_list = transformations_dict[reagent]
        for product in product_list:  # for each starting element, loop over all of its transformation (H->OH, H->HO...)
            for count, _ in enumerate(starting_molecule):  # loop over all elements in the starting molecule
                if starting_molecule[count:count+len(reagent)] == reagent:
                    new_molecules.add(starting_molecule[0:count]+product+starting_molecule[count+len(reagent):])
    return new_molecules


def discover_new_molecules_by_1_step(previously_known_molecules, transformations_dict):
    """ takes set of all known molecules, and applies every possible transformation to each one of the known
    molecules in turn, hence creating a larger set of all known molecules """
    all_known_molecules = copy(previously_known_molecules)  # this is necessary to make independent copy, otherwise both variables point to the same object!
    for molecule in previously_known_molecules:
        new_molecules_1_step_later = apply_all_transformations(transformations_dict, molecule)
        all_known_molecules = all_known_molecules | new_molecules_1_step_later
    return all_known_molecules


def bruteforce_solver(transformations_dict, starting_molecules, target):
    """ keeps creating all possible new molecules 1 step at a time until we find the target molecule
    this is an inefficient solution but it is guaranteed to reach the right answer
    But
    the target molecule is 468 characters long, so more than 200 elements
    since my transitions normally take 1 element and turn it into 2 or 3, this means the minimum steps
    to find the correct answer is probably at least 100 steps
    ive been running my code for 10 min and its only reached 7 steps (and created 1554,000 molecules)
    so this brute force approach is not viable..."""
    created_molecules = copy(starting_molecules)
    i = 0
    while target not in created_molecules:
        print('we still have not made the target molecule')
        created_molecules = discover_new_molecules_by_1_step(created_molecules, transformations_dict)
        i += 1
        print('after {} steps, we have created {} molecules'.format(i, len(created_molecules)))
    print('made the target molecule after {} steps'.format(i))
    return created_molecules, i


if __name__ == '__main__':
    start_time = time.time()
    input_file = 'Day19_input.txt'
    part = 2

    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
    if len(sys.argv) == 3:
        part = sys.argv[2]

    allowed_transformations, medecine = parse(input_file)

    if part == 1:
        distinct_possibilities = apply_all_transformations(allowed_transformations, medecine)
        print('the number of unique possible molecules formed is {}'.format(len(distinct_possibilities)))
    else:
        start = {'e'}
        new_mols, num_steps = bruteforce_solver(allowed_transformations, start, medecine)

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} seconds to execute'.format(duration))
