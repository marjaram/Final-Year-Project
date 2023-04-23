##################################################### IMPORTS #######################################################
import math
import sys
import numpy as np
import pandas as pd
import ast
import logging
import placement
import copy
seed = np.random.default_rng()
logger = logging.getLogger('my_module_name')
logging.basicConfig(filename='log.log',filemode='w', encoding='utf-8', level=logging.DEBUG)

training_set = pd.read_csv('training_set.csv')['Item sets']
training_set = training_set.apply(lambda x: ast.literal_eval(x))

testing_set = pd.read_csv('testing_set.csv')['Item sets']

############################################# AUXILIARY AND SINGLE SELECTION FUNCTIONS #######################################################
def fitness_function(object_list): 
    fraction_util = 0
    for object in object_list:
        fraction_util += ((np.count_nonzero(object[0]))/(BIN_HEIGHT*BIN_WIDTH))**2
    fitness = fraction_util/len(object_list)

    return fitness


def single_ff(outer_bin_dict, outer_objects, item, i, BIN_WIDTH, BIN_HEIGHT):
    bin_dict = copy.deepcopy(outer_bin_dict)
    objects = copy.deepcopy(outer_objects)

    j = seed.choice([1,3,5,7,9]) # j-value determines colour of piece in display

    # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
    can_place = False 
    for o in range(len(objects)):
        object, success_flag = placement.bottom_left(objects[o], item, j)
        if success_flag == 1:
            can_place = True

            # Update return variables
            objects[o] = object
            bin_dict[f'{o}'].append(item)
            current_object = o
            break

    # Cannot fit in any bin. Create a new bin and place the item.
    if not can_place:
        objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
        object, success_flag = placement.bottom_left(objects[-1], item, j)
        if success_flag == 1:
            objects[-1] = object
            bin_dict[f'{o+1}'] = [item]
            current_object = o + 1
        else:
            logging.info(f'Fatal error, item {i}:{item} larger than bin')
    return objects, bin_dict, current_object


def single_nf(outer_bin_dict, outer_objects, item, i, current_object, BIN_WIDTH, BIN_HEIGHT):
    bin_dict = copy.deepcopy(outer_bin_dict)
    objects = copy.deepcopy(outer_objects)

    j = seed.choice([1,3,5,7,9]) # j-value determines colour of piece in display

    # Try to place in current object
    can_place = False 
    object, success_flag = placement.bottom_left(objects[current_object], item, j)
    if success_flag == 1:
        can_place = True

        # Update return variables
        bin_dict[f'{current_object}'].append(item)
        objects[current_object] = object

    # If cannot, iterate through other objects
    if not can_place:
        for o in range(len(objects)-1):
            new_current_object = (current_object + o + 1) % len(objects)
            object, success_flag = placement.bottom_left(objects[new_current_object], item, j)
            if success_flag == 1:
                can_place = True

                # update return variables
                bin_dict[f'{new_current_object}'].append(item)
                objects[new_current_object] = object
                new_current_object = current_object
                break
        # If cannot place in any other object, create new object and place there
        if not can_place:
            objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
            current_object = len(objects) - 1
            object, success_flag = placement.bottom_left(objects[current_object], item, j)
            if success_flag == 1:
                # Update return variables
                bin_dict[f'{len(objects) - 1}'] = [item]
                objects[current_object] = object
            else:
                logging.info(f'Fatal error, item {i}:{item} larger than bin')

    return objects, bin_dict, current_object


def single_bf(outer_bin_dict, outer_objects, item, i, BIN_WIDTH, BIN_HEIGHT):
    bin_dict = copy.deepcopy(outer_bin_dict)
    objects = copy.deepcopy(outer_objects)

    j = seed.choice([1,3,5,7,9]) # j-value determines colour of piece in display

    # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
    can_place = False 
    best_bin = objects[0]
    waste = BIN_WIDTH * BIN_HEIGHT

    for o in range(len(objects)):
        object, success_flag = placement.bottom_left(objects[o], item, j)
        if success_flag == 1:
            can_place = True
            if (BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(object[0])) < waste:
                best_bin_index = o
                best_bin = object
                waste = BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(object[0])
    
    if can_place:
        # update return variables
        bin_dict[f'{best_bin_index}'].append(item)
        objects[best_bin_index] = best_bin
        current_object = best_bin_index

    if not can_place:
        objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
        object, success_flag = placement.bottom_left(objects[-1], item, j)
        if success_flag == 1:
            current_object = len(objects) - 1
            objects[-1] = object
            bin_dict[f'{o+1}'] = [item]
        else:
            logging.info(f'Fatal error, item {i}:{item} larger than bin')
    return objects, bin_dict, current_object


