# Basic Implementation of Rectangular 2DIBPP
import numpy as np
import matplotlib.pyplot as plt
import random
import logging
import sys
from tabulate import tabulate

np.set_printoptions(threshold=sys.maxsize)
logging.basicConfig(filename='rectangle.log', level=logging.INFO, filemode='w')

# Create rectangles
def create_rectangles(bin_length, bin_height):
    
    # Generate random x and y coordinates, avoiding duplicates or coordinates on the same axis which are 1 away from each other.
    x_coords = []
    x_rounds = random.randint(40, 60)
    for round in range(x_rounds):
        x = random.randrange(2, bin_length - 2, 5)
        if x not in x_coords:
            x_coords.append(x)
    for x_coord in x_coords:
        short_length = random.randint(0,3)
        if x_coord + short_length < bin_length - 2:
            x_coords[x_coords.index(x_coord)] = x_coord + short_length

    y_coords = []
    y_rounds = random.randint(40, 60)
    for round in range(y_rounds):
        y = random.randrange(2, bin_height - 2, 5)
        if y not in y_coords:
            y_coords.append(y)
    for y_coord in y_coords:
        short_length = random.randint(0,3)
        if y_coord + short_length < bin_height - 2:
            y_coords[y_coords.index(y_coord)] = y_coord + short_length


    # Initialise bin
    bin = np.zeros((bin_height, bin_length), int)
    bin[0] = 1
    bin[-1] = 1
    for row in bin:
        row[0] += 1
        row[-1] += 1

    # Plot coord lines on bin
    for x_coord in x_coords:
        for row in bin:
            row[x_coord] += 1

    for y_coord in y_coords:
        bin[y_coord] += 1
    
    a, b = np.where(bin > 1)
    corners = list(zip(a, b))
    np.array(corners)
    print(corners)

    # Display bin
    # 1) Through table in Log File
    # table = tabulate(bin, headers=[i for i in range(bin_length)], tablefmt="fancy_grid")
    # logging.info(f'\n {table}')
    # 2) Through cmap
    plt.matshow(bin, cmap='Blues')
    plt.xticks([i for i in range(0, bin_length, 2)])
    plt.show()
    

# Implement Selection, Placement, and Filling (note filling is using the new 'sliding' heuristic)

# Main loop

# Bin parameters
bin_length = 100
bin_height = 50
create_rectangles(bin_length, bin_height)

