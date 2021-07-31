"""
Day 19 Advent of Code, Reindeer Chemistry

Stolen from https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/cy4cu5b
    Note this method does not guarantte the correct answer (shortest number of mutations), it just provides a path.

The correct algorithm apparently, is something called A star
"""

import sys
import time
from random import shuffle


def parse(file_loc):
    """ create a dictionary with arrays of outputs for each key (1 element can undergo multiple transformations)
    create additional reverse dictionary, this doesnt need arrays as each product is uniquely produced by 1 reagent"""
    transformations_dict = {}
    reverse_dict = {}
    with open(file_loc, "r") as myfile:
        for line in myfile:
            if '=>' in line:
                reagent, product = line.strip().split(' => ')
                reverse_dict[product] = reagent
                if reagent in transformations_dict:  # add new product to existing list
                    transformations_dict[reagent].append(product)
                else:  # this reagents isnt in the dictionary yet
                    transformations_dict[reagent] = [product]
            else:
                target_molecule = line.strip()
    return transformations_dict, target_molecule, reverse_dict


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


def one_substitute_back(start_mol, rev_transformations_dict, order_of_subs):
    """
    takes a final molecule and tries to make it simpler by doing 1 reverse substiutions
    this just applies the first valid substitution it can find, in many cases there will be many possibilities
    so this is not an exhaustive search and there is no gurantee that it will find the right solution.
    So this an attempt at a dumb/cheeky shortcut
    """
    made_sub = False
    for sub in order_of_subs:  # try the first subsitution in the list of subsitutions
        if made_sub == False:
            for count, _ in enumerate(start_mol):  # try each position in the start_mol
                if start_mol[count:count+len(sub)] == sub:
                    simpler_mol = start_mol[0:count]+rev_transformations_dict[sub]+start_mol[count+len(sub):]
                    made_sub = True
                    break  # breaks loop along start_mol, then re-enters next sub
        else:
            break  # breaks loop accross different subs

    # after all looping
    if made_sub == False:  # no solution was possible, we reached a dead end
        simpler_mol = start_mol
    return simpler_mol, made_sub


def reverse_subsitution_chain(original_mol, rev_transformations_dict, verbose):
    """ makes the first substitution possible every time, counts number of substitutions until it reaches 'e'
    or until no subs are possible in which case the solver has failed"""
    num_subs = 0
    dead_ends = []
    start_mol = original_mol

    order_of_subs = []
    for sub in allowed_reverse:
        order_of_subs.append(sub)
    shuffle(order_of_subs)  # doing this so I get a different solution every time I run

    while start_mol != 'e':
        start_mol, made_sub = one_substitute_back(start_mol, rev_transformations_dict, order_of_subs)
        if made_sub == False:
            dead_ends.append(start_mol)
            if verbose:
                print('our chain of substitutions ended before we reached e')
                print('{} dead ends have been found, reshuffling order of substitutions and starting again'.format(len(dead_ends)))
            # reshuffle, reset index and go back to original molecule before starting again
            num_subs = 0
            shuffle(order_of_subs)
            start_mol = original_mol
        else:
            num_subs += 1
    return num_subs


def prove_a_point(original_mol, rev_transformations_dict, n, verbose):
    """ repeat the solution n times to see what the answer would be, each time"""
    set_of_solutions = set()
    for _ in range(n):
        num_subs = reverse_subsitution_chain(original_mol, rev_transformations_dict, verbose)
        set_of_solutions.add(num_subs)
    return set_of_solutions


if __name__ == '__main__':
    start_time = time.time()
    input_file = 'Day19_input.txt'
    part = 2

    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
    if len(sys.argv) == 3:
        part = sys.argv[2]

    allowed_transformations, medecine, allowed_reverse = parse(input_file)

    if part == 1:
        distinct_possibilities = apply_all_transformations(allowed_transformations, medecine)
        print('the number of unique possible molecules formed is {}'.format(len(distinct_possibilities)))
    else:
        number_steps = reverse_subsitution_chain(medecine, allowed_reverse, verbose=False)
        print('our first possible solution took {} subsitutions to make the medecine'.format(number_steps))

        # not needed to solve the problem, just trying to prove a point
        num_runs = 100
        solution_set = prove_a_point(medecine, allowed_reverse, 100, verbose=False)
        print('after running the code {} times, {} possible solutions were found, {}'.format(num_runs, len(solution_set), solution_set))
        # ok, by chance it appears this soltuion always works for this problem, but thats just chance due to the inputs...


    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} seconds to execute'.format(duration))
