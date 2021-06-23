"""
Implement a bit wise circuit following instructions
Approach of finding commands that can be exectued and executing them, then repeat

This code requires python >3.7
"""

import time
import sys
import re


def instruction_reader(list_of_strings):
    '''parses instructions to list, and creates a dictionary of known variables and their values'''
    dict_known = {}
    instruction_array = []
    for entry in list_of_strings:
        words = entry.split()
        output = words[-1]  # The output is always the last word
        # Idenitfy the command given and the operands
        if 'AND' in entry:
            command = 'bit_and'
            op1 = words[0]
            op2 = words[2]
            add_int_to_dict(dict_known, [op1, op2])
        elif 'OR' in entry:
            command = 'bit_or'
            op1 = words[0]
            op2 = words[2]
            add_int_to_dict(dict_known, [op1, op2])
        elif 'NOT' in entry:
            command = 'bit_not'
            op1 = words[1]
            op2 = 'NA'  # doesnt exist for this command
            add_int_to_dict(dict_known, [op1])
        elif 'LSHIFT' in entry:
            command = 'bit_lshift'
            op1 = words[0]
            op2 = words[2]
            add_int_to_dict(dict_known, [op1])
        elif 'RSHIFT' in entry:
            command = 'bit_rshift'
            op1 = words[0]
            op2 = words[2]
            add_int_to_dict(dict_known, [op1])
        else:  # Only reamining possibility is set value
            command = 'bit_set'
            op1 = words[0]
            op2 = 'NA'  # doesnt exist for this command
            add_int_to_dict(dict_known, [op1])

        # append command and operands to instruction_array
        readable_instruction = [command, output, op1, op2]
        instruction_array.append(readable_instruction)
    return instruction_array, dict_known


def add_int_to_dict(input_dict, list_input_value):
    '''checks if operand is a number like 465 or an unknown variable name like 'gh'
       then adds number to dict of known. It is necessary for all integers to be in dict of known
       so when looping through commands, the code realises that ints are knowns.'''
    for input_value in list_input_value:
        if input_value.isnumeric():
            input_dict[input_value] = int(input_value)
    return None # This is a sub routine, it acts directly on inputs


def find_and_execute_possible_cmds(list_commands, dict_known):
    '''Loop through the list of commands and find commands that we can execute, and execute them'''
    for command in list_commands:
        if command[2] in dict_known:  # We know the first operator
            if command[0] in ['bit_and', 'bit_or']:  # Its an operation with 2 inputs
                if command[3] in dict_known:  # We know both operators
                    execture_cmd(command, list_commands, dict_known)
            else:  # its an operation with only 1 input
                execture_cmd(command, list_commands, dict_known)
    return None # This is a sub routine, it acts directly on inputs


def execture_cmd(single_cmd, list_commands, dict_known):
    '''Execute 'single_cmd' and remove that command from list, upadte dict of knowns'''
    if single_cmd[0] == 'bit_and':
        computed_value = dict_known[single_cmd[2]] & dict_known[single_cmd[3]]
    if single_cmd[0] == 'bit_or':
        computed_value = dict_known[single_cmd[2]] | dict_known[single_cmd[3]]
    if single_cmd[0] == 'bit_not':
        computed_value = ~dict_known[single_cmd[2]]
    if single_cmd[0] == 'bit_lshift':
        computed_value = dict_known[single_cmd[2]] << int(single_cmd[3])
    if single_cmd[0] == 'bit_rshift':
        computed_value = dict_known[single_cmd[2]] >> int(single_cmd[3])
    if single_cmd[0] == 'bit_set':
        computed_value = dict_known[single_cmd[2]]

    # Update dictionary and list of commands
    dict_known[single_cmd[1]] = computed_value  # add new known value to known dict
    list_commands.remove(single_cmd)
    return None # This is a sub routine, it acts directly on inputs


def part_2_override(instruction_array, a_value, dict_known):
    '''Add an instruction to set the value of b
    Find any instruction where the output is b and delete it'''
    # delete commands that give out put to b
    for entry in instruction_array:
        if entry[1] == 'b':
            instruction_array.remove(entry)

    # set value of b
    dict_known['b'] = a_value
    return None # This is a sub routine, it acts directly on inputs


start_time = time.time()
# Import instructions
with open('day7_input.txt', "r") as myfile:
    circuit_instructions = myfile.readlines()
parsed_instructions_1, known_variable_dict_1 = instruction_reader(circuit_instructions)

counter_1 = 0
while 'a' not in known_variable_dict_1:
    # print(f'Loop number {counter_1}, there are {len(parsed_instructions_1)} commands left to process')
    find_and_execute_possible_cmds(parsed_instructions_1, known_variable_dict_1)
    counter_1 += 1
print('For part 1, the value of a is {}'.format(known_variable_dict_1['a']))

# Re initilise for part two
parsed_instructions_2, known_variable_dict_2 = instruction_reader(circuit_instructions)
part_2_override(parsed_instructions_2, known_variable_dict_1['a'], known_variable_dict_2)
counter_2 = 0
while 'a' not in known_variable_dict_2:
    # print(f'Part 2 Loop number {counter_2}, there are {len(parsed_instructions_2)} commands left to process')
    find_and_execute_possible_cmds(parsed_instructions_2, known_variable_dict_2)
    counter_2 += 1
print('For part 2 the value of a is {}'.format(known_variable_dict_2['a']))

end_time = time.time()
duration = end_time - start_time

print('The code took {:.2f} milliseconds to execute'.format(1000 * duration))
