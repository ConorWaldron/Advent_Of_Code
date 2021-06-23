"""
Advent of Code 2015 Day 5

Problem description: santa is given a list of strings nad needs to decide
which are good and which are bad based on arbitary conditions. We need to
count the number of nice strings in the list.
"""
import time
import numpy as np

# Function appends strings to either nice_list or naughty_list depending on
# conditions and also makes list showing if string failed each condition

# Note we dont need to return the function variable nice_list as changing
# nice_list automatically changes the variable nice in the main function.


def string_checker_a(single_string,
                     nice_list, naughty_list, conditions_summary):
    # condition 1, check if at least 3 vowels are present
    vowels = ['a', 'e', 'i', 'o', 'u']
    vowel_counter = np.zeros(len(vowels))  # records number of each vowel
    i = 0  # reset vowel counter
    for index, specific_vowel in enumerate(vowels):
        vowel_counter[index] =  single_string.count(specific_vowel)  # count number of times that vowel was mentioned
        # Dont need this anymore as using enumerate  i += 1  # move counter on to next vowel
    number_vowels = np.sum(vowel_counter)
    """ This code is a waste of lines, if true, return true, else return false...
    if number_vowels > 2:
        condition1 = True
    else:
        condition1 = False
    """
    condition1 = (number_vowels > 2)

    # condition 2 contains at least 1 letter that appears twice in a row
    condition2 = False
    """ lets try and use zip instead and avoid the use of counters and we dont need to worry about -1
    for j in range(len(single_string)-1):  # dont go to final entry as there is no letter after final to compare to
        if single_string[j] == single_string[j+1]:
            condition2 = True
            break  # dont continue checking strings for two sets of replicates
    """
    for first, second in zip(single_string, single_string[1:]):  # this default terminates when the first iterator empties 
        if first == second:
            condition2 = True
            break
            
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


def string_checker_b(single_string, nice_list,
                     naughty_list, conditions_summary):

    # condition 1, is any pair the same as a pair later on in the string
    condition1 = False
    for i in range(len(single_string)-4):
        for k in range(i+2, len(single_string)-2):
            if single_string[i:i+2] == single_string[k:k+2]:
                condition1 = True
                break  # break the k loop if you find a match
        if condition1 == True:
            break  # break the i loop if you find a match

    # condition 2, 1 letter that repeats with exactly one letter between them
    condition2 = False
    """ # lets use zip instead, so we dont need to worry about the -2 
    for j in range(len(single_string)-2):  # dont go to final two entries as there is no letter after final to compare to
        if single_string[j] == single_string[j+2]:
            condition2 = True
            break  # dont continue checking strings for two sets of replicates
    """
    for first, third in zip(single_string, single_string[2:]):
        if first == third:
            condition2 = True
            break  # dont continue checking strings for two sets of replicates

    # logic to combine the two requirments
    if (condition1 and condition2):
        nice_list.append(single_string)
    else:
        naughty_list.append(single_string)
    this_string_conditions = [condition1, condition2]
    conditions_summary.append(this_string_conditions)
    return


def main(input_strings, option_choice):
    nice = []  # create list of nice strings
    naughty = []  # create list of naughty strings
    condition_list = []  # List showing how strings passed or failed

    for string_entry in input_strings:
        if option_choice == 1:
            string_checker_a(string_entry, nice, naughty, condition_list)
        elif option_choice == 2:
            string_checker_b(string_entry, nice, naughty, condition_list)

    number_failed = [0, 0, 0]
    for cond in condition_list:
        for m in range(len(cond)):
            if cond[m] == False:
                number_failed[m] += 1

    number_nice = len(nice)
    number_naughty = len(naughty)
    if option_choice == 1:
        print('For the conditions in part A')
    if option_choice == 2:
        print('For the conditions in part B')
    print('The number of nice strings is {}'.format(number_nice))
    print('The number of naughty strings is {}'.format(number_naughty))
    return nice, naughty, condition_list


if __name__ == "__main__":
    start_time = time.time()

    # Import list of strings
    with open("Day5_input.txt", "r") as myfile:
        aoc_input_strings = myfile.readlines()

    condition_choice = 2  # 1 for part A conditions, 2 for part B

    santa_nice_list, santa_naughty_list, reason_list = main(aoc_input_strings,
                                                            condition_choice)

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
