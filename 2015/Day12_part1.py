"""
Read highly nested & irregular JSON file
"""

import time
import json
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


if __name__ == "__main__":
    start_time = time.time()

    if len(sys.argv) != 2:
        print('Correct usage is python file.py puzzle_input.txt')

    else:
        with open(sys.argv[1], "r") as myfile:
            data = json.load(myfile)

        flattened_data = flatten_json(data)

        total_sum = sum_values(flattened_data)

        end_time = time.time()
        duration = end_time - start_time
        print('The answer is {}'.format(total_sum))
        print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
