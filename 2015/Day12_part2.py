"""
Read highly nested & irregular JSON file
"""

import time
import json
import operator
import re
import sys

def flatten_json(nested_json):
    """
    Code to flatten a highly nested JSON is shamelessly stolen from Alina Zhang,
    https://towardsdatascience.com/how-to-flatten-deeply-nested-json-objects-in-non-recursive-elegant-python-55f96533103d 
    This code is quite cool as it appends the key names to keep track of nest level
    so if the first key was 'tiger' and its value was a nested object in which a key was 'orange'
    and its value was another nested object which had a  key 'fast' that just went to a normal value 4
    it would say 'tiger_organe_fast' : 4, so you know how to find this value
    
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
        
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


def sum_values(flat_json):
    running_sum = 0
    for value in flat_json:
        if type(flat_json[value]) == int:
            running_sum += flat_json[value]
    return running_sum


def find_red(flat_json):
    red_json = {}
    for value in flat_json:
        if flat_json[value] == 'red':
            red_json[value] = flat_json[value]
    return red_json


def find_red_siblings(flat_json, red_dict):
    """
    for objects we need to delete all the siblings of a red key
    so {a: 4, b:red, c:pruple} everything gets deleted including a:4
    for arrays we do not need to delete the siblings
    so [4 red purple] only red gets deleted leaving [4 purple]
    
    I already have a list of the red_keys, now I want to add to that list
    the red object siblings
    """
    red_plus_obj_siblings = []
    for red_key in red_dict:
        # Check if object or array, arrays end in number, objects end in letter
        if red_key[-1] in '0123456789':  # found an array
            red_plus_obj_siblings.append(red_key)  # only the red part gets dropped, not the siblings
        else:  # found an object, now find obj siblings
            red_parent = red_key[:-2]  # access the parent key
            pattern = re.compile(red_parent + '.*')  # find the siblings
            for candidate_key in flat_json:
                check_match = bool(pattern.match(candidate_key))
                if check_match is True:
                    red_plus_obj_siblings.append(candidate_key)
    return red_plus_obj_siblings


def remove_red_siblings(flat_json, red_plus_obj_siblings):
    for red_sib in red_plus_obj_siblings:
        if red_sib in flat_json:
            del flat_json[red_sib]
    return flat_json


if __name__ == "__main__":
    start_time = time.time()

    if len(sys.argv) != 2:
        print('Correct usage is python file.py puzzle_input.txt')

    else:
        with open(sys.argv[1], "r") as myfile:
            data = json.load(myfile)

        flattened_data = flatten_json(data)
        part_1_total_sum = sum_values(flattened_data)
        red_data = find_red(flattened_data)
        red_incl_sibling_list = find_red_siblings(flattened_data, red_data)
        clean_dict = remove_red_siblings(flattened_data, red_incl_sibling_list)
        part_2_total_sum = sum_values(clean_dict)

        end_time = time.time()
        duration = end_time - start_time
        print('The answer is {}'.format(part_1_total_sum))
        print('The answer is {}'.format(part_2_total_sum))
        print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
