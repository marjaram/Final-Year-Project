import selection
import pandas as pd
import numpy as np
import time
import sys
import math
import ast

def fitness_function(object_list): 
    fraction_util = 0
    for object in object_list:
        fraction_util += ((np.count_nonzero(object[0]))/(BIN_HEIGHT*BIN_WIDTH))**2
    fitness = fraction_util/len(object_list)

    return fitness

problem_set = 'testing_set'
problem_set_df = pd.read_csv(f'{problem_set}.csv')

# Method for interpreting columns of a df as a list was found here: https://stackoverflow.com/a/63716874
problem_set_df['Labels'] = problem_set_df['Labels'].apply(lambda x: ast.literal_eval(x))
problem_set_df['Item sets'] = problem_set_df['Item sets'].apply(lambda x: ast.literal_eval(x))

# Main Loop
BIN_HEIGHT = 100
BIN_WIDTH = 100
NUM_RECTANGLES = 20

labels = problem_set_df['Labels']
item_sets = problem_set_df['Item sets']

ff_times = []
ffd_times = []
nf_times = []
nfd_times = []
bf_times = []
bfd_times = []
djd_times = []
djd2_times = []

ff_results = []
ffd_results = []
nf_results = []
nfd_results = []
bf_results = []
bfd_results = []
djd_results = []
djd2_results = []

best_heuristics = []

for problem_instance in range(len(labels)):
    items = item_sets[problem_instance]
    label = labels[problem_instance]

    ff_start = time.time_ns()
    ff_objects, ff_bin_dict = selection.ff(items,BIN_WIDTH,BIN_HEIGHT)
    ff_end = time.time_ns()
    ff_times.append((ff_end-ff_start)*10**-6)

    ffd_start = time.time_ns()
    ffd_objects, ffd_bin_dict = selection.ffd(items,BIN_WIDTH,BIN_HEIGHT)
    ffd_end = time.time_ns()
    ffd_times.append((ffd_end-ffd_start)*10**-6)

    nf_start = time.time_ns()
    nf_objects, nf_bin_dict = selection.nf(items,BIN_WIDTH,BIN_HEIGHT)
    nf_end = time.time_ns()
    nf_times.append((nf_end-nf_start)*10**-6)
    
    nfd_start = time.time_ns()
    nfd_objects, nfd_bin_dict = selection.nfd(items,BIN_WIDTH,BIN_HEIGHT)
    nfd_end = time.time_ns()
    nfd_times.append((nfd_end-nfd_start)*10**-6)

    bf_start = time.time_ns()
    bf_objects, bf_bin_dict = selection.bf(items,BIN_WIDTH,BIN_HEIGHT)
    bf_end = time.time_ns()
    bf_times.append((bf_end-bf_start)*10**-6)

    bfd_start = time.time_ns()
    bfd_objects, bfd_bin_dict = selection.bfd(items,BIN_WIDTH,BIN_HEIGHT)
    bfd_end = time.time_ns()
    bfd_times.append((bfd_end-bfd_start)*10**-6)

    djd_start = time.time_ns()
    djd_objects, djd_bin_dict = selection.djd(items,BIN_WIDTH,BIN_HEIGHT)
    djd_end = time.time_ns()
    djd_times.append((djd_end-djd_start)*10**-6)

    djd2_start = time.time_ns()
    djd2_objects, djd2_bin_dict = selection.djd2(items,BIN_WIDTH,BIN_HEIGHT)
    djd2_end = time.time_ns()
    djd2_times.append((djd2_end-djd2_start)*10**-6)

    ff_score = round(fitness_function(ff_objects),4)
    ffd_score = round(fitness_function(ffd_objects),4)
    nf_score = round(fitness_function(nf_objects),4)
    nfd_score = round(fitness_function(nfd_objects),4)
    bf_score = round(fitness_function(bf_objects),4)
    bfd_score = round(fitness_function(bfd_objects),4)
    djd_score = round(fitness_function(djd_objects),4)
    djd2_score = round(fitness_function(djd2_objects),4)

    ff_results.append(ff_score)
    ffd_results.append(ffd_score)
    nf_results.append(nf_score)
    nfd_results.append(nfd_score)
    bf_results.append(bf_score)
    bfd_results.append(bfd_score)
    djd_results.append(djd_score)
    djd2_results.append(djd2_score)

    scores = (ff_score, ffd_score, nf_score, nfd_score, bf_score, bfd_score, djd_score, djd2_score)
    best_heuristic = max(enumerate(scores),key=lambda x: x[1])[0]
    
    label.append(best_heuristic)
    best_heuristics.append(best_heuristic)
    print(f'problem: {problem_instance}, best heuristics: {best_heuristic}')
    

score_results = pd.DataFrame(
{      
         'Labels': labels,
         'Item sets': item_sets,
         'First Fit Score': ff_results,
         'First Fit Decreasing Score': ffd_results,
         'Next Fit Score': nf_results,
         'Next Fit Decreasing Score': nfd_results,
         'Best Fit Score': bf_results,
         'Best Fit Decreasing Score': bfd_results,
         'Djang-Fitch Score': djd_results,
         'Djang-Fitch 2 Score': djd2_results,
         'Best heuristic': best_heuristics
})
time_results = pd.DataFrame(
{      
         'Labels': labels,
         'Item sets': item_sets,
         'First Fit Times': ff_times,
         'First Fit Decreasing Times': ffd_times,
         'Next Fit Times': nf_times,
         'Next Fit Decreasing Times': nfd_times,
         'Best Fit Times': bf_times,
         'Best Fit Decreasing Times': bfd_times,
         'Djang-Fitch Times': djd_times,
         'Djang-Fitch 2 Times': djd2_times,   
}
)
score_results.to_csv(f'low_level_scores_{problem_set}.csv')
time_results.to_csv(f'low_level_times_{problem_set}.csv')