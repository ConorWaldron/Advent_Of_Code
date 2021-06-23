"""
escape characters are a pain :(
"""
import time
import re
import sys


pattern_backslash = re.compile(r'(\\\\)')
# Matches anything with double backslash \\
pattern_quote = re.compile(r'(\\")')
# Matches anything with backlash quote \"
pattern_ascii = re.compile(r'(\\x\w\w)')
# mathces anything with \x followed by 2 letters or numbers

pattern_combined = re.compile(r'((?:\\\\)|(?:\\")|(?:\\x\w\w))')
# using non capturing groups so I can catch any of the three patterns


def count_char(single_string):
    ''' counts number of characters in code, and how many time each escape sequnece occurs (assuming no overlapping sequences) '''

    num_characters_code_string = len(single_string.strip())

    # problem strings like kwdlysf\\xjpelae overlap backslash with ascii, so
    # the commented code below doesnt work as it double counts overlaps
    # I kept code as sometimes useful for debugging

    # num_backslash = len(re.findall(pattern_backslash, single_string))
    # num_quote = len(re.findall(pattern_quote, single_string))
    # num_ascii = len(re.findall(pattern_ascii, single_string))

    escape_char_list = re.findall(pattern_combined, single_string)

    num_backslash = 0
    num_quote = 0
    num_ascii = 0

    for count, escape in enumerate(escape_char_list):
        if escape == '\\\\':
            num_backslash += 1
            # print('found backslash')
        elif escape == '\\"':
            num_quote += 1
            # print('found qutoe')
        elif 'x' in escape:
            num_ascii += 1
            # print('found ascii')

#    the number of characters in memory is the number of characters in string
#    less two characters for the " at start and end
#    less 1 character for each \\ meaning just \
#    less 1 character for each \" meaning just "
#    less 3 characters for each \xww meaning some single character

    num_char_in_memory = num_characters_code_string - 2 - num_backslash - num_quote - 3 * num_ascii
    return num_characters_code_string, num_char_in_memory


if __name__ == "__main__":
    start_time = time.time()

    if len(sys.argv) != 2:
        print('Error, the required format is python pyfile.py file.txt')
    else:
        num_code_char = 0
        num_char_mem = 0
        # Import instructions
        with open(sys.argv[1], "r") as myfile:
            for instruction in myfile:
                # print(instruction)
                numb_code_single_string, num_mem_single_string = count_char(instruction)
                #print(numb_code_single_string, num_mem_single_string)
                num_code_char += numb_code_single_string
                num_char_mem += num_mem_single_string
            answer = num_code_char - num_char_mem
    
        end_time = time.time()
        duration = end_time - start_time
        print('The total number of literal characters is {}'.format(num_code_char))
        print('The total number of characters in memory is {}'.format(num_char_mem))
        print('The answer is {}'.format(answer))
        print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
