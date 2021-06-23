"""
Baking (Integer Non Linear Programming - Integer Optimisation)

This is a non lienar problem as the qualities are multiplied together
also there is an if statement if quality < 0, set quality = 0

Gekko weaknesses
1. I cant get it to do if statements

"""
import time
import numpy as np
from gekko import GEKKO

def instruction_parser(single_string):
    words = single_string.split()
    ingredient = words[0].strip(':')
    capacity = int(words[2].strip(','))
    durability = int(words[4].strip(','))
    flavor = int(words[6].strip(','))
    texture = int(words[8].strip(','))
    calories = int(words[10])
    return [ingredient, capacity, durability, flavor, texture, calories]


def ing_qualities_matrix(ingredient_qualities):
    num_ingredients = len(ingredient_qualities)
    num_qualities = len(ingredient_qualities[0])-1
    coefficients_matrix = np.zeros([num_ingredients, num_qualities])
    ing_names_list = []
    for count, ingredient in enumerate(ingredient_qualities):
        coefficients_matrix[count] = ingredient[1:]
        ing_names_list.append(ingredient[0])
    return coefficients_matrix, ing_names_list


def gekko_solver(coef, ing_names):
    m = GEKKO()  # Initialize gekko
    m.options.SOLVER = 1  # APOPT is an MINLP solver

    # Initialize variables
    num_ing = len(ing_names)
    ing1, ing2, ing3, ing4 = [m.Var(value=round(100/num_ing), lb=0, ub=100, integer=True) for i in range(num_ing)]

    # Calculate mixture properties
    recipe = np.array([ing1, ing2, ing3, ing4])
    qualities = np.dot(recipe, coef)

    '''
    # If statements wont work for me with Gekko,
    # Gekko actually turns python equations into strings for the .apm model, and this is where it fails...
    if qualities[0] <= 0:
        qualities[0] = 0
    if qualities[1] <= 0:
        qualities[1] = 0
    if qualities[2] <= 0:
        qualities[2] = 0
    if qualities[3] <= 0:
        qualities[3] = 0
        
    Similarly using np operations doesnt work
    qualities[qualities < 0] = 0
    
    I think the problem is the '<' operator
    '''

    # Constraints
    m.Equation(ing1 + ing2 + ing3 + ing4 == 100)
    m.Equation(qualities[4] == 500)
    m.Equation(qualities[0] >= 0)
    m.Equation(qualities[1] >= 0)
    m.Equation(qualities[2] >= 0)
    m.Equation(qualities[3] >= 0)

    # Objective Function
    m.Obj(-qualities[0:-1].prod())  # We minimise this, hence negative to get maximum
    m.solve(disp=False)  # Solve

    print('Results')
    print(f'{ing_names[0]}: ' + str(ing1.value))
    print(f'{ing_names[1]}: ' + str(ing2.value))
    print(f'{ing_names[2]}: ' + str(ing3.value))
    print(f'{ing_names[3]}: ' + str(ing4.value))
    print('Objective: ' + str(-m.options.objfcnval))

    return None


if __name__ == "__main__":
    start_time = time.time()

    parsed_instructions = []
    with open('Day15_input.txt', "r") as myfile:
        for instruction in myfile:
            parsed_instructions.append(instruction_parser(instruction))
    ing_coeffs, ing_list = ing_qualities_matrix(parsed_instructions)

    gekko_solver(ing_coeffs, ing_list)

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} seconds to execute'.format(duration))
