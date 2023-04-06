import numpy as np
import matplotlib.pyplot as plt
import sys
import generator
import placement
np.set_printoptions(threshold=sys.maxsize)
fig, axs = plt.subplots(4,4)
fig.set_figwidth(10)
fig.set_figheight(10)

# Define dimensions of bin and number of rectangles
BIN_HEIGHT = 100
BIN_WIDTH = 100
NUM_RECTANGLES = 20 

# Create: rectangle set, 8-digit label, area dictionary, height dictionary (to lookup when removing pieces wfrom labels)
items, label, area_dict, height_dict = generator.create_rectangles(BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES, shuffle=True, decreasing_area_sort=True)
bin_dict = {'0':[]} # Dictionary storing the items allocated to each bin
areas = 0
# Define list of objects(bins)
objects = [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]
print(f'Allocating {len(items)} items into {BIN_WIDTH}x{BIN_HEIGHT} bins. Label: {label[:4], label[4:7], label[7]}')


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

print('__________________________________________________________________________________________________________________________________________')
# Display each bin
for i in range(len(objects)):
    object = objects[i][0]
    print(f'Bin {i} percentage usage = {(100*np.count_nonzero(object))/(BIN_HEIGHT*BIN_WIDTH)}%')
    print(f'Items allocated to bin {i}: {bin_dict[f"{i}"]}')
    axs[i//4][i%4].matshow(object, cmap='Blues')
# print(f'Total area of rectangles = {areas}')
# print(f'Total bin spaced used = {BIN_HEIGHT*BIN_WIDTH*len(objects)}')
print(f'Average Storage efficiency = {100*areas/((BIN_HEIGHT*BIN_WIDTH*len(objects)))}%')
plt.show()





