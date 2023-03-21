import numpy as np
import matplotlib.pyplot as plt
import itertools

BIN_HEIGHT = 100
BIN_WIDTH = 50
NUM_POINTS = 5 # determines number of rectangles: NUM_RECTANGLES = (NUM_POINTS + 1) ** 2

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

# In 10000 iterations, for BIN_HEIGHT = 1000, BIN_WIDTH = 500 produces:
# mean min area: 11
# median min area: 6
# mean max area: 21824
# median max area: 20211
# Note: the number of rectangles produced = (num_points + 1)^2

# Problem version 1: Given single bin, how much of the bin's area can be used?
# Placement
# Bottom left: start piece in top right of bin (outside of shape); push down until collision, left until collision, repeat until stable condition

'''
Initialise bin object (zero-matrix) with piece in bottom left (small 1's)
'''
items = create_rectangles()
initial_piece = items.pop()
print(initial_piece)

object = np.zeros((BIN_HEIGHT, BIN_WIDTH))
# object[BIN_HEIGHT-initial_piece[1]:BIN_HEIGHT, :initial_piece[0]] +=1 
object[BIN_HEIGHT-initial_piece[1]:BIN_HEIGHT, BIN_WIDTH - initial_piece[0]:BIN_WIDTH] +=1 
# print(np.count_nonzero(object==0))

# BOTTOM LEFT PLACEMENT HEURISTIC
while len(items) > 0:
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
        # end_flag = True

    

















