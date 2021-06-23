"""
Advent of Code 2015, Day 1

Part A Problem Description 
Santa starts on floor 0, and is given an instruction file of ( and ) 
where( means go up and ) means go down one floor
the apratment goes from -infinity to +infinity
find out what floor santa ends on for a given set of instructions
"""
import time
start_time = time.time() #starts timer


#Import instructions to a string. This requires the user to save the instructions
#as a text file called "Day1_input_2015.txt" in the same directory as the .py file
with open ("Day1_input.txt", "r") as myfile:
    Instructions=myfile.readlines()[0]


Number_ups = Instructions.count('(')  #counts the number of times '(' appears in the instructions
Number_downs = Instructions.count(')')  #counts the number of times ')' appears in the instructions
Final_location = Number_ups - Number_downs
print('Santas final location is the {} floor'.format(Final_location))

"""
Part B Problem Description
Find the position of the first character that causes santa to enter the basement floor -1
The problem defines the first character in the instructions as position 1, not position 0
"""

def Enter_Basement_Identifier(Instruction_string):
    """Function that returns the position of the first character that makes Santa
    enter the basement. The input is the instruction string, the output is an integer
    already compensated for python list starting at index 0"""
    Current_Location = 0 #Initilise Santa's current location to 0
    Instruction_position = 1 #Initilise Instructor position to 1 for the first character
    for ch in Instruction_string:  #loop over characters in instruction string
    
        #for each instruction update santas current position    
        if ch == '(':
            Current_Location += 1
        else:  #there are only two options
            Current_Location -= 1
        
        #for each instruction check if we are at basement 
        if Current_Location == -1:
            break
        else:
            Instruction_position += 1
            
    return Instruction_position

Position_Instruction_to_Basement = Enter_Basement_Identifier(Instructions)
print('Santas enters the basement on the {} instruction'.format(Position_Instruction_to_Basement))


end_time = time.time()
duration = end_time - start_time
print('The code took {} milliseconds to execute'.format(1000*duration))