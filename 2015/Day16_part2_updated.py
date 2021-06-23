'''Day 16 Advent of Code, Aunt Sue'''

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
    :yield sue_dict: dictionary of integers from that input such as {'children': 3, 'cats': 7, 'samoyeds': 2,}
    '''
    with open(file_loc, "r") as myfile:
        pattern = r'(\w+): (\d+)'
        for line in myfile:
            regex_matches = re.findall(pattern, line)
            sue_dict = {regex_key: int(regex_value) for regex_key, regex_value in regex_matches}
            yield sue_dict


def rules(sue_key, candidate_value, target_value, part):
    '''
    Checks if a single value in a single sue input string against the target using part 1 & 2 rules
    :param sue_key: something like 'cats'
    :param candidate_value: some int
    :param target_value: some int
    '''
    if part == 2:
        if sue_key in ['cats', 'trees']:
            if candidate_value > target_value:
                return True
        elif sue_key in ['pomeranians', 'goldfish']:
            if candidate_value < target_value:
                return True
        else:
            if candidate_value == target_value:
                return True
    else:
        if candidate_value == target_value:
            return True
    return False


def matcher(search_dict, file_loc, part):
    '''
    checks each sue against the description and records ones that match (maybe there will be more than 1)
    :param search_dict: dictionary of the target sue description
    :param file_loc: file path to AOC input.txt
    :param part: 1 or 2 depending on what rules you want to apply
    :return possible_sues: list of numbers of Sues which match description
    '''
    sue_generator = parse(file_loc)
    sue_num = 0
    possible_sues = []
    for sue in sue_generator:
        sue_num += 1
        sue_descriptors = sue.keys()
        if all(rules(key, sue[key], search_dict[key], part) for key in sue_descriptors):
            possible_sues.append(sue_num)
            print('Sue number {} could be the right Sue'.format(sue_num))
    return possible_sues


if __name__ == '__main__':
    start_time = time.time()
    input_file = 'Day16_input.txt'
    part = 2

    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
        if len(sys.argv) == 3:
            part = int(sys.argv[2])

    possible_match_numbers = matcher(TARGET, input_file, part)

    if len(possible_match_numbers) == 0:
        print('No possible matches were found')
    elif len(possible_match_numbers) == 1:
        print('The only possible correct Sue is number {}'.format(possible_match_numbers))
    else:
        print('More than 1 possible Sue was found, they are numbers {}'.format(possible_match_numbers))

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
