import numpy as np
import placement
import logging
import copy
logger = logging.getLogger('my_module_name')
logging.basicConfig(filename='log.log',filemode='w', encoding='utf-8', level=logging.DEBUG)

def ff(items, objects, BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES):
    for i in range(len(items)):
        item = items.pop(0)
        logging.info(f'_____________________________________________________________________item {i} is {item}_____________________________________________________________________')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display

        # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
        can_place = False 
        for o in range(len(objects)):
            logging.info(f'Trying bin {o}')
            object, fail_flag = placement.bottom_left(objects[o], item, BIN_WIDTH, BIN_HEIGHT, j)
            if fail_flag != 0:
                can_place = True
                logging.info(f'Placed in bin {o}')
                bin_dict[f'{o}'].append(i)
                break
        if not can_place:
            objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
            bin = objects[-1]
            object, fail_flag = placement.bottom_left(bin, item, BIN_WIDTH, BIN_HEIGHT, j)
            if fail_flag != 0:
                logging.info(f'New bin {o+1} created and item {i} placed')
                bin_dict[f'{o+1}'] = [i]
            else:
                logging.info(f'Fatal error, item {i}:{item} larger than bin')
    return objects

def ffd(items, objects, BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES):
    pass

def nf(items, objects, BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES):
    current_object = 0

    for i in range(len(items)):
        item = items.pop(0)
        logging.info(f'_____________________________________________________________________item {i} is {item}, Current object is {current_object}_____________________________________________________________________')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display
        
        # Try to place in current object
        can_place = False 
        object, fail_flag = placement.bottom_left(objects[current_object], item, BIN_WIDTH, BIN_HEIGHT, j)
        if fail_flag != 0:
                can_place = True
                logging.info(f'Placed in current object: bin {current_object}')
                bin_dict[f'{current_object}'].append(i)

        # If cannot, iterate through other objects
        if not can_place:
            for o in range(len(objects)-1):
                logging.info(f'co: {current_object}, o:{o}, lo:{len(objects)}')
                new_current_object = (current_object + o + 1) % len(objects)
                logging.info(f'Trying bin {new_current_object}')
                object, fail_flag = placement.bottom_left(objects[new_current_object], item, BIN_WIDTH, BIN_HEIGHT, j)
                if fail_flag != 0:
                        can_place = True
                        logging.info(f'Placed in bin {new_current_object}')
                        bin_dict[f'{new_current_object}'].append(i)
                        break
            # If cannot place in any other object, create new object and place there
            if not can_place:
                objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
                current_object = len(objects) - 1
                object, fail_flag = placement.bottom_left(objects[current_object], item, BIN_WIDTH, BIN_HEIGHT, j)
                if fail_flag != 0:
                    logging.info(f'New bin {len(objects) - 1} created and item {i} placed')
                    bin_dict[f'{len(objects) - 1}'] = [NUM_RECTANGLES-len(items)-1]
                else:
                    logging.info(f'Fatal error, item {i}:{item} larger than bin')

    return objects

def nfd(items, objects, BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES):
    pass

def bf(items, objects, BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES):
    # Initially, operate in the same way as First fit until a second bin is opened
    for i in range(len(items)):
        item = items.pop(0)
        logging.info(f'_____________________________________________________________________item {i} is {item}_____________________________________________________________________')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display

        # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
        can_place = False 
        for o in range(len(objects)):
            logging.info(f'Trying bin {o}')
            object, fail_flag = placement.bottom_left(objects[o], item, BIN_WIDTH, BIN_HEIGHT, j)
            if fail_flag != 0:
                can_place = True
                logging.info(f'Placed in bin {o}')
                bin_dict[f'{o}'].append(i)
                break
        if not can_place:
            objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
            bin = objects[-1]
            object, fail_flag = placement.bottom_left(bin, item, BIN_WIDTH, BIN_HEIGHT, j)
            if fail_flag != 0:
                logging.info(f'New bin {o+1} created and item {i} placed')
                bin_dict[f'{o+1}'] = [i]
                break
            else:
                logging.info(f'Fatal error, item {i}:{item} larger than bin')
    
    logging.info('_____________________________________________________________________STARTING BEST PHASE_____________________________________________________________________')
    if len(items) > 0:
        # Start best-checking
        for i in range(len(items)):
            item = items.pop(0)
            logging.info(f'_____________________________________________________________________item {NUM_RECTANGLES-len(items)-1} is {item}_____________________________________________________________________')
            j = (2 * i + 1) % 10 # j-value determines colour of piece in display

            # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
            can_place = False 
            best_bin = objects[0]
            waste = BIN_WIDTH * BIN_HEIGHT
            for o in range(len(objects)):
                logging.info(f'Trying bin {o}')
                to_place = copy.deepcopy(objects[o])
                object, fail_flag = placement.bottom_left(to_place, item, BIN_WIDTH, BIN_HEIGHT, j)
                if fail_flag != 0:
                    can_place = True
                    if (BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(object)) < waste:
                        best_bin_index = o
                        best_bin = object
                        waste = np.count_nonzero(object)
            
            if can_place:
                logging.info(f'Placed in bin {best_bin_index}')
                objects[best_bin_index] = (best_bin,1)
                bin_dict[f'{best_bin_index}'].append(NUM_RECTANGLES-len(items)-1)

            if not can_place:
                objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
                bin = objects[-1]
                object, fail_flag = placement.bottom_left(bin, item, BIN_WIDTH, BIN_HEIGHT, j)
                if fail_flag != 0:
                    logging.info(f'New bin {o+1} created and item {i} placed')
                    bin_dict[f'{o+1}'] = [NUM_RECTANGLES-len(items)-1]
                else:
                    logging.info(f'Fatal error, item {i}:{item} larger than bin')
    return objects

def bfd(items, objects, BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES):
    pass

def djd(items, objects, BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES):
    waste = 0
    w = BIN_HEIGHT * BIN_WIDTH / 20 # value to increment waste by
    current_object = 0

    i = 0
    while len(items) > 0:
        # Fill bin until at least 1/3 area is covered. Store pieces that did not fit
        item = item.pop(0)
        logging.info(f'_____________________________________________________________________item {i} is {item}_____________________________________________________________________')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display
        i += 1

        object, fail_flag = placement.bottom_left(objects[0], item, BIN_WIDTH, BIN_HEIGHT, j)
        # if fail_flag == 1:
    #         items.pop(i)
    #     if np.count_nonzero(object) >= 1/3 * BIN_HEIGHT * BIN_WIDTH:
    #         break
    
    # remaining_space = BIN_HEIGHT * BIN_WIDTH - np.count_nonzero(object)

def djt(items, objects, BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES):
    pass

def filler(items, objects, BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES):
    pass