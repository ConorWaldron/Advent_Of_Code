"""
Circular Permuations
"""
import time
import sys
from itertools import permutations

def instruction_parser(single_string, set_of_guests, dict_of_relationships):
    '''parses instruction to foramt (person, gain/lose, integer, person)
    and it creates guest set and dictionary of combined (non directional) happiness values
    the dictionary key is a sorted tuple eg (Alice, Bob) never (Bob, Alice)'''
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

    sorted_key = tuple(sorted((person_A, person_B)))  # lists cannot be dict keys, so we convert to tuple
    if sorted_key in dict_of_relationships:
        dict_of_relationships[sorted_key] += value
    else:
        dict_of_relationships[sorted_key] = value
    return None  # this is a subroutine, it acts directly on inputs


def permuation_list_creator(set_of_guests):
    '''The itertools.permutations function is wasteful as it returns all
    possible arrangments, ignoring the mirror symetry in the problem
    A, B, C, D is the same as D, C, B, A
    and it ignores that the circular symetry
    A, B, C, D is the same as B, C, D, A is the same as C, D, A, B is the same as D, A, B, C

    by only accepting permutations that place A at the start we remove some but
    not all of this unnecessary duplication
    we still get A, B, C, D and A, D, C, B which are the same

    It is also useful to make list with same person at start and end to create a circle
    like A B C D A'''

    set_of_guests.remove('Alice')  # we manually make Alice the start and end of all permutations
    all_possible_permuations = permutations(set_of_guests)

    permuations_list = []
    for perm in all_possible_permuations:
        perm_tuple = ('Alice', ) + perm + ('Alice', )  # tuple concatenation
        permuations_list.append(perm_tuple)
    return permuations_list


def happiness_calculation(single_arrangment, dict_of_relationships):
    '''This function returns happiness for a single table arrangment
    it computes the total happiness of all guests at a table for 1 arrangment'''
    happiness = 0
    for guest1, guest2 in zip(single_arrangment, single_arrangment[1:]):
        happiness += dict_of_relationships[tuple(sorted((guest1, guest2)))]
    return happiness


def brute_force_table_optimiser(set_of_guests, dict_of_relationships):
    '''Searches all possible arrangments to find happiest one, returns best arrangment as tuple and happiness value'''
    list_possible_arrangments = permuation_list_creator(set_of_guests)
    optimal_happiness = -10000000
    index_optimal_arrangment = 0
    for count, arrangment in enumerate(list_possible_arrangments):
        current_happy = happiness_calculation(arrangment, dict_of_relationships)
        if current_happy > optimal_happiness:
            optimal_happiness = current_happy
            index_optimal_arrangment = count
        best_arrangment = list_possible_arrangments[index_optimal_arrangment]
    return best_arrangment, optimal_happiness


def least_happy_pair(single_arrangment, dict_of_relationships):
    '''this function finds which pair of people at the table are least happy
    to be next to each other'''
    least_happy_value = 1000
    for guest1, guest2 in zip(single_arrangment, single_arrangment[1:]):
        current_happy = dict_of_relationships[tuple(sorted((guest1, guest2)))]
        if current_happy < least_happy_value:
            least_happy_value = current_happy
            least_happy_guest_pair = (guest1, guest2)
    return least_happy_guest_pair


def main(filename):
    relationships_dict = {}
    guest_set = set()
    with open(filename, "r") as myfile:
        for instruction in myfile:
            instruction_parser(instruction, guest_set, relationships_dict)

    # Part 1
    optimal_arrangment, opt_happiness = brute_force_table_optimiser(guest_set, relationships_dict)
    print('the optiaml arrangment for part 1 is {}'.format(optimal_arrangment))
    print('the optimal happiness value for part 1 is {}'.format(opt_happiness))

    #Part 2
    # Find most miserbale pair, then Ill sit between them
    miserable_couple = least_happy_pair(optimal_arrangment, relationships_dict)
    print('sure arent {} and {} looking pretty miserable over there?,\
              yeah we better save them from each other'.format(miserable_couple[0], miserable_couple[1]))
    new_opt_arrangment = []
    for guest in optimal_arrangment:
        new_opt_arrangment.append(guest)
        if guest == miserable_couple[0]:
            new_opt_arrangment.append('me')
    print('the optiaml arrangment for part 2 is {}'.format(new_opt_arrangment))

    # Update our relationship list and guest list to include me
    for guest in guest_set:
        relationships_dict[tuple(sorted((guest, 'me')))] = 0
    guest_set.add('me')

    # caluclate the new happiness value
    optimal_happiness_2 = happiness_calculation(new_opt_arrangment, relationships_dict)
    print('the optimal happiness value for part 2 is {}'.format(optimal_happiness_2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Correct usage is python file.py puzzle_input.txt')

    else:
        start_time = time.time()
        main(sys.argv[1])
        end_time = time.time()
        duration = end_time - start_time
        print('The code took {:.1f} milliseconds to execute'.format(duration*1000))