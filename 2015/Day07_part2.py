"""
Implement a bit wise circuit following instructions
The big challenge is sorting the instruction orders so that all the
instructions can be executed in the right order

This code requires python > 3.7
"""

import time
import re
import sys

# parses instructions to list, and creates set of unknown variables and a dictionary of known variables and their values
def instruction_reader(list_of_strings):
    set_unknown = set()
    dict_known ={}
    instruction_array = []
    for entry in list_of_strings:
        words = entry.split()
        # Idenitfy the command given and the operands
        if 'AND' in entry:
            command = 'bit_and'
            output = words[4]
            op1 = words[0]
            op2 = words[2]
            add_to_set_or_dict(dict_known, set_unknown, [op1, op2, output])
        elif 'OR' in entry:
            command = 'bit_or'
            output = words[4]
            op1 = words[0]
            op2 = words[2]
            add_to_set_or_dict(dict_known, set_unknown, [op1, op2, output])
        elif 'NOT' in entry:
            command = 'bit_not'
            output = words[3]
            op1 = words[1]
            op2 = 'NA'  # doesnt exist for this command
            add_to_set_or_dict(dict_known, set_unknown, [op1, output])
        elif 'LSHIFT' in entry:
            command = 'bit_lshift'
            output = words[4]
            op1 = words[0]
            op2 = words[2]
            add_to_set_or_dict(dict_known, set_unknown, [op1, output])
        elif 'RSHIFT' in entry:
            command = 'bit_rshift'
            output = words[4]
            op1 = words[0]
            op2 = words[2]
            add_to_set_or_dict(dict_known, set_unknown, [op1, output])
        else:  # Only reamining possibility is set value
            command = 'bit_set'
            output = words[2]
            op1 = words[0]
            op2 = 'NA'  # doesnt exist for this command
            add_to_set_or_dict(dict_known, set_unknown, [op1, output])

        # append command and operands to instruction_array
        readable_instruction = [command, output, op1, op2]
        instruction_array.append(readable_instruction)
    return instruction_array, set_unknown, dict_known

    
# checks if operand is a number like 465 or an unknown variable name like 'gh'
# then adds number to dict of known, adds variable name to set of unknown 
def add_to_set_or_dict(input_dict, input_set, list_input_value):
    number_pattern = re.compile(r'\d')
    for input_value in list_input_value:
        reg_check = bool(number_pattern.match(input_value))
        if reg_check is True:
            input_dict[input_value] = int(input_value)
        else:
            input_set.add(input_value)
    return input_dict, input_set


# Find commands that we can execute
def find_possible_cmds(list_commands, dict_known):
    possible_instructions = []
    for command in list_commands:
        if command[2] in dict_known:  # We know the first operator
            if command[0] in ['bit_and', 'bit_or']:  # Its an operation with 2 inputs
                if command[3] in dict_known:  # We know both operators
                    possible_instructions.append(command)
            else:  # its an operation with only 1 input
                possible_instructions.append(command)
    return possible_instructions


# Execute command and remove command from list, upadte set of unknown and dict of knowns
def execture_cmd(list_commands, possible_commands, set_unknown, dict_known):
    for possible_cmd in possible_commands:
        if possible_cmd[0] == 'bit_and':
            computed_value = bitwise_and_gate(dict_known[possible_cmd[2]], dict_known[possible_cmd[3]])
        if possible_cmd[0] == 'bit_or':
            computed_value = bitwise_or_gate(dict_known[possible_cmd[2]], dict_known[possible_cmd[3]])
        if possible_cmd[0] == 'bit_not':
            computed_value = bitwise_not_gate(dict_known[possible_cmd[2]])
        if possible_cmd[0] == 'bit_lshift':
            computed_value = bitwise_left_gate(dict_known[possible_cmd[2]], int(possible_cmd[3]))
        if possible_cmd[0] == 'bit_rshift':
            computed_value = bitwise_right_gate(dict_known[possible_cmd[2]], int(possible_cmd[3]))
        if possible_cmd[0] == 'bit_set':
            computed_value = dict_known[possible_cmd[2]]
             
        # Update dictionary, set and list of commands
        dict_known[possible_cmd[1]] = computed_value  # add new known value to known dict
        set_unknown.remove(possible_cmd[1])  # remove new known value from unknown set
        list_commands.remove(possible_cmd)
    return list_commands, set_unknown, dict_known


