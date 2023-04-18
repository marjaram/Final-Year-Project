import selection
import pandas as pd
import numpy as np
import time
import sys
seed = np.random.default_rng()

def generate_rectangles(BIN_WIDTH=100, BIN_HEIGHT=100, NUM_RECTANGLES=20):
    # Generate widths and heights of rectangles between 1 and 2/3 bin dimensions
    widths = seed.integers(1,2*(BIN_WIDTH - 1)/3, NUM_RECTANGLES)
    heights = seed.integers(1,2*(BIN_WIDTH - 1)/3, NUM_RECTANGLES)
    rectangles = list(zip(widths, heights))
    np.random.shuffle(rectangles)

    # Rotate (swap width and height) of a random number of rectangles    
    num_rotations = seed.integers(NUM_RECTANGLES)
    for i in range(num_rotations):
        x = rectangles.pop(0)
        width, height = x[0], x[1]
        rectangles.append((height, width))

    # Generate label for problem instance
    areas = [(rectangle[0]*rectangle[1], rectangle) for rectangle in rectangles]
    # Area labels
    huge = 0
    large = 0
    medium = 0
    small = 0
    for area in areas:
        if area[0] > (BIN_WIDTH * BIN_HEIGHT)/2:
            huge += 1        
        elif (BIN_WIDTH * BIN_HEIGHT)/2 >= area[0] > (BIN_WIDTH * BIN_HEIGHT)/3:
            large += 1
        elif (BIN_WIDTH * BIN_HEIGHT)/3 >= area[0] > (BIN_WIDTH * BIN_HEIGHT)/4:
            medium += 1
        else:
            small += 1
    # Rectangularity labels
    tall = 0
    average = 0
    short = 0
    for area in areas:
        if area[1][1] > BIN_HEIGHT/2:
            tall += 1
        elif BIN_HEIGHT/2 >= area[1][1] > BIN_HEIGHT/3:
            average += 1
        else:
            short += 1

    problem_label = (huge, large, medium, small, tall, average, short)
    return rectangles, problem_label

def fitness_function(object_list): 
    fraction_util = 0
    for object in object_list:
        fraction_util += ((np.count_nonzero(object[0]))/(BIN_HEIGHT*BIN_WIDTH))**2
    fitness = fraction_util/len(object_list)

    return fitness

# Main Loop
BIN_HEIGHT = 1000
BIN_WIDTH = 1000
NUM_RECTANGLES = 30

labels = []

ff_times = []
ffd_times = []
nf_times = []
nfd_times = []
bf_times = []
bfd_times = []
djd_times = []

ff_results = []
ffd_results = []
nf_results = []
nfd_results = []
bf_results = []
bfd_results = []
djd_results = []

for problem_instace in range(1000):
    print(problem_instace)
    items, label = generate_rectangles(BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES)
    labels.append(label)

    ff_start = time.time_ns()
    ff_objects, ff_bin_dict = selection.ff(items,BIN_WIDTH,BIN_HEIGHT)
    ff_end = time.time_ns()
    ff_times.append(ff_end-ff_start)

    ffd_start = time.time_ns()
    ffd_objects, ffd_bin_dict = selection.ffd(items,BIN_WIDTH,BIN_HEIGHT)
    ffd_end = time.time_ns()
    ffd_times.append(ffd_end-ffd_start)

    nf_start = time.time_ns()
    nf_objects, nf_bin_dict = selection.nf(items,BIN_WIDTH,BIN_HEIGHT)
    nf_end = time.time_ns()
    nf_times.append(nf_end-nf_start)
    
    nfd_start = time.time_ns()
    nfd_objects, nfd_bin_dict = selection.nfd(items,BIN_WIDTH,BIN_HEIGHT)
    nfd_end = time.time_ns()
    nfd_times.append(nfd_end-nfd_start)

    bf_start = time.time_ns()
    bf_objects, bf_bin_dict = selection.bf(items,BIN_WIDTH,BIN_HEIGHT)
    bf_end = time.time_ns()
    bf_times.append(bf_end-bf_start)

    bfd_start = time.time_ns()
    bfd_objects, bfd_bin_dict = selection.bfd(items,BIN_WIDTH,BIN_HEIGHT)
    bfd_end = time.time_ns()
    bfd_times.append(bfd_end-bfd_start)

    djd_start = time.time_ns()
    djd_objects, djd_bin_dict = selection.djd(items,BIN_WIDTH,BIN_HEIGHT)
    djd_end = time.time_ns()
    djd_times.append(djd_end-djd_start)

    ff_results.append(fitness_function(ff_objects))
    ffd_results.append(fitness_function(ffd_objects))
    nf_results.append(fitness_function(nf_objects))
    nfd_results.append(fitness_function(nfd_objects))
    bf_results.append(fitness_function(bf_objects))
    bfd_results.append(fitness_function(bfd_objects))
    djd_results.append(fitness_function(djd_objects))
    
results = pd.DataFrame(
{      
         'Labels': labels,
         'First Fit Score': ff_results,
         'First Fit Times': ff_times,
         'First Fit Decreasing Score': ffd_results,
         'First Fit Decreasing Times': ffd_times,
         'Next Fit Score': nf_results,
         'Next Fit Times': nf_times,
         'Next Fit Decreasing Score': nfd_results,
         'Next Fit Decreasing Times': nfd_times,
         'Best Fit Score': bf_results,
         'Best Fit Times': bf_times,
         'Best Fit Decreasing Score': bfd_results,
         'Best Fit Decreasing Times': bfd_times,
         'Djang-Fitch Score': djd_results,
         'Djang-Fitch Times': djd_times,  
}
)
results.to_csv('low_level.csv')