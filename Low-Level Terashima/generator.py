import itertools
import numpy as np
seed = np.random.default_rng()
# TO DO: Create additional function that generates a rectangle set based on a given area/height label


def create_rectangles(BIN_WIDTH=100, BIN_HEIGHT=100, NUM_RECTANGLES=20, shuffle=True, rotate=False, decreasing_area_sort=False):
    widths = seed.integers(1,BIN_WIDTH - 1, NUM_RECTANGLES)
    heights = seed.integers(1,BIN_HEIGHT - 1, NUM_RECTANGLES)
    rectangles = list(zip(widths, heights))
    areas = [(rectangle[0]*rectangle[1], rectangle) for rectangle in rectangles]
    if shuffle:
        np.random.shuffle(rectangles)
    if rotate:
        num_rotations = seed.integers(NUM_RECTANGLES)
        for i in range(num_rotations):
            x = rectangles.pop(0)
            width, height = x[0], x[1]
            rectangles.append((height, width))
    if decreasing_area_sort:
        areas.sort()
        rectangles = [areas[i][1] for i in range(len(areas))]

    # Areas
    huge = 0
    large = 0
    medium = 0
    small = 0

    for area in areas:
        if area[0] > (BIN_WIDTH * BIN_HEIGHT)/2:
            huge += 1
        elif (BIN_WIDTH * BIN_HEIGHT)/2 >= area[0] > (BIN_WIDTH * BIN_HEIGHT)/3:
            large += 1
        elif (BIN_WIDTH * BIN_HEIGHT)/3 >= area[0] > (BIN_WIDTH * BIN_HEIGHT)/4:
            medium += 1
        else:
            small += 1
        
    # Rectangularity
    tall = 0
    average = 0
    short = 0
    for area in areas:
        if area[1][1] > BIN_HEIGHT/2:
            tall += 1
        elif BIN_HEIGHT/2 >= area[1][1] > BIN_HEIGHT/3:
            average += 1
        else:
            short += 1

    problem_label = (huge, large, medium, small, tall, average, short, 1)
    return rectangles, problem_label
