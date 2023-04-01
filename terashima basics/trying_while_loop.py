############################################################################# Imports and setup #####################################################################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import itertools
import sys
import os
import logging
np.set_printoptions(threshold=sys.maxsize)

BIN_HEIGHT = 100
BIN_WIDTH = 100
NUM_POINTS = 3 # determines number of rectangles: NUM_RECTANGLES = (NUM_POINTS + 1) ** 2

fig, axs = plt.subplots(4,4)
fig.set_figwidth(10)
fig.set_figheight(10)

############################################################################ Functions ########################################################################################################################################

def create_rectangles(shuffle=True, rotate=False):
    xs = [i for i in range(1,BIN_WIDTH)]
    ys = [i for i in range(1,BIN_HEIGHT)]
    x_coords = [0, BIN_WIDTH]
    y_coords = [0, BIN_HEIGHT]

    for point in range(NUM_POINTS):
        x, y = np.random.choice(xs), np.random.choice(ys)
        xs.remove(x)
        ys.remove(y)
        
        x_coords.append(x)
        y_coords.append(y)

    x_coords = sorted(x_coords)
    y_coords = sorted(y_coords)
    widths = [x_coords[i+1] - x_coords[i] for i in range(NUM_POINTS+1)]
    heights = [y_coords[i+1] - y_coords[i] for i in range(NUM_POINTS+1)]
    rectangles = list(itertools.product(widths, heights))
    
    if shuffle:
        np.random.shuffle(rectangles)
    if rotate:
        num_rotations = np.random.randint((NUM_POINTS+1)**2)
        for i in range(num_rotations):
            x = rectangles.pop(0)
            width, height = x[0], x[1]
            rectangles.append((height, width))
    return rectangles



################################## SORT BY DECREASING AREA #####################################################
sort = False
items = create_rectangles()

if sort:
    areas = []
    for i in range(len(items)):
        rectangle = items.pop()
        areas.append((rectangle[0]*rectangle[1], rectangle))

    areas.sort()
    for i in range(len(areas)):
        items.append(areas[i][1]) 


################################ FILL BOTTOM ROW ################################################################################################

# Place first piece in bottom left corner
initial_piece = items.pop()
object = np.zeros((BIN_HEIGHT, BIN_WIDTH))
object[BIN_HEIGHT-initial_piece[1]:BIN_HEIGHT, :initial_piece[0]] +=1

# Define points to help with future placement
rightmost = (initial_piece[0] - 1, BIN_HEIGHT - initial_piece[1]) # # rightmost: the highest point of the furthest right shape
uppermost = (initial_piece[0] - 1, BIN_HEIGHT - initial_piece[1]) # # uppermost: the furthest right point of the tallest shape
upperrightmost = (rightmost[0], uppermost[1]) # theoretical position, such that no shapes are beyond this point

i = 1
j = 0
not_break = True
while not_break:
    i += 2
    piece = items.pop()
    if (BIN_WIDTH - rightmost[0]) > piece[0]: 
        object[BIN_HEIGHT-piece[1]:BIN_HEIGHT, rightmost[0] + 1 : rightmost[0] + piece[0]+1] += i
        if BIN_HEIGHT - piece[1] <= uppermost[1]:
            uppermost = (rightmost[0] + piece[0] , BIN_HEIGHT - piece[1]) 
        rightmost = (rightmost[0] + piece[0], BIN_HEIGHT-piece[1])
        upperrightmost = (rightmost[0], uppermost[1])

    else:
        not_break = False

    axs[j//4, j%4].matshow(object, cmap='Reds')
    axs[j//4, j%4].plot(rightmost[0],rightmost[1],'go')
    axs[j//4, j%4].plot(uppermost[0],uppermost[1],'go')
    axs[j//4, j%4].plot(upperrightmost[0],upperrightmost[1],'ro')
    axs[j//4, j%4].text(20,20, f"UR={upperrightmost}")
    j += 1

################################ NEXT PIECE ################################################################################################

# INSERT PIECE AT UPPERRIGHTMOST POINT
while True:
    if len(items) == 0:
        break
    if upperrightmost[1] - piece[1] < 0:
        print(f'Cannot insert piece of size {piece}')
        break

    object[upperrightmost[1]-piece[1] : upperrightmost[1], BIN_WIDTH - piece[0]:BIN_WIDTH] += i 
    current_pos = (BIN_WIDTH - 1,uppermost[1]-piece[1])

    stable = False
    while not stable:
        prev_pos = current_pos

        # DOWN
        not_break = True
        while not_break and (current_pos[1] + piece[1] < BIN_HEIGHT):
            object[current_pos[1] + piece[1], current_pos[0]-piece[0]+1:current_pos[0]+1] += i
            row = object[current_pos[1] + piece[1], current_pos[0]-piece[0]+1:current_pos[0]+1]%2
            if 0 in row: # clash detected; move piece back up
                object[current_pos[1] + piece[1], current_pos[0]-piece[0]+1:current_pos[0]+1] -= i
                not_break = False
            else:
                object[current_pos[1], current_pos[0]-piece[0]+1:current_pos[0]+1] = 0
                current_pos = (current_pos[0],current_pos[1]+1)

        # LEFT
        not_break = True
        while not_break and (current_pos[0] - piece[0] >= 0):
            object[current_pos[1]: current_pos[1]+ piece[1], current_pos[0]-piece[0]] += i
            col = object[current_pos[1]: current_pos[1]+ piece[1], current_pos[0]-piece[0]]%2
            if 0 in col:
                object[current_pos[1]: current_pos[1]+ piece[1], current_pos[0]-piece[0]] -= i
                not_break = False
            else:
                object[current_pos[1]: current_pos[1]+ piece[1], current_pos[0]] = 0
                current_pos = (current_pos[0] - 1, current_pos[1])

        if prev_pos == current_pos:
            stable = True
            if current_pos[0] >= rightmost[0]:
                rightmost = current_pos
                upperrightmost = (rightmost[0], uppermost[1])
            if current_pos[1] <= uppermost[1]:
                uppermost = current_pos
                upperrightmost = (rightmost[0], uppermost[1])
            axs[j//4, j%4].matshow(object, cmap='Blues')
            axs[j//4, j%4].text(current_pos[0] - 20, current_pos[1], f"{current_pos}")
            axs[j//4, j%4].plot(rightmost[0],rightmost[1],'go')
            axs[j//4, j%4].plot(uppermost[0],uppermost[1],'go')
            axs[j//4, j%4].plot(upperrightmost[0],upperrightmost[1],'ro')
            axs[j//4, j%4].text(20,20, f"UR={upperrightmost}")
            j += 1
    i += 2
    piece = items.pop()

print(f'{np.count_nonzero(object)}/{BIN_HEIGHT*BIN_WIDTH}={(100*np.count_nonzero(object))/(BIN_HEIGHT*BIN_WIDTH)}%')
plt.show()


################################################################# EVALUTATION METRICS ################################################################################################

# Percentage usage

# Number of shapes remaining


