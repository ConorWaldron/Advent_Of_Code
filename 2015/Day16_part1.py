'''Day 16 Advent of Code, Aunt Sue'''
# objective, dont store in memory, just yield them one by one... check until you get perfect match
# store any aunt sues that could match in find, there could be more than one

import sys
import time
import re

TARGET = {'children': 3,
          'cats': 7,
          'samoyeds': 2,
          'pomeranians': 3,
          'akitas': 0,
          'vizslas': 0,
          'goldfish': 5,
          'trees': 3,
          'cars': 2,
          'perfumes': 1}

def parse(file_loc):
    '''
    generator that yields dictionary of input file one sue at a time
    expected format of input is 'Sue XXX: search_word1: int, search_word2: int, search_word3: int'

    :param file_loc: file path to AOC input.txt
    :yield sue_dict: dictionary of integers from that input
    '''
    with open(file_loc, "r") as myfile:
        pattern = r'(\w+): (\d+)'
        for line in myfile:
            regex_matches = re.findall(pattern, line)
            sue_dict = {regex_key: int(regex_value) for regex_key, regex_value in regex_matches}
            yield sue_dict

def matcher(search_dict, file_loc):
    '''
    checks each sue against the description and records ones that match
    :param search_dict: dictionary of the target sue description
    :param file_loc: file path to AOC input.txt
    :return possible_sues: list of numbers of Sues which match description
    '''
    sue_generator = parse(file_loc)
    sue_num = 0
    possible_sues = []
    for sue in sue_generator:
        sue_num += 1
        sue_descriptors = sue.keys()
        if all(sue[key] == search_dict[key] for key in sue_descriptors):
            possible_sues.append(sue_num)
            print('Sue number {} could be the right Sue'.format(sue_num))
    return possible_sues


if __name__ == '__main__':
    start_time = time.time()
    input_file = 'Day16_input.txt'

    if len(sys.argv) >= 2:
        input_file = sys.argv[1]

    possible_match_numbers = matcher(TARGET, input_file)
    if len(possible_match_numbers) == 0:
        print('No possible matches were found')
    elif len(possible_match_numbers) == 1:
        print('The correct Sue is number {}'.format(possible_match_numbers))
    else:
        print('More than 1 possible Sue was found, they are numbers {}'.format(possible_match_numbers))

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
