"""
Advent of Code 2015, Day 3
Part A Problem Description 
Calculate how many unique houses Santa visits including the starting house
Follow instructions where ^v<> are up, down, left and right

Part B Problem Description
Santa and Robot Santa start at same location and then take turns following
direction from elf
"""

import time
# Function to move Santa/Robot 1 position for 1 instruction
def single_move(houses_set, direction, current_location):
    if direction == '^':
        new_location = (current_location[0] + 1, current_location[1]) 
    elif direction == 'v':
        new_location = (current_location[0] - 1, current_location[1]) 
    elif direction == '<':
        new_location = (current_location[0], current_location[1] - 1) 
    elif direction == '>':
        new_location = (current_location[0], current_location[1] + 1) 
    else:
        print('direction character not a valid instruction')
    set.add(houses_set, new_location) # adds to set only if new house location
    return houses_set, new_location

# Function to count the number of unique houses visited by Santa/robot 
# for a list of directions
def count_unique_houses(directions):
    santas_position = (0,0) # intilise santa at position (0,0)
    robot_position = (0,0) # intilise robot at position (0,0)
    set_of_unique_houses = {(0,0)} # initilise with the (0,0) starting location
    
    # Part A, santa only
    for ch in directions:
        set_of_unique_houses, santas_position = single_move(set_of_unique_houses, ch, santas_position)
    number_unique_houses = len(set_of_unique_houses)
    print('The number of unique houses Santa visited is {}'.format(number_unique_houses))

    # reinitilise variables for part B
    santas_position = (0,0) # intilise santa at position (0,0)
    robot_position = (0,0) # intilise robot at position (0,0)
    set_of_unique_houses = {(0,0)} # initilise with the (0,0) starting location
    
    # Part B, santa and robot alternate directions
    i = 0  # initilise counter to track if odd or even for santa/robot to move    
    for ch in directions:
        if i%2 == 0: # if even number santa moves
            set_of_unique_houses, santas_position = single_move(set_of_unique_houses, ch, santas_position)
        else:  # if odd number robot moves
            set_of_unique_houses, robot_position = single_move(set_of_unique_houses, ch, robot_position)
        i += 1 # iterate between santa and robot santa moves
    number_unique_houses = len(set_of_unique_houses)
    print('The number of unique houses visited by Santa and Robot Santa is {}'.format(number_unique_houses))

def main():
    with open ("Day3_input_2015.txt", "r") as myfile:
        aoc_directions=myfile.readlines()[0] # Import directions as string
    count_unique_houses(aoc_directions)
    return 

if __name__ == "__main__":
   start_time = time.time() 
   main()
   end_time = time.time()
   duration = end_time - start_time
   print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
    

