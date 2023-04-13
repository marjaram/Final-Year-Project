import numpy as np
import matplotlib.pyplot as plt
import generator
import placement
import sys
import copy
fig, axs = plt.subplots(4,4)
fig.set_figwidth(10)
fig.set_figheight(10)

# Define dimensions of bin and number of rectangles
BIN_HEIGHT = 100
BIN_WIDTH = 100
NUM_RECTANGLES = 20 
selection_heuristic = 'djd' # alternatively: 'first', 'next', 'djd'
placement_heuristic = 'bl'

# Create: rectangle set, 8-digit label, area dictionary, height dictionary (to lookup when removing pieces wfrom labels)
test_set = [(55, 55), (47, 47), (43, 43), (45, 37), (32, 49), (34, 44), (65, 23), (25, 57), (41, 34), (57, 18), (24, 41), (43, 20), (33, 24), (23, 34), (46, 16), (17, 35), (36, 10), (44, 4), (54, 3), (3, 11)]
items, label, area_dict, height_dict = generator.create_rectangles(BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES, shuffle=True, decreasing_area_sort=True)
items = test_set
bin_dict = {'0':[]} # Dictionary storing the items allocated to each bin
areas = 0
# Define list of objects(bins)
objects = [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]
# print(f'Allocating {len(items)} items into {BIN_WIDTH}x{BIN_HEIGHT} bins. Label: {label[:4], label[4:7], label[7]}')

if selection_heuristic == 'first':
    for i in range(len(items)):
        item = items.pop(0)
        areas += (item[0]*item[1])
        print(f'_____________________________________________________________________item {i} is {item}_____________________________________________________________________')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display

        # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
        can_place = False 
        for o in range(len(objects)):
            print(f'Trying bin {o}')
            object, fail_flag = placement.bottom_left(objects[o], item, BIN_WIDTH, BIN_HEIGHT, j)
            if fail_flag != 0:
                can_place = True
                print(f'Placed in bin {o}')
                bin_dict[f'{o}'].append(i)
                break
        if not can_place:
            objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
            bin = objects[-1]
            object, fail_flag = placement.bottom_left(bin, item, BIN_WIDTH, BIN_HEIGHT, j)
            if fail_flag != 0:
                print(f'New bin {o+1} created and item {i} placed')
                bin_dict[f'{o+1}'] = [i]
            else:
                print(f'Fatal error, item {i}:{item} larger than bin')

elif selection_heuristic == 'best':
    # Initially, operate in the same way as First fit until a second bin is opened
    for i in range(len(items)):
        item = items.pop(0)
        areas += (item[0]*item[1])
        print(f'_____________________________________________________________________item {i} is {item}_____________________________________________________________________')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display

        # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
        can_place = False 
        for o in range(len(objects)):
            print(f'Trying bin {o}')
            object, fail_flag = placement.bottom_left(objects[o], item, BIN_WIDTH, BIN_HEIGHT, j)
            if fail_flag != 0:
                can_place = True
                print(f'Placed in bin {o}')
                bin_dict[f'{o}'].append(i)
                break
        if not can_place:
            objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
            bin = objects[-1]
            object, fail_flag = placement.bottom_left(bin, item, BIN_WIDTH, BIN_HEIGHT, j)
            if fail_flag != 0:
                print(f'New bin {o+1} created and item {i} placed')
                bin_dict[f'{o+1}'] = [i]
                break
            else:
                print(f'Fatal error, item {i}:{item} larger than bin')


    print('_____________________________________________________________________STARTING BEST PHASE_____________________________________________________________________')
    if len(items) > 0:
        # Start best-checking
        for i in range(len(items)):
            item = items.pop(0)
            areas += (item[0]*item[1])
            print(f'_____________________________________________________________________item {NUM_RECTANGLES-len(items)-1} is {item}_____________________________________________________________________')
            j = (2 * i + 1) % 10 # j-value determines colour of piece in display

            # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
            can_place = False 
            best_bin = objects[0]
            waste = BIN_WIDTH * BIN_HEIGHT
            for o in range(len(objects)):
                print(f'Trying bin {o}')
                to_place = copy.deepcopy(objects[o])
                object, fail_flag = placement.bottom_left(to_place, item, BIN_WIDTH, BIN_HEIGHT, j)
                if fail_flag != 0:
                    can_place = True
                    if (BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(object)) < waste:
                        best_bin_index = o
                        best_bin = object
                        waste = np.count_nonzero(object)
            
            if can_place:
                print(f'Placed in bin {best_bin_index}')
                objects[best_bin_index] = (best_bin,1)
                bin_dict[f'{best_bin_index}'].append(NUM_RECTANGLES-len(items)-1)

            if not can_place:
                objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
                bin = objects[-1]
                object, fail_flag = placement.bottom_left(bin, item, BIN_WIDTH, BIN_HEIGHT, j)
                if fail_flag != 0:
                    print(f'New bin {o+1} created and item {i} placed')
                    bin_dict[f'{o+1}'] = [NUM_RECTANGLES-len(items)-1]
                else:
                    print(f'Fatal error, item {i}:{item} larger than bin')

