"""
Implement a bit wise circuit following instructions
Recursive approach assisted by spyder debugger
"""

import time


def instruction_reader(list_of_strings):
    '''creates dictionary of instructions and dictionary of wire values'''
    dict_instructions = {}
    dict_values = {}
    for entry in list_of_strings:
        instruction = entry.strip().split(' -> ') # note we are splitting on space arrow to remove white space
        output = instruction[1]  # The output is always the last word
        dict_instructions[output] = instruction[0]
        dict_values[output] = 'unknown'
    return dict_instructions, dict_values


def get_wire_value(target):
    '''calculates target value by recursvie method'''
    #  Step 1 check if this is a wire name or a number
    if target not in wire_values:
        # its a number value as a string input like '1943'
        return int(target)
    else: # its a wire name 
        # Step 2 check if we already know the value of this wire
        # my if statement is not working...
        if wire_values[target] == 'unknown': # we need to calculate it
            # Step 3 find instruction for target, then find operands labels
            instruction = wire_instructions[target]
            [op_label1, op_label2, cmd] = operand_finder(instruction)
            #  Step 4 get value of the operands, this is the recursive part
            op1_value = get_wire_value(op_label1)
            op2_value = get_wire_value(op_label2)
            #  Step 5 Now that we know value of both operands, lets compute target value
            target_value = bit_compute(op1_value, op2_value, cmd)
            #  Step 6 Add newly calculated value to dict_values
            wire_values[target] = target_value
            return target_value  # this is the ultiamte exit of the recurisve function
        else: # we already know it, so just return its value
            return wire_values[target]  


def operand_finder(single_cmd):
    ''' returns the operands from the instruction, if the instruction is of
    the type that only has 1 operand, it returns 0 as the 2nd operand'''
    words = single_cmd.split()
    # Idenitfy the command given and the operands
    if 'AND' in words:
        command = 'bit_and'
        op1 = words[0]
        op2 = words[2]
    elif 'OR' in words:
        command = 'bit_or'
        op1 = words[0]
        op2 = words[2]
    elif 'NOT' in words:
        command = 'bit_not'
        op1 = words[1]
        op2 = '0'
    elif 'LSHIFT' in words:
        command = 'bit_left'
        op1 = words[0]
        op2 = words[2]
    elif 'RSHIFT' in words:
        command = 'bit_right'
        op1 = words[0]
        op2 = words[2]
    else:  # Only reamining possibility is set value
        command = 'bit_set'
        op1 = words[0]
        op2 = '0'
    return [op1, op2, command]


def bit_compute(operand1, operand2, cmd):
    if cmd == 'bit_and':
        value = operand1 & operand2
    if cmd == 'bit_or':
        value = operand1 | operand2
    if cmd == 'bit_not':
        value = ~operand1
    if cmd == 'bit_left':
        value = operand1 << operand2
    if cmd == 'bit_right':
        value = operand1 >> operand2
    if cmd == 'bit_set':
        value = operand1
    return value


start_time = time.time()  
# Import instructions
with open('Day7_input.txt', "r") as myfile:
    circuit_instructions = myfile.readlines()
wire_instructions, wire_values = instruction_reader(circuit_instructions)

answer = get_wire_value('a')


end_time = time.time()
duration = end_time - start_time
print('The answer is {:.2f}'.format(answer))
print('The code took {:.2f} milliseconds to execute'.format(1000 * duration))
