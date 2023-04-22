# DOES NOT CURRENTLY WORK!!!!


from placement import bottom_left
import numpy as np
from main import generate_rectangles
import math
import random
import logging
import sys
logger = logging.getLogger('my_module_name')
logging.basicConfig(filename='log.log',filemode='w', encoding='utf-8', level=logging.DEBUG)

# GENERATE ITEM SET/USE TEST SET AND CALCULATE 'IDEAL' NUMBER OF BINS
BIN_WIDTH = 1000
BIN_HEIGHT = 1000
NUM_RECTANGLES = 30

# items, label = generate_rectangles(BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES)
items = [(330, 501), (6, 478), (175, 453), (193, 267), (31, 608), (37, 486), (586, 313), (371, 382), (342, 124), (240, 175), (352, 81), (660, 448), (658, 552), (147, 531), (448, 373), (255, 47), (580, 219), (204, 172), (266, 636), (395, 258), (364, 612), (38, 606), (137, 399), (323, 279), (70, 424), (281, 82), (176, 487), (380, 112), (519, 268), (207, 611)]
label = (0, 1, 1, 28, 8, 9, 13)

total_items_area = 0
for item in items:
    total_items_area += item[0] * item[1]

ideal = math.ceil(total_items_area/(BIN_HEIGHT*BIN_WIDTH))

# GENERATE INITIAL POPULATION
POP_SIZE = 5
population = []
while len(population) < POP_SIZE:
    np.random.shuffle(items)
    num_bins = ideal + random.choice([0,1,2,3])
    individual = {object:[] for object in range(num_bins)}
    for i in range(0, num_bins):
        if i == num_bins - 1:
            individual[i] = (items[i*math.floor(NUM_RECTANGLES/num_bins):])
        else:
            individual[i] = (items[i*math.floor(NUM_RECTANGLES/num_bins):(i+1) * math.floor(NUM_RECTANGLES/num_bins)])
    population.append(individual)

solution = population[0]
bin1 = solution[0]
print(bin1)
bin1_bin = (np.zeros((BIN_WIDTH, BIN_HEIGHT)),None)
i = 0
for item in bin1:
    print(f'item {item}')
    i += 1
    bin1_bin, success_flag = bottom_left(bin1_bin, item, i)
    if success_flag != 1:
        print('Placement failed')
        break
    print('success')
    print(np.count_nonzero(bin1_bin[0])/(BIN_WIDTH*BIN_HEIGHT))


# GENETIC ALGORITHM
# Chromosome: 