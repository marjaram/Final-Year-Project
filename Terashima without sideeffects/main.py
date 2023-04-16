import selection
import numpy as np
seed = np.random.default_rng()

def generate_rectangles(BIN_WIDTH=100, BIN_HEIGHT=100, NUM_RECTANGLES=20):
    # Generate widths and heights of rectangles between 1 and 2/3 bin dimensions
    widths = seed.integers(1,2*(BIN_WIDTH - 1)/3, NUM_RECTANGLES)
    heights = seed.integers(1,2*(BIN_WIDTH - 1)/3, NUM_RECTANGLES)
    rectangles = list(zip(widths, heights))
    np.random.shuffle(rectangles)

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

    problem_label = (huge, large, medium, small, tall, average, short)
    return rectangles, problem_label

def fitness_function(object_list): 
    fraction_util = 0
    for object in object_list:
        fraction_util += ((np.count_nonzero(object[0]))/(BIN_HEIGHT*BIN_WIDTH))**2
    fitness = fraction_util/len(object_list)

    return fitness

# Main Loop
BIN_HEIGHT = 1000
BIN_WIDTH = 1000
NUM_RECTANGLES = 30

for problem_instace in range(1000):
    items, label = generate_rectangles(BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES)

    ff_objects, ff_bin_dict = selection.ff(items,BIN_WIDTH,BIN_HEIGHT)
    ffd_objects, ffd_bin_dict = selection.ffd(items,BIN_WIDTH,BIN_HEIGHT)
    nf_objects, nf_bin_dict = selection.nf(items,BIN_WIDTH,BIN_HEIGHT)
    nfd_objects, nfd_bin_dict = selection.nfd(items,BIN_WIDTH,BIN_HEIGHT)
    bf_objects, bf_bin_dict = selection.bf(items,BIN_WIDTH,BIN_HEIGHT)
    bfd_objects, bfd_bin_dict = selection.bfd(items,BIN_WIDTH,BIN_HEIGHT)
    djd_objects, djd_bin_dict = selection.djd(items,BIN_WIDTH,BIN_HEIGHT)

    solutions = {'ff':ff_objects, 'ffd':ffd_objects, 'nf':nf_objects, 'nfd':nfd_objects, 'bf':bf_objects, 'bfd':bfd_objects, 'djd':djd_objects}
    fitness = fitness_function(ff_objects)
    best_solution = 'ff'
    for solution in solutions:
        new_fitness = fitness_function(solutions[solution])
        print(f'{solution}: {new_fitness:.4f}')
        if new_fitness > fitness:
            fitness = new_fitness
            best_solution = solution
        
    print(f'Problem: {problem_instace}, label: {label}, best solution: {best_solution}')    

