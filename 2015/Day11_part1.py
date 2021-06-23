"""
Password Security
"""

import time
import re
import sys


def string_incremeneter(string_input):
    # check if we are at z (or zzzz) and need to loop
    z_counter = 0
    for char in reversed(string_input):
        if char == 'z':
            z_counter += 1
        else:
            break  # We only care about the last zs

    # Using ord and chr to swap between character and number
    if z_counter > 0:
        new_string = string_input[:-(z_counter + 1)]
        new_string = new_string + chr(ord(string_input[-(z_counter + 1)])+1)
        new_string = new_string + 'a'*z_counter
    else:
        new_string = string_input[:-1]
        new_string = new_string + chr(ord(string_input[-1])+1)
    return new_string


def condition1(string_input):
    # I am not sure if Regex would be faster, but this seemed simpler to code
    meets_req = False
    for first, second, third in zip(string_input, string_input[1:], string_input[2:]):
        ch1 = ord(first)
        ch2 = ord(second)
        ch3 = ord(third)
        if ch1 == (ch2 - 1) == (ch3 - 2):
            meets_req = True
            break
    return meets_req


def condition2(string_input):
    # Regex checks if string contains the letters 'i' or 'o' or 'l'
    pattern2 = re.compile(r'.*(i|o|l)')
    meets_req = not(bool(pattern2.match(string_input)))
    return meets_req


def condition3(string_input):
    #  regex  to find any pattern which consists of 2 repeating characters
    # such as 'gjsaajhuul' but not 'hgaaajgb'
    pattern3 = re.compile(r'.*(.)\1.*(.)\2.*')
    meets_req = bool(pattern3.match(string_input))
    return meets_req


def new_password_finder(string_input):
    meets_req = False
    new_attempt = string_input
    counter = 0
    while meets_req is False:
        new_attempt = string_incremeneter(new_attempt)
        counter += 1
        cond1 = condition1(new_attempt)
        cond2 = condition2(new_attempt)
        cond3 = condition3(new_attempt)
        if cond1 == cond2 == cond3 is True:
            break
        elif (counter % 10000) == 0:
            print(f'Trying attempt number {counter}')
    return new_attempt


if __name__ == "__main__":
    start_time = time.time()

    if len(sys.argv) != 2:
        print('Correct usage is python file.py puzzle_input')

    else:
        puzzle_input = sys.argv[1]
        # sample_input = 'ghijklmn'

        new_password = new_password_finder(puzzle_input)

    end_time = time.time()
    duration = end_time - start_time
    print('the next password is {}'.format(new_password))
    print('The code took {:.2f} seconds to execute'.format(duration))
