import numpy as np
import matplotlib.pyplot as plt
import generator
import placement
import sys
import copy
import selection
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logger = logging.getLogger('my_module_name')
logging.basicConfig(filename='log.log',filemode='w', encoding='utf-8', level=logging.DEBUG)

fig, axs = plt.subplots(4,4)
fig.set_figwidth(10)
fig.set_figheight(10)

# Define dimensions of bin and number of rectangles
BIN_HEIGHT = 100
BIN_WIDTH = 100
NUM_RECTANGLES = 20 
selection_heuristic = 'ff' # alternatively: 'first', 'next', 'djd'
placement_heuristic = 'bl'

# Create: rectangle set, 8-digit label, area dictionary, height dictionary (to lookup when removing pieces wfrom labels)
items, label, area_dict, height_dict = generator.create_rectangles(BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES, shuffle=True, decreasing_area_sort=True)
items_copy = copy.deepcopy(items)
# items = [(55, 55), (47, 47), (43, 43), (45, 37), (32, 49), (34, 44), (65, 23), (25, 57), (41, 34), (57, 18), (24, 41), (43, 20), (33, 24), (23, 34), (46, 16), (17, 35), (36, 10), (44, 4), (54, 3), (3, 11)]
bin_dict = {'0':[]} # Dictionary storing the items allocated to each bin
# Define list of objects(bins)
objects = [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]
logging.info(f'Selection: {selection_heuristic}, Placement: {placement_heuristic}. Allocating {len(items)} items into {BIN_WIDTH}x{BIN_HEIGHT} bins.')

# if selection_heuristic == 'ff':
#     objects = selection.ff(items, [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]], BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES)

# elif selection_heuristic == 'bf':
#     objects = selection.bf(items, [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]], BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES)

# elif selection_heuristic == 'nf':
#     objects = selection.nf(items, [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]], BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES)
    
# elif selection_heuristic == 'djd': # ASSUMES ITEMS ARE PRESORTED IN DESCENDING ORDER
#     objects = selection.djd(items, [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]], BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES)

logging.info('__________________________________________________________________________________________________________________________________________')
ff_objects = selection.ff(items, [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]], BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES)
bin_dict_ff = copy.deepcopy(bin_dict)
bin_dict = {'0':[]} # Dictionary storing the items allocated to each bin
items = copy.deepcopy(items_copy)

bf_objects = selection.bf(items, [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]], BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES)
items = copy.deepcopy(items_copy)
bin_dict_bf = copy.deepcopy(bin_dict)
bin_dict = {'0':[]} # Dictionary storing the items allocated to each bin

nf_objects = selection.nf(items, [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]], BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES)
items = copy.deepcopy(items_copy)
bin_dict_nf = copy.deepcopy(bin_dict)

print(len(ff_objects))
print(len(nf_objects))
print(len(bf_objects))


pu_total = 0
for i in range(len(ff_objects)):
    print(i)
    object = ff_objects[i][0]
    logging.info(f'Bin {i} percentage usage = {(100*np.count_nonzero(object))/(BIN_HEIGHT*BIN_WIDTH)}%')
    pu_total += ((100*np.count_nonzero(object))/(BIN_HEIGHT*BIN_WIDTH))**2
    logging.info(f'Items allocated to bin {i}: {bin_dict_ff[f"{i}"]}')
    axs[i//4][i%4].matshow(object, cmap='Blues')
fitness = pu_total/len(ff_objects)
logging.info(f'Fitness of this ff packing is {fitness:.2f}')

pu_total = 0
for i in range(len(nf_objects)):
    print(i)
    object = nf_objects[i][0]
    logging.info(f'Bin {i} percentage usage = {(100*np.count_nonzero(object))/(BIN_HEIGHT*BIN_WIDTH)}%')
    pu_total += ((100*np.count_nonzero(object))/(BIN_HEIGHT*BIN_WIDTH))**2
    logging.info(f'Items allocated to bin {i}: {bin_dict_nf[f"{i}"]}')
    axs[(i+4)//4][i+4%4].matshow(object, cmap='Blues')
fitness = pu_total/len(nf_objects)
logging.info(f'Fitness of this nf packing is {fitness:.2f}')

pu_total = 0
for i in range(len(bf_objects)):
    print(i)
    object = bf_objects[i][0]
    logging.info(f'Bin {i} percentage usage = {(100*np.count_nonzero(object))/(BIN_HEIGHT*BIN_WIDTH)}%')
    pu_total += ((100*np.count_nonzero(object))/(BIN_HEIGHT*BIN_WIDTH))**2
    logging.info(f'Items allocated to bin {i}: {bin_dict_bf[f"{i}"]}')
    axs[(i+8)//4][i%4].matshow(object, cmap='Blues')
fitness = pu_total/len(bf_objects)
logging.info(f'Fitness of this bf packing is {fitness:.2f}')

plt.show()







