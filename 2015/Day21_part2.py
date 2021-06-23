'''
Day 21 Advent of Code, RPG
could I remove np, I dont make much use of it...
can I make this smarter and not use brute force?
'''

import sys
import time
import numpy as np
import math

PLAYER_HITPOINTS = 100
WEAPONS = np.array([
                    [8, 4, 0],
                    [10, 5, 0],
                    [25, 6, 0],
                    [40, 7, 0],
                    [74, 8, 0],
                    ])

# row of 0s allows you not to buy armour
ARMOUR = np.array([
                [0, 0, 0],
                [13, 0, 1],
                [31, 0, 2],
                [53, 0, 3],
                [75, 0, 4],
                [102, 0, 5],
            ])

# 2 rows of 0s allows you not to any rings
RINGS = np.array([
                [0, 0, 0],
                [0, 0, 0],
                [25, 1, 0],
                [50, 2, 0],
                [100, 3, 0],
                [20, 0, 1],
                [40, 0, 2],
                [80, 0, 3],
            ])

WEAPONS_NAMES = ['Dagger','Shortsword',
                 'Warhammer', 'Longsword', 'Greataxe']
ARMOUR_NAMES = ['naked', 'Leather', 'Chainmail',
                'Splintmail', 'Bandedmail', 'Platemail']
RING_NAMES = ['bare_fingered', 'DAM+1', 'DAM+2', 'DAM+3',
              'DEF+1', 'DEF+2', 'DEF+3']


def parser(file_loc):
    '''
    Reads input and returns boss stats as list
    [hit points, damage, armour]
    '''
    boss_stats = []
    with open(file_loc, "r") as myfile:
        for line in myfile:
            boss_stats.append(int(line.split()[-1]))
    return boss_stats


def shop(purchases):
    ''' pick your weapon, shield and ring, computes cost '''
    weapon = WEAPONS[purchases[0], :]
    shield = ARMOUR[purchases[1], :]
    left_ring = RINGS[purchases[2], :]
    right_ring = RINGS[purchases[3], :]
    cost = WEAPONS[purchases[0], 0] + ARMOUR[purchases[1], 0] + RINGS[purchases[2], 0] + RINGS[purchases[3], 0]
    return weapon, shield, left_ring, right_ring, cost


def player_calculator(weapon, shield, left_ring, right_ring):
    '''calculates player stats'''
    combined_bonus = weapon + shield + left_ring + right_ring
    return [PLAYER_HITPOINTS, combined_bonus[1], combined_bonus[2]]


def battle(player_stats, boss_stats):
    ''' returns true if player defeats boss '''
    player_dies = math.ceil(player_stats[0]/max(1, (boss_stats[1]-player_stats[2])))
    boss_dies = math.ceil(boss_stats[0]/max(1, (player_stats[1]-boss_stats[2])))
    if player_dies >= boss_dies:
        return True
    return False


def main(file_loc):
    boss_values = parser(file_loc)

    cheapest_win = 1000
    most_expensive_lost = 0
    worst_equipment = [0, 0, 0, 0]
    best_equipment = [0, 0, 0, 0]

    for i in range(len(WEAPONS[:, 0])):
        for j in range(len(ARMOUR[:, 0])):
            for k in range(len(RINGS[:, 0])):
                for m in range(len(RINGS[:, 0])):
                    if k == m:
                        continue
                    purchase = [i, j, k, m]
                    weaponry, defence, l_jewels, r_jewels, gold = shop(purchase)
                    player_attributes = player_calculator(weaponry, defence, l_jewels, r_jewels)
                    victory = battle(player_attributes, boss_values)
                    if victory:
                        if gold < cheapest_win:
                            cheapest_win = gold
                            best_equipment = purchase
                    else:
                        if gold > most_expensive_lost:
                            most_expensive_lost = gold
                            worst_equipment = purchase
    return cheapest_win, best_equipment, most_expensive_lost, worst_equipment


if __name__ == '__main__':
    start_time = time.time()
    input_file = 'Day21_input.txt'

    if len(sys.argv) >= 2:
        input_file = sys.argv[1]

    best_value, optimum_equipment, worst_value, terrible_equipment = main(input_file)
    print('the cheapest equipment required to win costs {}'.format(best_value))
    print('the optimum equipment is {}, {}, {} and {}'.format(WEAPONS_NAMES[optimum_equipment[0]], \
                                                              ARMOUR_NAMES[optimum_equipment[1]], \
                                                              RING_NAMES[optimum_equipment[2]], \
                                                              RING_NAMES[optimum_equipment[3]]))

    print('the dearest equipment that still loses costs {}'.format(worst_value))
    print('the worst equipment is {}, {}, {} and {}'.format(WEAPONS_NAMES[terrible_equipment[0]], \
                                                              ARMOUR_NAMES[terrible_equipment[1]], \
                                                              RING_NAMES[terrible_equipment[2]], \
                                                              RING_NAMES[terrible_equipment[3]]))

    end_time = time.time()
    duration = end_time - start_time
    print('The code took {:.2f} seconds to execute'.format(duration))
