'''Day 18 Advent of Code, game of life'''

import sys
import time
import numpy as np

def parse(file_loc, part_num):
    mygrid = np.zeros([100, 100], dtype=int)
    with open(file_loc, "r") as myfile:
        for i, line in enumerate(myfile):
            grid_line = line.strip()
            for j, char in enumerate(grid_line):
                if char == '#':
                    mygrid[i, j] = 1
    if part_num == 2:
        mygrid[0, 0] = 1
        mygrid[0, -1] = 1
        mygrid[-1, 0] = 1
        mygrid[-1, -1] = 1
    return mygrid


def count_neighbours(three_by_three):
    on_neighbours = np.sum(three_by_three) - three_by_three[1,1]
    return on_neighbours


def single_step(initial, part_num):
    side_len = initial.shape[0]
    old = np.zeros([side_len+2, side_len+2], dtype=int)
    old[1:-1, 1:-1] = initial
    new = np.zeros_like(initial, dtype=int)
    for i in range(side_len):
        for j in range(side_len):
            num_on_neighbours = count_neighbours(old[i:i+3, j:j+3])
            if old[i+1, j+1] == 1:
                if num_on_neighbours == 2 or num_on_neighbours == 3:
                    new[i, j] = 1
            if old[i+1, j+1] == 0:
                if num_on_neighbours == 3:
                    new[i, j] = 1
    if part_num == 2:
        new[0, 0] = 1
        new[0, -1] = 1
        new[-1, 0] = 1
        new[-1, -1] = 1
    return new


def animator(initial, num_steps, part_num):
    i = 0
    old = initial
    while i < num_steps:
        new = single_step(old, part_num)
        old = new
        i += 1
    return new


if __name__ == '__main__':
    start_time = time.time()
    input_file = 'Day18_input.txt'
    part = 1
    number_steps = 100

    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
    if len(sys.argv) == 3:
        part = int(sys.argv[2])

    start_lights = parse(input_file, part)
    final = animator(start_lights, number_steps, part)
    lights_on = np.sum(final)
    print('The number of lights on at the end is {}'.format(lights_on))

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} seconds to execute'.format(duration))
