"""
Baking (Integer Non Linear Programming - Integer Optimisation)

This is a non lienar problem as the qualities are multiplied together
also there is an if statement if quality < 0, set quality = 0

I solved it ignoring the integer rules, hoping that by rounding my
continuous values to integer values I would get the optimum result.
This is not always true, in fact often after rounding the teaspoons you are
left with just 99 teaspoons. I probably need a better method


"""
import time
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, minimize
import sys


def instruction_parser(single_string):
    '''
    :param single_string: a single string from the input file
    :return: parsed integer values from input string
    '''''
    words = single_string.split()
    ingredient = words[0].strip(':')
    capacity = int(words[2].strip(','))
    durability = int(words[4].strip(','))
    flavor = int(words[6].strip(','))
    texture = int(words[8].strip(','))
    calories = int(words[10])
    return [ingredient, capacity, durability, flavor, texture, calories]


def ing_qualities_matrix(ingredient_qualities):
    '''
    Creates a np array with the ingredients in the rows and the qualities in columns
    :param ingredient_qualities: list of lists, showing qualities of each ingredient
    :return: np matrix
    '''''
    num_ingredients = len(ingredient_qualities)
    num_qualities = len(ingredient_qualities[0])-1
    coefficients_matrix = np.zeros([num_ingredients, num_qualities])
    for count, ingredient in enumerate(ingredient_qualities):
        coefficients_matrix[count] = ingredient[1:]
    return coefficients_matrix


def mixture_proprties(coefficients_matrix, recipe):
    '''
    applies dot product to calculate capcaity, durability etc of cookies
    for a given recipe
    :param coefficients_matrix: np.array of qualities of each ingredient
    :param recipe: np.vector of number of teaspoons of each ingredient, must sum to 100
    :return: np.vector of resulting mixture qualities
    '''
    mix_qual = np.dot(recipe, coefficients_matrix)
    return mix_qual


def objective_calculator(recipe, coefficients_matrix, max_min):
    '''My solver can only do minimise, so to maximise the value, we instead
    try to minimise the negative of the value. Since I sometimes want to find
    the value and sometimes I want the negative value, I use the max_min
    parameter which will be -1 during optimisation and +1 otherwise'''
    mix_qual = mixture_proprties(coefficients_matrix, recipe)
    useful_qual = mix_qual[0:-1]
    useful_qual[useful_qual < 0] = 0  # makes negative values 0
    obj_value = max_min * np.prod(useful_qual)
    return obj_value


def continuous_solver(coefficients_matrix):
    '''
    This optimises the ingredients according to the objective function and a set of linear constraints
    but this is a continuous optimiser so it returns floats not integers, therefore I need to round my answer,
    sometimes this results in the teaspoons being dropped to below 100, so I need to add one back. This is not
    the best way to solve this problem but I couldnt find a suitable integer programming solver.
    :param coefficients_matrix: np array of ingredient qualities
    :return: optimum ingredients as a np array
    '''
    num_ing = coefficients_matrix.shape[0]

    my_bounds = Bounds(np.zeros(num_ing),
                       np.full(num_ing, 100),
                       )

    # in constraints below, first list is coefficients of x1 and x2, second list is equaltiy, that sum <100 and >100
    my_lin_constraints = LinearConstraint(A=np.ones(num_ing), lb=100, ub=100)
    calory_constraint = LinearConstraint(A = ing_coeffs[:,-1], lb=500, ub=500)

    initial_guess = np.full(num_ing, 100/num_ing)

    # This is a continuous optimiser, not an integer one so it returns floats
    optimiser_result = minimize(objective_calculator, initial_guess,
                                args=(ing_coeffs, -1), method='trust-constr',
                                constraints=(my_lin_constraints, calory_constraint),
                                options={'verbose': 0}, bounds=my_bounds)

    continuous_teaspoons = optimiser_result.x
    # continuous_value = optimiser_result.fun  # Minimised function value
    rounded_teaspoons = np.round(continuous_teaspoons)

    # since I used a non integer approach, sometimes the rounding drops teaspoons down to 99
    if sum(rounded_teaspoons) < 100:
        print('rounding resulted in less than 100 teaspoons, need to bump one up')
        decimals = continuous_teaspoons - np.round(continuous_teaspoons)
        nearest_full = np.argmax(decimals)
        rounded_teaspoons[nearest_full] += 1
    rounded_value = objective_calculator(rounded_teaspoons, ing_coeffs, 1)

    rounded_qual = mixture_proprties(coefficients_matrix, rounded_teaspoons)
    if rounded_qual[-1] != 500:
        print('Uh oh, my recipe has {} calories which is not exactly 500'.format(rounded_qual[-1]))
        print('Using a continuous solver is not a good solution to this problem')

    return rounded_value


if __name__ == "__main__":
    start_time = time.time()

    input_file = 'Day15_input.txt'

    if len(sys.argv) == 2:
        input_file = sys.argv[1]

    parsed_instructions = []
    with open(input_file, "r") as myfile:
        for instruction in myfile:
            parsed_instructions.append(instruction_parser(instruction))
    ing_coeffs = ing_qualities_matrix(parsed_instructions)

    optimal_recipe = continuous_solver(ing_coeffs)
    print('The score for part 2 is {}'.format(optimal_recipe))

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} seconds to execute'.format(duration))
