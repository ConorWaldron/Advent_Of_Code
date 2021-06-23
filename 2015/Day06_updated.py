"""
Advent of Code 2015 Day 6

Updates since last version
read instructions 1 line at a time instead of storing them all in a big list
toggle with simpler 1 minus implementation instead of if statements
vectorised implementation
"""
import time
import numpy as np
import sys


# Returns instructions in computer readable format
def instruction_reader(single_string):
    # Idenitfy the command given
    if 'on' in single_string:
        command = 0
    elif 'off' in single_string:
        command = 1
    elif 'toggle' in single_string:
        command = 2
    else:
        print('Invalid instruction')

    # identify the cordinates
    corners = [i for i in single_string.split() if ',' in i]
    first_corner = corners[0].split(',')
    second_corner = corners[1].split(',')

    # append command and cordinates to instruction_array
    readable_instruction = [command, int(first_corner[0]),
                            int(first_corner[1]), int(second_corner[0]),
                            int(second_corner[1])]
    return readable_instruction


def light_switcher(light_grid, single_instruction):
    command, x1, y1, x2, y2 = single_instruction
    if command == 0:  # On command
        light_grid[x1:x2+1, y1:y2+1] = 1  # Vector implmentation is faster than for loops

    if command == 1:  # Off command
        light_grid[x1:x2+1, y1:y2+1] = 0  

    if command == 2:  # Toggle command
        light_grid[x1:x2+1, y1:y2+1] = 1 - light_grid[x1:x2+1, y1:y2+1]
    return light_grid


def light_switcher_ancient_elvish(light_grid, single_instruction):
    command, x1, y1, x2, y2 = single_instruction
    if command == 0:  # Increase by 1
        light_grid[x1:x2+1, y1:y2+1] += 1 

    if command == 1:  # decrease by 1 to minimum of 0
        light_grid[x1:x2+1, y1:y2+1] -= 1  
        light_grid[light_grid<0] = 0  # Sets all values less than 0 equal to 0 

    if command == 2:  # increase by 2
        light_grid[x1:x2+1, y1:y2+1] += 2   
    return light_grid


if __name__ == "__main__":
    start_time = time.time()
    my_grid_A = np.zeros((1000, 1000), dtype=int) # int uses less storage than default
    my_grid_B = np.zeros((1000, 1000), dtype=int)
    
    if len(sys.argv) != 2:
        print('Error, the required format is python pyfile.py file.txt')
    else:
        # Import instructions
        with open(sys.argv[1], "r") as myfile:
            for instruction in myfile:
                readable_instruction = instruction_reader(instruction)
                my_grid_A = light_switcher(my_grid_A, readable_instruction)
                my_grid_B = light_switcher_ancient_elvish(my_grid_B, readable_instruction)
        num_lights_on_a = int(np.sum(my_grid_A))
        print(f'For part A, the number of lights on is {num_lights_on_a}')
        num_lights_on_b = int(np.sum(my_grid_B))
        print(f'For part B, the toal brightness is {num_lights_on_b}')

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
