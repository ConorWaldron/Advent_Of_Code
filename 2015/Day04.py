# -*- coding: utf-8 -*-
"""
Advent of Code 2015 Day 4, Advent Coin Mining
Problem description
The MD5 hash function takes some input and returns a 32 character hexadecimal
string as the hash output. We are given a alphabetic character string input
and told we need to append it with some decimal number. The aim is to find the
lowest decimal number to add to the alphabet string which when the string and
number are combined produce a hexadecimal hash that leads with 5 zeros.
"""

import hashlib
import time


# Function that iterates through numbers starting at 1 until it hits target
def advent_coin_miner(input_string, number_zeros):
    solution = False  # repeat while loop until solution is true
    number = 1
    while solution == False:
        concat_input = input_string + str(number)
        hash_out = hashlib.md5(concat_input.encode("utf-8")).hexdigest()
        first_characters = hash_out[0:number_zeros]
        target = '0' * number_zeros  # creates a string with n zeroes
        if first_characters == target:  # check if I found a solution
            solution = True
        else:
            number += 1
        if number % 100000 == 0:  # to show that the code is still running
            print('Tested up to number {}, still no success'.format(number))
    return number


def main(input_aoc):
    answer_A = advent_coin_miner(input_aoc, 5)
    print('The answer to part A is {}'.format(answer_A))

    answer_B = advent_coin_miner(input_aoc, 6)
    print('The answer to part B is {}'.format(answer_B))
    return


if __name__ == "__main__":
    start_time = time.time()
    input_string = 'ckczppom'  # The example input from Advent of Code
    main(input_string)
    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
