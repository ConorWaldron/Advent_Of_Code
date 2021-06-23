"""
Advent of Code 2015 Day 6

Problem description
We have a 1000 by 1000 square grid of lights and we need to turn on a specific
pattern by following santas instrictions. Santas instructions will either be
turn on, turn off or toggle a specific range of lights.

For part A turn on means turn on (or leave on those lights), while toggle means
switch  all lights which were on to off and vice versa.

For part B, turn on means increase brightness by 1, toggle means increase
brighness by 2 and turn off means reduce brightness by 1 to min of 0.

Santa describes the position of the lights by giving the cordinate of opposite
corners of rectanges for example 660, 55 through 986, 197
"""
import time
import numpy as np
import sys


# Returns instructions in computer readable format
def instruction_reader(list_of_strings):
    instruction_array = []
    for entry in list_of_strings:
        # Idenitfy the command given
        if 'on' in entry:
            command = 0
        elif 'off' in entry:
            command = 1
        elif 'toggle' in entry:
            command = 2
        else:
            print('Invalid instruction')

        # identify the cordinates
        corners = [i for i in entry.split() if ',' in i]
        first_corner = corners[0].split(',')
        second_corner = corners[1].split(',')

        # append command and cordinates to instruction_array
        readable_instruction = [command, int(first_corner[0]),
                                int(first_corner[1]), int(second_corner[0]),
                                int(second_corner[1])]
        instruction_array.append(readable_instruction)
    return instruction_array


def light_switcher(light_grid, single_instruction):
    if single_instruction[0] == 0:  # On command
        for i in range(single_instruction[1], single_instruction[3]+1):  # Loop over rows, add 1 ot be inclusive
            light_grid[i, single_instruction[2]:single_instruction[4]+1] = 1  # add 1 to be inclusive

    if single_instruction[0] == 1:  # Off command
        for i in range(single_instruction[1], single_instruction[3]+1):  # Loop over rows, add 1 to be inclusive
            light_grid[i, single_instruction[2]:single_instruction[4]+1] = 0  # add 1 to be inclusive

    if single_instruction[0] == 2:  # Toggle command
        for i in range(single_instruction[1], single_instruction[3]+1):  # Loop over rows, add 1 to be inclusive
            for j in range(single_instruction[2], single_instruction[4]+1):  # Loop over columns, add 1 to be inclusive
                if light_grid[i, j] == 0:
                    light_grid[i, j] = 1
                elif light_grid[i, j] == 1:
                    light_grid[i, j] = 0
                else:
                    print('light was in unknown starting state')
    return light_grid


def light_switcher_ancient_elvish(light_grid, single_instruction):
    if single_instruction[0] == 0:  # Increase by 1
        for i in range(single_instruction[1], single_instruction[3]+1):  # Loop over rows, add 1 ot be inclusive
            light_grid[i, single_instruction[2]:single_instruction[4]+1] += 1  # increase values by 1

    if single_instruction[0] == 1:  # decrease by 1 to minimum of 0
        for i in range(single_instruction[1], single_instruction[3]+1):  # Loop over rows, add 1 to be inclusive
            light_grid[i, single_instruction[2]:single_instruction[4]+1] -= 1  # reduce value by 1
            for j in range(single_instruction[2], single_instruction[4]+1):  # Loop over columns, add 1 to be inclusive
                if light_grid[i, j] < 0:
                    light_grid[i, j] = 0

    if single_instruction[0] == 2:  # increase by 2
        for i in range(single_instruction[1], single_instruction[3]+1):  # Loop over rows, add 1 ot be inclusive
            light_grid[i, single_instruction[2]:single_instruction[4]+1] += 2  # increase values by 1     
    return light_grid


if __name__ == "__main__":
    start_time = time.time()
    my_grid = np.zeros((1000, 1000))
    
    if len(sys.argv) != 2:
        print('Error, the required format is python pyfile.py file.txt')
    else:
        # Import instructions
        with open(sys.argv[1], "r") as myfile:
            light_instructions = myfile.readlines()
        readable_instructions = instruction_reader(light_instructions)
    
        for single_order in readable_instructions:
            my_grid = light_switcher(my_grid, single_order)
        num_lights_on_a = int(np.sum(my_grid))
        print(f'For part A, the number of lights on is {num_lights_on_a}')
    
        my_grid = np.zeros((1000, 1000))  # Reinitilise for part B
        for single_order in readable_instructions:
            my_grid = light_switcher_ancient_elvish(my_grid, single_order)
        num_lights_on_b = int(np.sum(my_grid))
        print(f'For part B, the toal brightness is {num_lights_on_b}')

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
    
A = np.random.rand(10,10)
B = np,random.rand(10,10)

for i in range(0, len(A[:,0])):
    for j in range(0, len(B[0,:])):
        C = a[i,j] * B[i,j]
