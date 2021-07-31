'''Day 18 Advent of Code, game of life
using filter to count neighbours (similar to filters in CNNs)
uainf vectorisation
'''

import sys
import time
import numpy as np
from scipy.ndimage.filters import generic_filter


LEN = 100


def parse(file_loc):
    mygrid = np.zeros([LEN, LEN], dtype=bool)
    with open(file_loc, "r") as myfile:
        for i, line in enumerate(myfile):
            grid_line = line.strip()
            for j, char in enumerate(grid_line):
                if char == '#':
                    mygrid[i, j] = True
    return mygrid


def count_neighbours(grid):
    ''' The following filter slides through all lights to count neighbours:
          1 1 1
          1 0 1
          1 1 1
    '''
    foot_print = np.ones((3, 3))
    foot_print[1, 1] = 0
    ''' mode and cval define how to treat edges: here it adds a border of 0 to the grid '''
    return generic_filter(grid.astype(int), np.sum, footprint=foot_print, mode='constant', cval=0)


def single_step(initial):
    " using boolean logic"
    neighbours = count_neighbours(initial)

    # finds which lights were off, that turned on (all other lights are off)
    off_to_on = np.equal(neighbours, 3)  # returns boolean true or false
    started_off_lights = np.invert(initial) & off_to_on

    # finds which lights were on, that stayed on (all other lights are off)
    on_to_on = np.equal(neighbours, 2) | np.equal(neighbours, 3)  # returns boolean true or false
    started_on_lights = initial & on_to_on

    # finds correct outcome by combining the off to on and the on stay on lights
    next_step = started_off_lights | started_on_lights

    return next_step


def animator(initial, num_steps):
    old = initial
    for _ in range(num_steps):  # specifying that I am not using the counter
        new = single_step(old)
        old = new
    return new


if __name__ == '__main__':
    start_time = time.time()
    input_file = 'Day18_input.txt'

    if len(sys.argv) >= 2:
        input_file = sys.argv[1]

    start_lights = parse(input_file)
    final = animator(start_lights, LEN)
    lights_on = np.sum(final)
    print('The number of lights on at the end is {}'.format(lights_on))

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} seconds to execute'.format(duration))
