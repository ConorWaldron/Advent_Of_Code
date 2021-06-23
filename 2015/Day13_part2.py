"""
Circular Permuations
"""
import time
import sys
from itertools import permutations


def instruction_parser(single_string, set_of_guests, list_of_relationships):
    '''parses instruction to foramt (person, gain/lose, integer, person)
    and it creates guest list set'''
    words = single_string.split()
    person_A = words[0]
    person_B = words[-1][:-1]  # extra slice to remove '.' at end of name
    if words[2] == 'gain':
        value = int(words[3])
    elif words[2] == 'lose':
        value = -int(words[3])
    else:
        print('parsing error')
        value = 0
    set_of_guests.add(person_A)
    list_of_relationships.append((person_A, person_B, value))
    return None # this is a subroutine, it acts directly on input list


def permuation_creator(set_of_guests):
    '''The itertools.permutations function is wasteful as it returns all
    possible arrangments, ignoring the mirror symetry in the problem
    A, B, C, D is the same as D, C, B, A
    and it igores that the circular symetry
    A, B, C, D is the same as B, C, D, A is the same as C, D, A, B is the same as D, A, B, C

    by only accepting permutations that place A at the start we remove some but
    not all of this unnecessary duplication
    we still get A, B, C, D and A, D, C, B which are the same'''

    all_possible_permuations = permutations(set_of_guests)

    all_possible_permuations_list = []  # shows the full list without placing alice at start (not actually used in code)
    shortened_permutations_list = []  # shows shortened list (is used in code)
    for perm in all_possible_permuations:
        all_possible_permuations_list.append(perm)
        if perm[0] == 'Alice':
            shortened_permutations_list.append(perm)
    return all_possible_permuations_list, shortened_permutations_list


def circular_guest_list_generator(single_arrangment):
    '''later on it is really handy to make a list with the first guest also
    repeated at the end, so change A, B, C, D to A, B, C, D, A
    since my permuations are tuples (which are immutable), to add A at the end I need to make a
    new list object'''
    circular_list = []
    for guest in single_arrangment:
        circular_list.append(guest)
    circular_list.append(single_arrangment[0])
    return circular_list


def single_guest_happiness(guestA, guestB, list_of_relationships):
    '''finds out how happy guest A will be sitting beside guest B'''
    for relationship in list_of_relationships:
        if relationship[0] == guestA:
            if relationship[1] == guestB:
                happyA_value = relationship[2]
    return happyA_value


def pair_relationship_finder(guest1, guest2, list_of_relationships):
    '''returns the combined happiness values when guest 1 and 2 sit beside each other'''
    happiness_guest1 = single_guest_happiness(guest1, guest2, list_of_relationships)
    happiness_guest2 = single_guest_happiness(guest2, guest1, list_of_relationships)
    sum_happiness = happiness_guest1 + happiness_guest2
    return sum_happiness


def happiness_calculation(single_arrangment, list_of_relationships):
    '''This function returns happiness
    it computes the total happiness of all guests at a table for 1 arrangment'''
    happiness = 0
    circular_guest_list = circular_guest_list_generator(single_arrangment)
    for guest1, guest2 in zip(circular_guest_list, circular_guest_list[1:]):
        happiness += pair_relationship_finder(guest1, guest2, list_of_relationships)
    return happiness


def least_happy_pair(single_arrangment, list_of_relationships):
    '''this function finds which pair of people at the table are least happy
    to be next to each other'''
    circular_guest_list = circular_guest_list_generator(single_arrangment)
    least_happy_value = 1000
    for guest1, guest2 in zip(circular_guest_list, circular_guest_list[1:]):
        current_happy = pair_relationship_finder(guest1, guest2, list_of_relationships)
        if current_happy < least_happy_value:
            least_happy_value = current_happy
            least_happy_guest_pair = (guest1, guest2)
    return least_happy_guest_pair


if __name__ == "__main__":
    start_time = time.time()

    if len(sys.argv) != 2:
        print('Correct usage is python file.py puzzle_input.txt')

    else:
        relationships_list = []
        guest_set = set()
        with open(sys.argv[1], "r") as myfile:
            for instruction in myfile:
                instruction_parser(instruction, guest_set, relationships_list)

        # Part 1
        possible_arrangments, useful_arrangments = permuation_creator(guest_set)
        optimal_happiness = -10000000
        index_optimal_arrangment = 0
        for count, arrangment in enumerate(useful_arrangments):
            current_happy = happiness_calculation(arrangment, relationships_list)
            # print('the arrangment {} gives happiness value of {}'.format(arrangment, current_happy))
            if current_happy > optimal_happiness:
                optimal_happiness = current_happy
                index_optimal_arrangment = count
            best_arrangment = useful_arrangments[index_optimal_arrangment]
        print('the optiaml arrangment for part 1 is {}'.format(best_arrangment))
        print('the optimal happiness value for part 1 is {}'.format(optimal_happiness))

        #Part 2
        # Find most miserbale pair, then Ill sit between them
        miserable_couple = least_happy_pair(best_arrangment, relationships_list)
        print('sure arent {} and {} looking pretty miserable over there?,\
              yeah we better save them from each other'.format(miserable_couple[0], miserable_couple[1]))
        new_opt_arrangment = []
        for guest in best_arrangment:
            new_opt_arrangment.append(guest)
            if guest == miserable_couple[0]:
                new_opt_arrangment.append('me')
        print('the optiaml arrangment for part 2 is {}'.format(new_opt_arrangment))

        # Update our relationship list and guest list to include me
        for guest in guest_set:
            relationships_list.append((guest, 'me', 0))
            relationships_list.append(('me', guest, 0))
        guest_set.add('me')

        # caluclate the new happiness value
        optimal_happiness_2 = happiness_calculation(new_opt_arrangment, relationships_list)
        print('the optimal happiness value for part 2 is {}'.format(optimal_happiness_2))

        end_time = time.time()
        duration = end_time - start_time

        print('The code took {:.2f} seconds to execute'.format(duration))
