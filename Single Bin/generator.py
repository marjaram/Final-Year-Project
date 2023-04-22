import itertools
import numpy as np

def create_rectangles(BIN_WIDTH, BIN_HEIGHT, NUM_POINTS, shuffle=True, rotate=True, decreasing_area_sort=False):
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
    if decreasing_area_sort:
        areas = [(rectangle[0]*rectangle[1], rectangle) for rectangle in rectangles] 
        areas.sort()
        rectangles = [areas[i][1] for i in range(len(areas))]
    return rectangles