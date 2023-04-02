############################################################################# Imports and setup #####################################################################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools
import sys
import generator
np.set_printoptions(threshold=sys.maxsize)

BIN_HEIGHT = 100
BIN_WIDTH = 100
NUM_POINTS = 3 # determines number of rectangles: NUM_RECTANGLES = (NUM_POINTS + 1) ** 2

fig, axs = plt.subplots(4,4)
fig.set_figwidth(10)
fig.set_figheight(10)
items = generator.create_rectangles(BIN_WIDTH, BIN_HEIGHT, NUM_POINTS)
object = np.zeros((BIN_HEIGHT, BIN_WIDTH))

def bottom_left(items):
    # Place first piece in bottom left corner
    initial_piece = items.pop()
    object[BIN_HEIGHT-initial_piece[1]:BIN_HEIGHT, :initial_piece[0]] +=1

    # Define points to help with future placement
    rightmost = (initial_piece[0] - 1, BIN_HEIGHT - initial_piece[1]) # rightmost: the highest point of the furthest right shape
    uppermost = (initial_piece[0] - 1, BIN_HEIGHT - initial_piece[1]) # uppermost: the furthest right point of the tallest shape
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

    # Insert next piece at Upperrightmost point, then move down and left until in a stable position
    while True:
        if len(items) == 0:
            break
        if upperrightmost[1] - piece[1] < 0:
            break

        object[upperrightmost[1]-piece[1] : upperrightmost[1], BIN_WIDTH - piece[0]:BIN_WIDTH] += i 
        current_pos = (BIN_WIDTH - 1,uppermost[1]-piece[1])

        stable = False
        while not stable:
            prev_pos = current_pos

            # Move piece down
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

            # Move piece left
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
            
            # Stop when stable position reached
            if prev_pos == current_pos:
                stable = True
                if current_pos[0] >= rightmost[0]:
                    rightmost = current_pos
                    upperrightmost = (rightmost[0], uppermost[1])
                if current_pos[1] <= uppermost[1]:
                    uppermost = current_pos
                    upperrightmost = (rightmost[0], uppermost[1])
                axs[j//4, j%4].matshow(object, cmap='Blues')
                axs[j//4, j%4].plot(rightmost[0],rightmost[1],'go')
                axs[j//4, j%4].plot(uppermost[0],uppermost[1],'go')
                axs[j//4, j%4].plot(upperrightmost[0],upperrightmost[1],'ro')
                axs[j//4, j%4].text(20,20, f"UR={upperrightmost}")
                j += 1
        i += 2
        piece = items.pop()
 
    # Redefine uppermost, rightmost, upperrightmost then check if piece can be placed below and left of upperrightmost point
    rightmost = (BIN_WIDTH-1, 0)
    uppermost = (BIN_WIDTH-1, 0)
    upperrightmost = (BIN_WIDTH-1, 0)

    while True:
        if len(items) == 0:
            break
        current_pos = (BIN_WIDTH-1, 0)
        object[:piece[1], BIN_WIDTH-piece[0]:] += i # insert new piece
        
        # Check if piece can be placed
        col = object[current_pos[1]: current_pos[1]+ piece[1], current_pos[0]-piece[0]+1] % 2
        row = object[current_pos[1] + piece[1] - 1, current_pos[0]-piece[0]+1:current_pos[0]+1] % 2
        if 0 in row or 0 in col:
            object[:piece[1], BIN_WIDTH-piece[0]:] -= i
            break

        stable = False
        while not stable:
            prev_pos = current_pos

            # Move piece down
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

            # Move piece left
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
            
            # Stop when stable position reached
            if prev_pos == current_pos:
                stable = True
                if current_pos[0] >= rightmost[0]:
                    rightmost = current_pos
                    upperrightmost = (rightmost[0], uppermost[1])
                if current_pos[1] <= uppermost[1]:
                    uppermost = current_pos
                    upperrightmost = (rightmost[0], uppermost[1])
                axs[j//4, j%4].matshow(object, cmap='Greens')
                axs[j//4, j%4].plot(rightmost[0],rightmost[1],'go')
                axs[j//4, j%4].plot(uppermost[0],uppermost[1],'go')
                axs[j//4, j%4].plot(upperrightmost[0],upperrightmost[1],'ro')
                axs[j//4, j%4].text(20,20, f"UR={upperrightmost}")
                j += 1
            
        i += 2
        piece = items.pop()
    
    print(f'Area filled = {np.count_nonzero(object)}/{BIN_HEIGHT*BIN_WIDTH} = {(100*np.count_nonzero(object))/(BIN_HEIGHT*BIN_WIDTH)}%')
    print(f'Pieces remaining = {len(items) + 1}/{(NUM_POINTS+1)**2}')
    plt.show()

bottom_left(items)