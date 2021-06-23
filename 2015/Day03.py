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
start_time = time.time() #starts timer

#Import directions list. This requires the user to save the instructions
#as a text file called "Day3_input_2015.txt" in the same directory as the .py file
with open ("Day3_input_2015.txt", "r") as myfile:
    Directions=myfile.readlines()[0]

Santas_Position = (0,0) #intilise santa at position (0,0)
Robot_Position = (0,0) #intilise santa at position (0,0)
Set_of_Unique_Houses = {(0,0)}  #make set of tuples where each tuple is a house co-ordinate
#initilise set with the (0,0) starting location

def Single_Move(Houses_Set, Direction, Current_Location):
    if Direction == '^':
        New_Location = (Current_Location[0] + 1, Current_Location[1]) 
    elif Direction == 'v':
        New_Location = (Current_Location[0] - 1, Current_Location[1]) 
    elif Direction == '<':
        New_Location = (Current_Location[0], Current_Location[1] - 1) 
    else:
        New_Location = (Current_Location[0], Current_Location[1] + 1) 
    
    set.add(Houses_Set, New_Location) #adds to set only if new house location
    return Houses_Set, New_Location


#Solution for Part A
for ch in Directions:
   Set_of_Unique_Houses, Santas_Position = Single_Move(Set_of_Unique_Houses, ch, Santas_Position)
Number_Unique_Houses = len(Set_of_Unique_Houses)
print('The number of unique houses Santa visited is {}'.format(Number_Unique_Houses))
"""

#Solution for Part B
i = 0  #initilise counter to track if odd or even for santa/robot to move    
for ch in Directions:
    if i%2 == 0: #if even number
        Set_of_Unique_Houses, Santas_Position = Single_Move(Set_of_Unique_Houses, ch, Santas_Position)
    else:  #if odd number
        Set_of_Unique_Houses, Robot_Position = Single_Move(Set_of_Unique_Houses, ch, Robot_Position)
    i += 1 #iterate between santa and robot santa moves
Number_Unique_Houses = len(Set_of_Unique_Houses)
print('The number of unique houses visited by Santa and Robot Santa is {}'.format(Number_Unique_Houses))
"""
end_time = time.time()
duration = end_time - start_time
print('The code took {} milliseconds to execute'.format(1000*duration))