elif selection_heuristic == 'next':

    current_object = 0

    for i in range(len(items)):
        item = items.pop(0)
        areas += (item[0]*item[1])
        print(f'_____________________________________________________________________item {i} is {item}, Current object is {current_object}_____________________________________________________________________')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display
        
        # Try to place in current object
        can_place = False 
        object, fail_flag = placement.bottom_left(objects[current_object], item, BIN_WIDTH, BIN_HEIGHT, j)
        if fail_flag != 0:
                can_place = True
                print(f'Placed in current object: bin {current_object}')
                bin_dict[f'{current_object}'].append(i)

        # If cannot, iterate through other objects
        if not can_place:
            for o in range(len(objects)-1):
                print(f'co: {current_object}, o:{o}, lo:{len(objects)}')
                new_current_object = (current_object + o + 1) % len(objects)
                print(f'Trying bin {new_current_object}')
                object, fail_flag = placement.bottom_left(objects[new_current_object], item, BIN_WIDTH, BIN_HEIGHT, j)
                if fail_flag != 0:
                        can_place = True
                        print(f'Placed in bin {new_current_object}')
                        bin_dict[f'{new_current_object}'].append(i)
                        break
            # If cannot place in any other object, create new object and place there
            if not can_place:
                objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
                current_object = len(objects) - 1
                object, fail_flag = placement.bottom_left(objects[current_object], item, BIN_WIDTH, BIN_HEIGHT, j)
                if fail_flag != 0:
                    print(f'New bin {len(objects) - 1} created and item {i} placed')
                    bin_dict[f'{len(objects) - 1}'] = [NUM_RECTANGLES-len(items)-1]
                else:
                    print(f'Fatal error, item {i}:{item} larger than bin')

elif selection_heuristic == 'djd': # ASSUMES ITEMS ARE PRESORTED IN DESCENDING ORDER!
    waste = 0
    w = BIN_HEIGHT * BIN_WIDTH / 20 # value to increment waste by
    current_object = 0

    i = 0
    while len(items) > 0:
        # Fill bin until at least 1/3 area is covered. Store pieces that did not fit
        item = item.pop(0)
        print(f'_____________________________________________________________________item {i} is {item}_____________________________________________________________________')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display
        i += 1

        object, fail_flag = placement.bottom_left(objects[0], item, BIN_WIDTH, BIN_HEIGHT, j)
        if fail_flag == 1:
    #         items.pop(i)
    #     if np.count_nonzero(object) >= 1/3 * BIN_HEIGHT * BIN_WIDTH:
    #         break
    
    # remaining_space = BIN_HEIGHT * BIN_WIDTH - np.count_nonzero(object)

print('__________________________________________________________________________________________________________________________________________')
# Display each bin
pu_total = 0
for i in range(len(objects)):
    object = objects[i][0]
    print(f'Bin {i} percentage usage = {(100*np.count_nonzero(object))/(BIN_HEIGHT*BIN_WIDTH)}%')
    pu_total += ((100*np.count_nonzero(object))/(BIN_HEIGHT*BIN_WIDTH))**2
    print(f'Items allocated to bin {i}: {bin_dict[f"{i}"]}')
    axs[i//4][i%4].matshow(object, cmap='Blues')

fitness = pu_total/len(objects)
print(f'Fitness of this packing is {fitness:.2f}')

plt.show()







