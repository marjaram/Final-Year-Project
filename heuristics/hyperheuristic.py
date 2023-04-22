import math
import sys
import numpy as np
import pandas as pd
import ast
import logging
import placement
seed = np.random.default_rng()
logger = logging.getLogger('my_module_name')
logging.basicConfig(filename='log.log',filemode='w', encoding='utf-8', level=logging.DEBUG)

###################################################### AUXILIARY FUNCTIONS ######################################################

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


def euclidean_distance(chromosome_block, problem_label):
    ed_total = 0
    for index in range(7):
        ed_total += (chromosome_block[index] - problem_label[index]) ** 2
    return math.sqrt(ed_total)


############################################# MAIN CODE ###############################################################

POPULATION_SIZE = 10
BIN_WIDTH = 100
BIN_HEIGHT = 100
NUM_RECTANGLES = 20

training_data_set = pd.read_csv('low_level_scores_training_set_0.csv')
training_data_set['Labels'] = training_data_set['Labels'].apply(lambda x: ast.literal_eval(x))
testing_data_set = pd.read_csv('testing_set.csv')
testing_data_set['Labels'] = testing_data_set['Labels'].apply(lambda x: ast.literal_eval(x))

# Generate initial population
    # 10 individuals. Each individual has a random number of labels (2-5% of training set size)
population = []
for i in range(POPULATION_SIZE):
    chromosome = []
    num_blocks = seed.integers(0.02*len(training_data_set), 0.05*len(training_data_set))
    for j in range(num_blocks):
        index = seed.choice([row for row in range(len(training_data_set))])
        chromosome.append(training_data_set.iloc[index]['Labels'])
    population.append(chromosome)

# Assign 5 problems to each individual and compute fitness
items1, label1 = generate_rectangles(seed, BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES)
items2, label2 = generate_rectangles(seed, BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES)
items3, label3 = generate_rectangles(seed, BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES)
items4, label4 = generate_rectangles(seed, BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES)
items5, label5 = generate_rectangles(seed, BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES)
    
problem1 = [items1, label1]
problem2 = [items2, label2]
problem3 = [items3, label3]
problem4 = [items4, label4]
problem5 = [items5, label5]

problems = [problem1, problem2, problem3, problem4, problem5]
for chromosome in population:
    for problem in problems:
        solution_bin_dict = {'0':[]}
        solution_objects =  [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]
        items = problem[0]

        while problem[1][7] != 0: # Problem not solved, pieces still remaining
            # Find closest (euclidean distance) block in chromosome to the problem label, and choose associated selection heuristic
            closest_block = -1
            shortest_distance = 800
            for block in chromosome:
                if euclidean_distance(block, problem[1]) < shortest_distance:
                    closest_block = block
                    shortest_distance = euclidean_distance(block, problem[1])
            
            selection_heuristic = closest_block[-1]

            # Apply first fit
            if selection_heuristic == 0: 
                item = items.pop(0)
                logging.info(f'item {i}:{item}')
                j = seed.choice[1,3,5,7,9]

                # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
                can_place = False 
                for o in range(len(solution_objects)):
                    logging.info(f'Trying bin {o}')
                    object, success_flag = placement.bottom_left(solution_objects[o], item, j)
                    if success_flag == 1:
                        can_place = True
                        logging.info(f'Placed in bin {o}')

                        # Update return variables and label(area, height, remaining pieces)
                        solution_objects[o] = object
                        solution_bin_dict[f'{o}'].append(i)
                        break

                # Cannot fit in any bin. Create a new bin and place the item.
                if not can_place:
                    solution_objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
                    object, success_flag = placement.bottom_left(solution_objects[-1], item, j)
                    if success_flag == 1:
                        logging.info(f'New bin {o+1} created and item {i} placed')
                        solution_objects[-1] = object
                        solution_bin_dict[f'{o+1}'] = [i]

                # Update label
                area = item[0] * item[1]
                height = item[1]
                remaining_pieces = items

                if area > (BIN_WIDTH * BIN_HEIGHT)/2:
                    pass   
                elif (BIN_WIDTH * BIN_HEIGHT)/2 >= area > (BIN_WIDTH * BIN_HEIGHT)/3:
                    pass
                elif (BIN_WIDTH * BIN_HEIGHT)/3 >= area > (BIN_WIDTH * BIN_HEIGHT)/4:
                    pass
                else:
                    pass

                


            # Apply First fit decreasing
            elif selection_heuristic == 1:
                pass
            elif selection_heuristic == 2: # Next fit
                pass
            elif selection_heuristic == 3: # Next fit decreasing
                pass
            elif selection_heuristic == 4: # Best fit
                pass
            elif selection_heuristic == 5: # Best fit decreasing
                pass
            elif selection_heuristic == 6: # DJD
                pass
            elif selection_heuristic == 7: # DJD2
                pass

            # Apply selection heuristic one step and update state attached to point
            sys.exit()


            # Update state to P'
        # Store solution in dictionary 
    # Calculate fitness using ff(k) - bsh(k)

# Apply selection, crossover, mutation to produce 2 children
    # Selection 1: choose k (the tournament size) individuals from the population at random
        # choose the best individual from the tournament with probability p
        # choose the second best individual with probability p*(1-p)
        # choose the third best individual with probability p*((1-p)^2)
        # and so on
    # Crossover 1: 2-point crossover. For both parents, use a uniform distribution to randomly sample for which block is chosen (different for both parents).
        # Then use the same method to randomly sample a point in the block to crossover (same for both parents)
    # Crossover 2: Exchange 10% of blocks between parents, meaning that child 1 inherits 90% from parent 1 and 10% from parent 2, and vice versa for child 2.
    # Mutation 1: Randomly generate new block and add to end of chromosome
    # Mutation 2: Randomly select a block and remove it from the chromosome
    # Mutation 3: Randomly select a block and a point in the block, and replace the value with a new number between 3 and -3, using a normal distribution with mean 0.5, and truncated.
# Assign 5 problems to each child and compute fitness (see other fitness function)
# Replace 2 worst individuals with new offspring
# Assign new problem to every individual in new population and compute fitness (see l)