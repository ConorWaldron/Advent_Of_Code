'''Day 20 Advent of Code, infinity presents'''

import sys
import time
from functools import reduce


def factors(n):
    '''returns set of all the factors of n
    taken from https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python'''
    return set(reduce(list.__add__,
                      ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def present_calculator(house_num):
    factor_set = factors(house_num)
    presents = 0
    for num in factor_set:
        presents += num * 10
    return presents


def main(target):
    house_num = 1
    while True:
        if house_num % 100000 == 0:
            print('Checking house number {}'.format(house_num))
        num_presents = present_calculator(house_num)
        if num_presents > target:
            break
        house_num += 1
    return house_num


if __name__ == '__main__':
    start_time = time.time()
    min_presents = 29000000
    part = 2

    if len(sys.argv) >= 2:
        min_presents = sys.argv[1]
    if len(sys.argv) = 3:
        part = sys.argv[2]

    min_house_number = main(min_presents)
    print('The lowest house number is {}'.format(min_house_number))

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} seconds to execute'.format(duration))
