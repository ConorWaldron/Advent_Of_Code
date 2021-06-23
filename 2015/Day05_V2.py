"""
Advent of Code 2015 Day 5

Problem description: santa is given a list of strings nad needs to decide
which are good and which are bad based on arbitary conditions. We need to
count the number of nice strings in the list.

https://regex101.com/ or www.regexr.com

"""
import sys
import re
import time


def conditions_A(single_string):
    vowel = bool(re.compile(r'(.*[aeiou]){3,}').search(single_string))
    duplicate = bool(re.compile(r'(.)\1').search(single_string))
    banned = not(bool(re.compile(r'(ab|cd|pq|xy)').search(single_string)))  # Note use of not as the Regex found matches that had the banned strings
    result_final = vowel and duplicate and banned
    return result_final


def conditions_B(single_string):
    repeated_pair = bool(re.compile(r'(..).*\1').search(single_string))
    repeat_with_gap = bool(re.compile(r'.*(.).\1.*').search(single_string))
    result_final = repeated_pair and repeat_with_gap
    return result_final


def main(filename, option):
    with open(filename, "r") as myfile:
        aoc_input_strings = myfile.readlines()

    number_nice = 0  # initilise count of nice strings at 0
    for count, single_string in enumerate(aoc_input_strings):
        if option == 'A':
            single_string_outcome = conditions_A(single_string)
        elif option == 'B':
            single_string_outcome = conditions_B(single_string)
        else:
            single_string_outcome = 0  # An error occured but we still need a value here
            if count == 0:
                print('Error! The function argument for option must be \'A\' or \'B\'')
        number_nice += single_string_outcome  # we can add booleans as int
    return number_nice


if __name__ == "__main__":
    start_time = time.time()
    """
    if len(sys.argv) != 3:
        print('The correct syntax to run this code from the command line\
              is python [file.py] [textfile.txt] [option] where option should\
              be A or B')
    else:
        answer = main(sys.argv[1], sys.argv[2])
        if sys.argv[2] == 'A' or sys.argv[2] == 'B':
            print(f'There are {answer} nice strings')
    
    """
    # For running from spyder
    option ='B'
    answer = main('Day5_input.txt', option)
    if option == 'A' or option == 'B':
        print(f'There are {answer} nice strings')
    
    
    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
