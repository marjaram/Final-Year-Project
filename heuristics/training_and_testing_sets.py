import sys
import numpy as np
import pandas as pd

BIN_WIDTH=100
BIN_HEIGHT=100
NUM_RECTANGLES=20

def generate_rectangles(seed, BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES):
    # Generate widths and heights of rectangles between 1 and 2/3 bin dimensions
    widths = seed.integers(1,BIN_WIDTH, NUM_RECTANGLES)
    heights = seed.integers(1,BIN_HEIGHT, NUM_RECTANGLES)
    rectangles = list(zip(widths, heights))
    seed.shuffle(rectangles)

    # Rotate (swap width and height) of a random number of rectangles    
    num_rotations = seed.integers(NUM_RECTANGLES)
    for i in range(num_rotations):
        x = rectangles.pop(0)
        width, height = x[0], x[1]
        rectangles.append((height, width))

    # Generate label for problem instance
    areas = [(rectangle[0]*rectangle[1], rectangle) for rectangle in rectangles]
    # Area labels
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
    # Rectangularity labels
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
    huge, large, medium, small, tall, average, short = huge/NUM_RECTANGLES, large/NUM_RECTANGLES, medium/NUM_RECTANGLES, small/NUM_RECTANGLES, tall/NUM_RECTANGLES, average/NUM_RECTANGLES, short/NUM_RECTANGLES
    problem_label = [huge, large, medium, small, tall, average, short, 1]
    return rectangles, problem_label


# Create training set of 1000
labels_list = []
items_list = []
for i in range(1000):
    rng = np.random.default_rng(seed=i)
    items, label = generate_rectangles(rng,BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES)
    items_list.append(items)
    labels_list.append(label)

labels_list_series = pd.Series(labels_list)
items_list_series = pd.Series(items_list)

training_set_df = pd.DataFrame(
    {'Labels': labels_list_series,
    'Item sets': items_list_series
    })
training_set_df = training_set_df.astype('object')
training_set_df.to_csv(f'training_set.csv')


# Create testing set of 500
labels_list = []
items_list = []
for i in range(500):
    rng = np.random.default_rng(1000+i)
    items, label = generate_rectangles(rng,BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES)
    items_list.append(items)
    labels_list.append(label)

    labels_list_series = pd.Series(labels_list)
    items_list_series = pd.Series(items_list)

    testing_set_df = pd.DataFrame(
        {'Labels': labels_list_series,
        'Item sets': items_list_series
        })
    testing_set_df = testing_set_df.astype('object')
    testing_set_df.to_csv(f'testing_set.csv')