def single_djd(outer_bin_dict, outer_objects, problems, current_bin, BIN_WIDTH, BIN_HEIGHT):

    # make deepcopies of everything
    bin_dict = copy.deepcopy(outer_bin_dict)
    objects = copy.deepcopy(outer_objects)
    items = copy.deepcopy(problems)
    current_object = copy.deepcopy(current_bin)

    j = seed.choice([1,3,5,7,9]) # j-value determines colour of piece in display
    waste = 0
    w = BIN_WIDTH * BIN_HEIGHT / 20
    
    # sort items by decreasing area
    areas = [[x[0] * x[1], x] for x in items]
    areas.sort(reverse=True)
    items = [area[1] for area in areas]
    for o in range(len(objects)):
        failed = []
        ofa = BIN_HEIGHT * BIN_WIDTH - np.count_nonzero(objects[current_object][0])
        while waste <= ofa:
            for item in items:
                # If current bin is filled < 1/3, try to place the piece
                if np.count_nonzero(objects[current_object][0]) < (BIN_WIDTH * BIN_HEIGHT / 3):
                    object, success_flag = placement.bottom_left(objects[current_object], item, j)
                    if success_flag == 1:
                        items.remove(item)
                        bin_dict[f'{current_object}'].append(item)
                        objects[current_object] = object
                        return objects, bin_dict, items, current_object
                    else:
                        failed.append(item)
                
                item_area = item[0] * item[1]
                if ofa - item_area > waste:
                    break # item is too small to fill free area, need to increment waste

                if (item_area > ofa) or item in failed:
                    continue # item is too big/doesn't fit, get next smallest item

                object, success_flag = placement.bottom_left(objects[current_object], item, j)
                if success_flag == 1:
                    items.remove(item)
                    bin_dict[f'{current_object}'].append(item)
                    objects[current_object] = object
                    return objects, bin_dict, items, current_object
                else:
                    failed.append(item)
            waste += w
        current_object = (current_object + 1) % len(objects)

    # All bins have failed, create a new bin and place item there
    item = items[0]
    objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
    object, success_flag = placement.bottom_left(objects[-1], item, j)
    if success_flag == 1:
        current_object = len(objects) - 1
        objects[current_object] = object
        bin_dict[f'{current_object}'] = [item]
        items.remove(item)                
        return objects, bin_dict, items, current_object
    else:
        logging.info(f'Fatal error, item {i}:{item} larger than bin')
    return objects, bin_dict, items, current_object
############################################# PARAMETERS #######################################################
# GLOBAL (NEED TO CHANGES ACROSS MULTIPLE PROGRAMS)
BIN_WIDTH = 100
BIN_HEIGHT = 100
NUM_RECTANGLES = 20

# SPECIFIC (JUST FOR GENETIC ALGORITHM)
population_size = 25
seeding = False 
problems_per_round = 5
############################################# GENETIC ALGORITHM #######################################################


# GENERATE INITIAL POPULATION
if not seeding: # RANDOMLY
    initial_population = []
    for i in range(population_size):
        initial_chromosome = [seed.integers(0,7) for i in range(NUM_RECTANGLES)]
        initial_population.append(initial_chromosome)
else:
    pass

# MAIN LOOP
    # CALCULATE FITNESS - sample 5 problems from training set. For each problem, run the single-item selection heuristics.

fitnesses = []
for i in range(100):
    logging.info(f'Problem {i}')
    print(f'Problem {i}')
    # Randomly sample a problem from the training set
    problem = copy.deepcopy(training_set[seed.integers(0,len(training_set))])
    bin_dict = {'0':[]}
    objects =  [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]
    # Solve problem using the heuristics in the chromosome
    chromosome = initial_population[0]
    round = 0
    current_bin = 0
    while round < NUM_RECTANGLES:
        logging.info(f'Round {round}: {len(problem)} items remaining')
        solution = chromosome[round]
        # logging.info('Descending')
        if solution in [1,3,5]: # choose largest remaining piece by area
            areas = [[x[0] * x[1], x] for x in problem]
            areas.sort(reverse=True)
            item = areas[0][1]
            problem.remove(item)
        elif solution in [0,2,4]:
            item = problem.pop(0) # instead choose first piece in queue

        if solution in [0,1]:
            # logging.info('First Fit')
            objects, bin_dict, current_bin = single_ff(bin_dict, objects, item, round, BIN_WIDTH, BIN_HEIGHT)

        elif solution in [2,3]:
            # logging.info('Next Fit')
            objects, bin_dict, current_bin = single_nf(bin_dict, objects, item, round, current_bin, BIN_WIDTH, BIN_HEIGHT)
        
        elif solution in [4,5]:
            # logging.info('Best Fit')
            objects, bin_dict, current_bin = single_bf(bin_dict, objects, item, round, BIN_WIDTH, BIN_HEIGHT)

        elif solution == 6:
            # logging.info('DJD')
            objects, bin_dict, problem, current_bin = single_djd(bin_dict, objects, problem, current_bin, BIN_WIDTH, BIN_HEIGHT)
            pass

        # logging.info(bin_dict)
        round += 1

    fitnesses.append(fitness_function(objects))

fitnesses_series = pd.Series(fitnesses)
print(fitnesses_series.describe())

    # PARENT SELECTION
    # CROSSOVER
    # MUTATION
