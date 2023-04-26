import sys
import numpy as np
import pandas as pd
import copy
import placement
import logging
import ast
seed = np.random.default_rng(52)

testing_set_df = pd.read_csv('testing_set.csv')
testing_set_df['Item sets'] = testing_set_df['Item sets'].apply(lambda x: ast.literal_eval(x))
testing_set = testing_set_df['Item sets']
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

# GLOBAL (NEED TO CHANGES ACROSS MULTIPLE PROGRAMS)
BIN_WIDTH = 100
BIN_HEIGHT = 100
NUM_RECTANGLES = 20

# SPECIFIC (JUST FOR GENETIC ALGORITHM)
testing_population_size = 5
seeding = False 
problems_per_round = 20
elitism = 0.1 # Fraction which are transferred to the next generation unchanged, or mutation (mutated elitist)
reproduction_rate = 0.4 # Fraction which are chosen to reproduce
rotation_chance = 0.1
point_chance = 0.1
num_iterations = 200

##################################################################################################################
# GET POPULATION FROM FITNESS DATAFRAME
population = pd.read_csv('archive data/popsize=40,num_iterations=200/fitness_df_150.csv').iloc[:testing_population_size]
population['Chromosome'] = population['Chromosome'].apply(lambda x: ast.literal_eval(x))
population = population['Chromosome']

fitness_dict = {i:[] for i in range(testing_population_size)}

count = 0
for current_problem in testing_set:
    print(f'Problem {count}')
    count += 1
    for chromosome_index in range(testing_population_size):
        chromosome = population[chromosome_index]
        problem = copy.deepcopy(current_problem)
        bin_dict = {'0':[]}
        objects =  [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]
        round = 0
        current_bin = 0
        while round < NUM_RECTANGLES:
            solution = chromosome[round]
            if solution in [1,3,5]: # choose largest remaining piece by area
                areas = [[x[0] * x[1], x] for x in problem]
                areas.sort(reverse=True)
                item = areas[0][1]
                problem.remove(item)
            elif solution in [0,2,4]:
                item = problem.pop(0) # instead choose first piece in queue

            if solution in [0,1]:
                objects, bin_dict, current_bin = single_ff(bin_dict, objects, item, round, BIN_WIDTH, BIN_HEIGHT)

            elif solution in [2,3]:
                objects, bin_dict, current_bin = single_nf(bin_dict, objects, item, round, current_bin, BIN_WIDTH, BIN_HEIGHT)
            
            elif solution in [4,5]:
                objects, bin_dict, current_bin = single_bf(bin_dict, objects, item, round, BIN_WIDTH, BIN_HEIGHT)

            elif solution == 6:
                objects, bin_dict, problem, current_bin = single_djd(bin_dict, objects, problem, current_bin, BIN_WIDTH, BIN_HEIGHT)

            round += 1
        fitness = fitness_function(objects)
        fitness_dict[chromosome_index].append(fitness)

fitness_df = pd.DataFrame(fitness_dict)


output_df = pd.concat([testing_set_df,fitness_df], axis=1)
output_df.drop(columns=['Unnamed: 0'], inplace=True)
output_df.to_csv('hyper_heuristic_testing_archive data_popsize=40,num_iterations=200_fitness_df_150.csv.csv')
output_df.describe().to_csv(f'hyper_heuristic_testing_summary_archive data_popsize=40,num_iterations=200_fitness_df_150.csv.csv')