''' Day 19 Advent of Code, Reindeer Chemistry '''

import sys
import time


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
    return transformations_dict, target_molecule


def apply_all_possible_single_transformations(transformations_dict, starting_molecule):
    """ applies all possible transformations for the starting molecule and the allowed transformations """
    new_molecules = set()
    for reagent in transformations_dict:  # loop over all starting elements (H, O, F ...)
        product_list = transformations_dict[reagent]
        for product in product_list:  # for each starting element, loop over all of its transformation (H->OH, H->HO...)
            for count, _ in enumerate(starting_molecule):  # loop over all elements in the starting molecule
                if starting_molecule[count:count+len(reagent)] == reagent:
                    new_molecules.add(starting_molecule[0:count]+product+starting_molecule[count+len(reagent):])
    return new_molecules


if __name__ == '__main__':
    start_time = time.time()
    input_file = 'Day19_input.txt'

    if len(sys.argv) >= 2:
        input_file = sys.argv[1]

    allowed_transformations, medecine = parse(input_file)
    distinct_possibilities = apply_all_possible_single_transformations(allowed_transformations, medecine)
    print('the number of unique possible molecules formed is {}'.format(len(distinct_possibilities)))

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} seconds to execute'.format(duration))
