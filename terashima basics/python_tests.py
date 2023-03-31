import matplotlib.pyplot as plt
import numpy as np
import itertools

BIN_HEIGHT = 100
BIN_WIDTH = 100
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

################################## SORT BY DECREASING AREA #####################################################
sort = False
items = create_rectangles()
if sort:
    areas = []
    items = create_rectangles()
    for i in range(len(items)):
        rectangle = items.pop()
        areas.append((rectangle[0]*rectangle[1], rectangle))

    areas.sort()
    for i in range(len(areas)):
        items.append(areas[i][1]) 


################################ PLACEMENT HEURISTICS: BOTTOM LEFT ################################

# Placing initial piece in bottom left
initial_piece = items.pop()
object = np.zeros((BIN_HEIGHT, BIN_WIDTH))
object[BIN_HEIGHT-initial_piece[1]:BIN_HEIGHT, :initial_piece[0]] +=1  


fig, axs = plt.subplots(2)
axs[0].matshow(object, cmap='Blues')
axs[1].matshow(object, cmap='Reds')
fig.suptitle('A single plot')
plt.show()