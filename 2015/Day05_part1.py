"""
Advent of Code 2015 Day 5

Problem description: santa is given a list of strings nad needs to decide
which are good and which are bad based on arbitary conditions. We need to
count the number of nice strings in the list.
"""
import time
import numpy as np

# Function counts number of nice strings and also returns array which
# explains which conditions were passed and which failed for each string
def string_checker_a(single_string, nice_list,
                     naughty_list, conditions_summary):
    # condition 1, check if at least 3 vowels are present
    vowels = ['a', 'e', 'i', 'o', 'u']
    vowel_counter = np.zeros(len(vowels))  # records number of each vowel
    i = 0  # reset counter
    for specific_vowel in vowels:
        vowel_counter[i] =  single_string.count(specific_vowel)  # count number of times that vowel was mentioned
        i += 1  # move counter on to next vowel
    number_vowels = np.sum(vowel_counter)
    if number_vowels > 2:
        condition1 = True
    else:
        condition1 = False

    # condition 2 contains at least 1 letter that appears twice in a row
    condition2 = False
    for j in range(0, len(single_string)-1):  # dont go to final entry as there is no letter after final to compare to
        if single_string[j] == single_string[j+1]:
            condition2 = True
            break  # dont continue checking strings for two sets of replicates
    
    # condition 3 string does not contain the strings ab, cd, pq, or xy
    condition3 = True  # swap to False if it contains a banned string
    banned = ['ab', 'cd', 'pq', 'xy']  # list of banned strings
    for banned_combo in banned:
        if banned_combo in single_string:
            condition3 = False
            break  # stop checking for duplicate number of banned entries

    # logic to combine three requirments
    if ((condition1 and condition2) and (condition3)):
        nice_list.append(single_string)
    else:
        naughty_list.append(single_string)
    this_string_conditions = [condition1, condition2, condition3]
    conditions_summary.append(this_string_conditions)
    return


def main(input_strings):
    nice = []  # create list of nice strings
    naughty = []  # create list of naughty strings
    condition_list = []  # List showing how strings passed or failed

    for string_entry in input_strings:
        string_checker_a(string_entry, nice, naughty, condition_list)

    number_failed = [0, 0, 0]
    for cond in condition_list:
        for m in range(0, len(cond)):
            if cond[m] == False:
                number_failed[m] += 1

    number_nice = len(nice)
    number_naughty = len(naughty)
    
    print('For the conditions in part A')
    print('The number of nice strings is {}'.format(number_nice))
    print('The number of naughty strings is {}'.format(number_naughty))
    return nice, naughty, condition_list


if __name__ == "__main__":
    start_time = time.time()

    # Import list of strings
    with open("input.txt", "r") as myfile:
        aoc_input_strings = myfile.readlines()

    santa_nice_list, santa_naughty_list, reason_list = main(aoc_input_strings)

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
