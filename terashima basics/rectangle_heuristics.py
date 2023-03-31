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
# items = create_rectangles()
# items = [(87, 29), (5, 43), (4, 43), (87, 12), (4, 12), (4, 29), (87, 16), (5, 12), (4, 16), (4, 29), (4, 43), (4, 12), (5, 29), (5, 16), (4, 16), (87, 43)]
items = [(10,10),(40,10),(10,30),(40,40)]
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
    if (BIN_WIDTH - 1 - rightmost[0]) > piece[0]: 
        object[BIN_HEIGHT-piece[1]:BIN_HEIGHT, rightmost[0] + 1 : rightmost[0] + piece[0]+1] += i
        if BIN_HEIGHT - piece[1] <= uppermost[1]:
            uppermost = (rightmost[0] + piece[0] , BIN_HEIGHT - piece[1]) 
        rightmost = (rightmost[0] + piece[0], BIN_HEIGHT-piece[1])
        upperrightmost = (rightmost[0], uppermost[1])

    else:
        not_break = False

    axs[j//4, j%4].matshow(object, cmap='Reds')
    axs[j//4, j%4].plot(rightmost[0], rightmost[1],'ro')
    axs[j//4, j%4].plot(uppermost[0], uppermost[1],'ro')
    axs[j//4, j%4].plot(upperrightmost[0],upperrightmost[1],'ro')
    axs[j//4, j%4].text(rightmost[0]-20, rightmost[1]-20, f"R={rightmost}")
    axs[j//4, j%4].text(uppermost[0]-20, uppermost[1]-20, f"U={uppermost}")
    axs[j//4, j%4].text(upperrightmost[0],upperrightmost[1], f"UR={upperrightmost}")
    j += 1

################################ NEXT PIECE ################################################################################################

# INSERT PIECE AT UPPERRIGHTMOST POINT
object[upperrightmost[1]-piece[1] : upperrightmost[1], BIN_WIDTH - piece[0]:BIN_WIDTH] += i 

axs[j//4, j%4].matshow(object, cmap='Blues')
axs[j//4, j%4].plot(rightmost[0], rightmost[1],'ro')
axs[j//4, j%4].plot(uppermost[0], uppermost[1],'ro')
axs[j//4, j%4].plot(upperrightmost[0],upperrightmost[1],'ro')
axs[j//4, j%4].text(rightmost[0], rightmost[1], f"R={rightmost}")
axs[j//4, j%4].text(uppermost[0], uppermost[1], f"U={uppermost}")
axs[j//4, j%4].text(upperrightmost[0],upperrightmost[1], f"UR={upperrightmost}")

# DOWN
not_break = True
current_pos = (BIN_WIDTH - 1,uppermost[1]-piece[1])

axs[j//4, j%4].plot(current_pos[0],current_pos[1],'go')
axs[j//4, j%4].text(current_pos[0] - 20,current_pos[1], f"CP={current_pos}")
j += 1

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
axs[j//4, j%4].matshow(object, cmap='Greens')
axs[j//4, j%4].text(current_pos[0] - 40,current_pos[1]-20, f"CP={current_pos}")
j += 1
print(current_pos[1])
print(current_pos[1]+ piece[1]) 
print(current_pos[0]-piece[0]-1)
not_break = True
while not_break and (current_pos[0] - piece[0] > 0):
    object[current_pos[1]: current_pos[1]+ piece[1], current_pos[0]-piece[0]] += i
    col = object[current_pos[1]: current_pos[1]+ piece[1], current_pos[0]-piece[0]]%2
    if 0 in col:
        object[current_pos[1]: current_pos[1]+ piece[1], current_pos[0]-piece[0]] -= i
        not_break = False
    else:
        object[current_pos[1]: current_pos[1]+ piece[1], current_pos[0]] = 0
        current_pos = (current_pos[0] - 1, current_pos[1])       

axs[j//4, j%4].matshow(object, cmap='Reds')
axs[j//4, j%4].text(current_pos[0] - 20, current_pos[1], f"{current_pos}")

j += 1

plt.show()

################################################################# EVALUTATION METRICS ################################################################################################

# Percentage usage

# Number of shapes remaining


# Do I need this loop? At least for the first few placements, I should just be able to place the piece next to the start piece?
'''while len(items) > 0:
    piece = items.pop()
    print(piece)
    object[:piece[1], BIN_WIDTH-piece[0]:BIN_WIDTH] +=1 
    
    # If doesn't fit (check for >1 values), return error signal and break out of loop
    if 2 in object[:piece[1], BIN_WIDTH-piece[0]:BIN_WIDTH]:
        object[:piece[1], BIN_WIDTH-piece[0]:BIN_WIDTH] -= 1
        print(f'Could not fit in piece {piece}') 
        break
    
    start_position = (BIN_WIDTH, 0)
    current_position = (BIN_WIDTH, 0)
    # Down movement

    while current_position[1] < BIN_HEIGHT-piece[1]:
        print(current_position)
        object[current_position[1], current_position[0]-piece[0]:current_position[0]] = 0
        object[current_position[1] + piece[1], current_position[0]-piece[0]:current_position[0]] += 1
        plt.matshow(object, cmap='Blues')
        plt.text(current_position[0], current_position[1], f"{current_position}")
        plt.show()
        if 2 in object[current_position[1] + piece[1], current_position[0]-piece[0]:current_position[0]]:
            object[current_position[1] + piece[1], current_position[0]-piece[0]:current_position[0]] -= 1
            # Move object up
            object[current_position[1], current_position[0]-piece[0]:current_position[0]] += 1
            object[current_position[1] + piece[1], current_position[0]-piece[0]:current_position[0]] -= 1
            break
        

        # If there are any values greater than 1 in bottom row
            # Increment row above by 1
            # Decrement bottom row by 1
            #break
        current_position = (current_position[0], current_position[1]+1)
    
    # LEFT MOVEMENT
    # While true:
        # Set right col to 0's
        # Increment cols underneath by 1
        # If there col any values greater than 1 in left col
            # Increment col to right by 1
            # Decrement left col by 1

    # if position == current_position:
        # end_flag = True'''
