"""
look and say

identify the first number
count how many identical numbers follow that one, unitereptured
move on to next number repeat (identify next number, count how many
identical versions of that number follow without interruption)
"""

import time

def single_puzzle_itr(string_input):
    if len(string_input) == 1:
        output_string = str(1) + string_input

    elif len(string_input) > 1:
        current_digit = string_input[0]
        current_num_of_digit = 1
        output_string = str()

        for char in string_input[1:]:
            if char == current_digit:
                current_num_of_digit += 1
            else:
                output_string = output_string + str(current_num_of_digit) + str(current_digit)
                current_digit = char
                current_num_of_digit = 1

        # Reached end of string
        output_string = output_string + str(current_num_of_digit) + str(current_digit)

    return output_string


def multiple_iterations(string_input, num_iter):
    output = string_input
    for count in range(0, num_iter):
        output = single_puzzle_itr(output)
        # print statement useful for debugging
        # print(f'after {count+1} iterations, the output is {output}')
    return output


if __name__ == "__main__":
    start_time = time.time()

    puzzle_input = '3113322113'
    sample_input = '1'

    solution = len(multiple_iterations(puzzle_input, 40))

    end_time = time.time()
    duration = end_time - start_time
    print('the lenght of the solution is {}'.format(solution))
    print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