def decimal_to_binary_string(decimal_num):
    binary_string = bin(decimal_num).replace("0b", "")  # returns a string
    binary16bit_str = binary_string.zfill(16)  # adds leading 0s so len = 16
    return binary16bit_str


def bitwise_and_gate(decimal_a, decimal_b):
    and_output = decimal_a & decimal_b  # applies bit wise operation to decimal inputs
    return and_output


def bitwise_or_gate(decimal_a, decimal_b):
    or_output = decimal_a | decimal_b  # applies bit wise operation to decimal inputs
    return or_output


# Need to specify that this is a 16 bit signal
def bitwise_not_gate(decimal_in):
    binary_str = decimal_to_binary_string(decimal_in)
    binary_temp1 = binary_str.replace('0', '2')
    binary_temp2 = binary_temp1.replace('1', '0')
    binary_not = binary_temp2.replace('2', '1')
    not_output = int(binary_not, 2)
    return not_output


def bitwise_left_gate(decimal_in, steps):
    left_output = decimal_in << steps  # applies bit wise operation to decimal inputs
    return left_output


def bitwise_right_gate(decimal_in, steps):
    right_output = decimal_in >> steps  # applies bit wise operation to decimal inputs
    return right_output


# Add an instruction to set the value of b
# Find any instruction where the output is b and delete it
def part_2_override(instruction_array, a_value, dict_known):
    # delete commands that give out put to b
    for entry in instruction_array:
        if entry[1] == 'b':
            instruction_array.remove(entry)
            print('removing command that used to give value to B')

    # set value of b
    dict_known['b'] = a_value
    return instruction_array, dict_known

    
if __name__ == "__main__":
    start_time = time.time()

    if len(sys.argv) != 2:
        print('Error, the required format is python pyfile.py file.txt')
    else:
        # Import instructions
        with open("Day7_input.txt", "r") as myfile:
            circuit_instructions = myfile.readlines()
        parsed_instructions_1, set_of_unknown_variables_1, known_variable_dict_1 = instruction_reader(circuit_instructions)
        
        counter_1 = 0
        while 'a' in set_of_unknown_variables_1:
            print(f'Part 1 Loop number {counter_1}, there are {len(set_of_unknown_variables_1)} unknown variables and {len(parsed_instructions_1)} commands left to process')
            test_possibles_1 = find_possible_cmds(parsed_instructions_1, known_variable_dict_1)
            parsed_instructions_1, set_of_unknown_variables_1, known_variable_dict_1 = execture_cmd(parsed_instructions_1, test_possibles_1, set_of_unknown_variables_1, known_variable_dict_1)
            counter_1 += 1
        print('For part 1 the value of a is {}'.format(known_variable_dict_1['a']))
    
        # Re initilise for part two
        parsed_instructions_2, set_of_unknown_variables_2, known_variable_dict_2 = instruction_reader(circuit_instructions)
        parsed_instructions_2, known_variable_dict_2 = part_2_override(parsed_instructions_2, known_variable_dict_1['a'], known_variable_dict_2)
        counter_2 = 0
        while 'a' in set_of_unknown_variables_2:
            print(f'Part 2 Loop number {counter_2}, there are {len(set_of_unknown_variables_2)} unknown variables and {len(parsed_instructions_2)} commands left to process')
            test_possibles_2 = find_possible_cmds(parsed_instructions_2, known_variable_dict_2)
            parsed_instructions_2, set_of_unknown_variables_2, known_variable_dict_2 = execture_cmd(parsed_instructions_2, test_possibles_2, set_of_unknown_variables_2, known_variable_dict_2)
            counter_2 += 1
        
        end_time = time.time()
        duration = end_time - start_time
        print('For part 2 the value of a is {}'.format(known_variable_dict_2['a']))
        print('The code took {:.2f} milliseconds to execute'.format(1000*duration))
