# SELECTION HEURISTIC FUNCTIONS

# Takes a list of item tuples [(width, height), ...] and bin dimensions
# Allocates every item to some bin, depending on the algorithm. Calls placement.py to place an item in a bin.
# Returns a list of objects containing all items, and a dictionary mapping items to bins called bin_dict.

import numpy as np
import placement
import logging
import copy
import sys
logger = logging.getLogger('my_module_name')
logging.basicConfig(filename='log.log',filemode='w', encoding='utf-8', level=logging.DEBUG)

# FIRST FIT: Rank the created bins in a queue. Insert item into first bin where it fits
def ff(rectangles, BIN_WIDTH, BIN_HEIGHT):
    items = copy.deepcopy(rectangles)

    # initialise the return variables
    bin_dict = {'0':[]}
    objects =  [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]

    for i in range(len(items)):
        item = items.pop(0)
        logging.info(f'item {i}:{item}')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display

        # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
        can_place = False 
        for o in range(len(objects)):
            logging.info(f'Trying bin {o}')
            object, success_flag = placement.bottom_left(objects[o], item, j)
            if success_flag == 1:
                can_place = True
                logging.info(f'Placed in bin {o}')

                # Update return variables
                objects[o] = object
                bin_dict[f'{o}'].append(i)
                break

        # Cannot fit in any bin. Create a new bin and place the item.
        if not can_place:
            objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
            object, success_flag = placement.bottom_left(objects[-1], item, j)
            if success_flag == 1:
                logging.info(f'New bin {o+1} created and item {i} placed')
                objects[-1] = object
                bin_dict[f'{o+1}'] = [i]
            else:
                logging.info(f'Fatal error, item {i}:{item} larger than bin')
    return objects, bin_dict

# FIRST FIT DECREASING: SAME AS ABOVE, BUT SORT ITEMS BY DECREASING AREA FIRST
def ffd(rectangles, BIN_WIDTH, BIN_HEIGHT):
    items = copy.deepcopy(rectangles)
    
    # sort by decreasing area
    areas = [(item[0]*item[1], item) for item in items]
    areas.sort(reverse=True)
    items = [areas[i][1] for i in range(len(areas))]
    
    # initialise the return variables
    bin_dict = {'0':[]}
    objects =  [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]

    for i in range(len(items)):
        item = items.pop(0)
        logging.info(f'item {i}:{item}')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display

        # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
        can_place = False 
        for o in range(len(objects)):
            logging.info(f'Trying bin {o}')
            object, success_flag = placement.bottom_left(objects[o], item, j)
            if success_flag == 1:
                can_place = True
                logging.info(f'Placed in bin {o}')

                # Update return variables
                objects[o] = object
                bin_dict[f'{o}'].append(rectangles.index(item))
                break

        # Cannot fit in any bin. Create a new bin and place the item.
        if not can_place:
            objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
            object, success_flag = placement.bottom_left(objects[-1], item, j)
            if success_flag == 1:
                logging.info(f'New bin {o+1} created and item {i} placed')
                objects[-1] = object
                bin_dict[f'{o+1}'] = [rectangles.index(item)]
            else:
                logging.info(f'Fatal error, item {i}:{item} larger than bin')
    return objects, bin_dict

# NEXT FIT: Maintain a 'current bin' to keep pieces in. When unable to place a piece, use the next bin. 
#   When unable to place in any bin, create a new one.
def nf(rectangles, BIN_WIDTH, BIN_HEIGHT):
    items = copy.deepcopy(rectangles)

    # initialise the return variables
    bin_dict = {'0':[]}
    objects =  [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]
    
    # Set pointer to the current object
    current_object = 0

    for i in range(len(items)):
        item = items.pop(0)
        logging.info(f'item {i} is {item}, Current object is {current_object}')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display
        
        # Try to place in current object
        can_place = False 
        object, success_flag = placement.bottom_left(objects[current_object], item, j)
        if success_flag == 1:
            can_place = True
            logging.info(f'Placed in current object: bin {current_object}')

            # Update return variables
            bin_dict[f'{current_object}'].append(i)
            objects[current_object] = object

        # If cannot, iterate through other objects
        if not can_place:
            for o in range(len(objects)-1):
                logging.info(f'co: {current_object}, o:{o}, lo:{len(objects)}')
                new_current_object = (current_object + o + 1) % len(objects)
                logging.info(f'Trying bin {new_current_object}')
                object, success_flag = placement.bottom_left(objects[new_current_object], item, j)
                if success_flag == 1:
                    can_place = True
                    logging.info(f'Placed in bin {new_current_object}')

                    # update return variables
                    bin_dict[f'{new_current_object}'].append(i)
                    objects[new_current_object] = object
                    break
            # If cannot place in any other object, create new object and place there
            if not can_place:
                objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
                current_object = len(objects) - 1
                object, success_flag = placement.bottom_left(objects[current_object], item, j)
                if success_flag == 1:
                    logging.info(f'New bin {len(objects) - 1} created and item {i} placed')
                    # Update return variables
                    bin_dict[f'{len(objects) - 1}'] = [len(rectangles)-len(items)-1]
                    objects[current_object] = object
                else:
                    logging.info(f'Fatal error, item {i}:{item} larger than bin')

    return objects, bin_dict

# NEXT FIT DECREASING: SAME AS ABOVE, BUT SORT ITEMS BY DECREASING AREA FIRST
def nfd(rectangles, BIN_WIDTH, BIN_HEIGHT):
    items = copy.deepcopy(rectangles)

    # sort by decreasing area
    areas = [(item[0]*item[1], item) for item in items]
    areas.sort(reverse=True)
    items = [areas[i][1] for i in range(len(areas))]

    # initialise the return variables
    bin_dict = {'0':[]}
    objects =  [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]
    
    # Set pointer to the current object
    current_object = 0

    for i in range(len(items)):
        item = items.pop(0)
        logging.info(f'item {i} is {item}, Current object is {current_object}')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display
        
        # Try to place in current object
        can_place = False 
        object, success_flag = placement.bottom_left(objects[current_object], item, j)
        if success_flag == 1:
            can_place = True
            logging.info(f'Placed in current object: bin {current_object}')

            # Update return variables
            bin_dict[f'{current_object}'].append(i)
            objects[current_object] = object

        # If cannot, iterate through other objects
        if not can_place:
            for o in range(len(objects)-1):
                logging.info(f'co: {current_object}, o:{o}, lo:{len(objects)}')
                new_current_object = (current_object + o + 1) % len(objects)
                logging.info(f'Trying bin {new_current_object}')
                object, success_flag = placement.bottom_left(objects[new_current_object], item, j)
                if success_flag == 1:
                    can_place = True
                    logging.info(f'Placed in bin {new_current_object}')

                    # update return variables
                    bin_dict[f'{new_current_object}'].append(i)
                    objects[new_current_object] = object
                    break
            # If cannot place in any other object, create new object and place there
            if not can_place:
                objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
                current_object = len(objects) - 1
                object, success_flag = placement.bottom_left(objects[current_object], item, j)
                if success_flag == 1:
                    logging.info(f'New bin {len(objects) - 1} created and item {i} placed')
                    # Update return variables
                    bin_dict[f'{len(objects) - 1}'] = [len(rectangles)-len(items)-1]
                    objects[current_object] = object
                else:
                    logging.info(f'Fatal error, item {i}:{item} larger than bin')

    return objects, bin_dict

# BEST FIT: Places the item in the bin with the least free area. When unable to place, create a new bin.

def bf(rectangles, BIN_WIDTH, BIN_HEIGHT):
    items = copy.deepcopy(rectangles)

    # initialise the return variables
    bin_dict = {'0':[]}
    objects =  [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]

    logging.info(f'Initial filling (only 1 bin available)')
    for i in range(len(items)):
        item = items.pop(0)
        logging.info(f'item {i}:{item}')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display

        # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
        can_place = False 
        for o in range(len(objects)):
            logging.info(f'Trying bin {o}')
            object, success_flag = placement.bottom_left(objects[o], item, j)
            if success_flag == 1:
                can_place = True

                # Update return variables
                objects[o] = object
                bin_dict[f'{o}'].append(i)
                break

        # Cannot fit in any bin. Create a new bin and place the item.
        if not can_place:
            logging.info(f'New bin {o+1} created')
            objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
            object, success_flag = placement.bottom_left(objects[-1], item, j)
            if success_flag == 1:
                # update return variables
                objects[-1] = object
                bin_dict[f'{o+1}'] = [i]
                break
            else:
                logging.info(f'Fatal error, item {i}:{item} larger than bin')
    
    if len(items) > 0:
        logging.info('START BEST BIN')
        # For each remaining item, iterate through all bins and allocate item to the best bin
        for i in range(len(items)):
            item = items.pop(0)
            logging.info(f'item {len(rectangles)-len(items)-1} is {item}')
            j = (2 * i + 1) % 10 # j-value determines colour of piece in display

            # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
            can_place = False 
            best_bin = objects[0]
            waste = BIN_WIDTH * BIN_HEIGHT

            for o in range(len(objects)):
                logging.info(f'Trying bin {o}')
                object, success_flag = placement.bottom_left(objects[o], item, j)
                if success_flag == 1:
                    can_place = True
                    if (BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(object[0])) < waste:
                        best_bin_index = o
                        best_bin = object
                        waste = BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(object[0])
            
            if can_place:
                logging.info(f'Placed in bin {best_bin_index}')
                # update return variables
                bin_dict[f'{best_bin_index}'].append(len(rectangles)-len(items)-1)
                objects[best_bin_index] = best_bin

            if not can_place:
                objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
                object, success_flag = placement.bottom_left(objects[-1], item, j)
                if success_flag == 1:
                    logging.info(f'New bin {o+1} created and item {rectangles.index(item)} placed')
                    objects[-1] = object
                    bin_dict[f'{o+1}'] = [rectangles.index(item)]
                else:
                    logging.info(f'Fatal error, item {i}:{item} larger than bin')
    return objects, bin_dict


# BEST FIT DECREASING: SAME AS ABOVE, BUT SORT ITEMS BY DECREASING AREA FIRST
def bfd(rectangles, BIN_WIDTH, BIN_HEIGHT):
    items = copy.deepcopy(rectangles)

    # sort by decreasing area
    areas = [(item[0]*item[1], item) for item in items]
    areas.sort(reverse=True)
    items = [areas[i][1] for i in range(len(areas))]

    # initialise the return variables
    bin_dict = {'0':[]}
    objects =  [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]

    logging.info(f'Initial filling (only 1 bin available)')
    for i in range(len(items)):
        item = items.pop(0)
        logging.info(f'item {i}:{item}')
        j = (2 * i + 1) % 10 # j-value determines colour of piece in display

        # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
        can_place = False 
        for o in range(len(objects)):
            logging.info(f'Trying bin {o}')
            object, success_flag = placement.bottom_left(objects[o], item, j)
            if success_flag == 1:
                can_place = True

                # Update return variables
                objects[o] = object
                bin_dict[f'{o}'].append(rectangles.index(item))
                break

        # Cannot fit in any bin. Create a new bin and place the item.
        if not can_place:
            logging.info(f'New bin {o+1} created')
            objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
            object, success_flag = placement.bottom_left(objects[-1], item, j)
            if success_flag == 1:
                # update return variables
                objects[-1] = object
                bin_dict[f'{o+1}'] = [rectangles.index(item)]
                break
            else:
                logging.info(f'Fatal error, item {i}:{item} larger than bin')
    
    if len(items) > 0:
        logging.info('START BEST BIN')
        # For each remaining item, iterate through all bins and allocate item to the best bin
        for i in range(len(items)):
            item = items.pop(0)
            logging.info(f'item {len(rectangles)-len(items)-1} is {item}')
            j = (2 * i + 1) % 10 # j-value determines colour of piece in display

            # Try to place rectangle. If possible, return updated bin and NONE. Else, return bin and item
            can_place = False 
            best_bin = objects[0]
            waste = BIN_WIDTH * BIN_HEIGHT

            for o in range(len(objects)):
                logging.info(f'Trying bin {o}')
                object, success_flag = placement.bottom_left(objects[o], item, j)
                if success_flag == 1:
                    can_place = True
                    if (BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(object[0])) < waste:
                        best_bin_index = o
                        best_bin = object
                        waste = BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(object[0])
            
            if can_place:
                logging.info(f'Placed in bin {best_bin_index}')
                # update return variables
                bin_dict[f'{best_bin_index}'].append(rectangles.index(item))
                objects[best_bin_index] = best_bin

            if not can_place:
                objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
                object, success_flag = placement.bottom_left(objects[-1], item, j)
                if success_flag == 1:
                    logging.info(f'New bin {o+1} created and item {rectangles.index(item)} placed')
                    objects[-1] = object
                    bin_dict[f'{o+1}'] = [rectangles.index(item)]
                else:
                    logging.info(f'Fatal error, item {i}:{item} larger than bin')
    return objects, bin_dict

# DJANG AND FITCH: Fill the current object until it is >= 1/3 full. Look for combinations of 1/2/3 items that can 
#   be added to the object to leave unoccupied area <= waste. If no pieces can be placed, increment waste. Otherwise,
#   open a new bin.

# AUXILIARY FUNCTIONS FOR DJD

# Alg 2: Takes a list of unplaced items, a bin, the waste limit, and a list of items which have failed to be place i the bin
    # Tries to find a single item that can be added to the bin such that the free space in the bin <= waste
    # Returns updated unplaced list, updated bin, updated failed list, and success flag
def alg2(unplaced_items, bin, failed_list, waste, BIN_WIDTH, BIN_HEIGHT):
    
    items = copy.deepcopy(unplaced_items)
    object = copy.deepcopy(bin)
    failed = copy.deepcopy(failed_list)

    object_free_area = BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(object[0])
    logging.info(f'alg 2: ofa: {object_free_area}')
    for item in items:
        logging.info(f'considering {item}')
        item_area = item[0] * item[1]
        
        if object_free_area - item_area > waste:
            logging.info(f'ofa {object_free_area} - aop {item_area} = {object_free_area - item_area}> waste {waste}')
            break # item is too small to fill free area, need to increment waste

        if (item_area > object_free_area) or item in failed:
            logging.info(f'Item doesnt fit')
            continue # item is too big/doesn't fit, get next smallest item

        object, success_flag = placement.bottom_left(object, item, (2 * (items.index(item)) + 1) % 10)
        if success_flag == 1:
            items.remove(item)
            return items, object, failed, 1, item
        
        else:
            failed.append(item)
            logging.info(f'updated failed: {failed}')
    
    return items, object, failed, 0, -1
    

def djd(rectangles, BIN_WIDTH, BIN_HEIGHT):
    # sort by decreasing area
    sorted_items = copy.deepcopy(rectangles) 
    areas = [(item[0]*item[1], item) for item in sorted_items]
    areas.sort(reverse=True)
    sorted_items = [areas[i][1] for i in range(len(areas))] # Unchanged, used for indexing and logging post-sorting

    unplaced_items = copy.deepcopy(sorted_items) # Remove item from unplaced every time it is placed

    # initialise the return variables
    bin_dict = {'0':[]}
    objects =  [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]
    
    waste = 0
    w = BIN_WIDTH * BIN_HEIGHT / 20

    # Set pointer to the current object
    current_object = 0

    # Set a index for the current item, note that this is with respect to the post-sorting order
    current_item = 0
    
    failed = []
    while len(unplaced_items) > 0:
        placed_items = []
        # Fill object to at least 1/3 capacity
        for current_item in range(len(unplaced_items)):
            if np.count_nonzero(objects[current_object][0]) >= (BIN_WIDTH * BIN_HEIGHT / 3):
                break
            else:
                item = unplaced_items[current_item]
                j = (2 * (current_item) + 1) % 10

                object, success_flag = placement.bottom_left(objects[current_object], item, j)
                if success_flag == 1:
                    placed_items.append(unplaced_items[current_item])
                    objects[current_object] = object
                    bin_dict[f'{current_object}'].append(unplaced_items[current_item])
                    logging.info(f'{unplaced_items[current_item]} added in third filling')
                else:
                    failed.append(unplaced_items[current_item])
                    logging.info(f'updated failed: {failed}')
        for i in placed_items:
            unplaced_items.remove(i)
        
        # Try pieces 1-by-1
        items, object, failed_list, alg2_flag, placed_item = alg2(unplaced_items, objects[current_object], failed, waste, BIN_WIDTH, BIN_HEIGHT)
        unplaced_items = items
        objects[current_object] = object
        failed = failed_list

        if alg2_flag == 1:
            logging.info(f'{placed_item} placed by 1-grouping')
            waste = 0
            # Update return variable
            bin_dict[f'{current_object}'].append(placed_item)

        else:
            object_free_area =  BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(objects[current_object][0])
            if waste < object_free_area:
                waste += w
                logging.info(f'Waste is {waste}')
            # Next object
            else: 
                logging.info(f'Piece placed, resetting and going to next object')
                if len(unplaced_items) > 0:
                    current_object += 1
                    objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
                    bin_dict[f'{current_object}'] = []
                    failed = []
                    placed_items = []

    # Reformat bin_dict to consider indices of pieces in original items list, not actual piece dimensions
    new_bin_dict = {key:[] for key in bin_dict}
    for key in bin_dict:
        for rectangle in bin_dict[key]:
            new_rectangle = rectangles.index(rectangle)
            new_bin_dict[key].append(new_rectangle)

    return objects, new_bin_dict


def alg3(unplaced_items, bin, failed_list, failed_list_2d,  waste, BIN_WIDTH, BIN_HEIGHT):
    items = copy.deepcopy(unplaced_items)
    object = copy.deepcopy(bin)
    failed = copy.deepcopy(failed_list)
    failed_2d = copy.deepcopy(failed_list_2d)

    object_free_area = BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(object[0])
    logging.info(f'alg 3: ofa: {object_free_area}')
    for item in items:
        logging.info(f'First item {item}')
        item_area = item[0] * item[1]
        if len(items) < 2:
            logging.info(f'Short on items. Only {len(items)} item(s) remaining')
            break
        largest_item = items[0] if items[0] != item else items[1]
        if object_free_area - item_area - largest_item[0] * largest_item[1]  > waste:
            logging.info(f'First item too small. ofa {object_free_area} - aop {item_area} = {object_free_area - item_area - largest_item[0] * largest_item[1]} > waste {waste}')
            break # item is too small to fill free area, need to increment waste
        smallest_item = items[-1] if items[-1] != item else items[-2]
        if (item_area + smallest_item[0] * smallest_item[1] > object_free_area) or item in failed:
            logging.info(f'First item too big/doesnt fit')
            continue # item is too big/doesn't fit, get next smallest item
        potential_object, success_flag = placement.bottom_left(object, item, (2 * (items.index(item)) + 1) % 10)
        if success_flag == 0:
            failed.append(item)
            logging.info(f'updated failed: {failed}')
        else:
            for second_item in items:
                if second_item != item:
                    logging.info(f'Second item {second_item}')
                    second_item_area = second_item[0] * second_item[1]
                    if object_free_area - item_area - second_item_area > waste:
                        logging.info(f'The two items are too small. Trying a new first item. ofa {object_free_area} - aop {item_area} - aop2 {second_item_area}= {object_free_area - item_area - second_item_area} > waste {waste}')
                        break
                    if (item_area + second_item_area > object_free_area) or (item in failed) or ((item, second_item) in failed_2d):
                        logging.info(f'Second item too big/doesnt fit')
                        continue
                    new_object, success_flag = placement.bottom_left(potential_object, second_item, (2 * (items.index(second_item)) + 1) % 10)
                    if success_flag == 1:
                        items.remove(item)
                        items.remove(second_item)
                        return items, new_object, failed, failed_2d, 1, item, second_item
            
            failed_2d.append((item, second_item))
            logging.info(f'updated failed_2d: {failed_2d}')
    
    return items, object, failed, failed_2d, 0, -1, -1


def djd2(rectangles, BIN_WIDTH, BIN_HEIGHT):
    # sort by decreasing area
    sorted_items = copy.deepcopy(rectangles) 
    areas = [(item[0]*item[1], item) for item in sorted_items]
    areas.sort(reverse=True)
    sorted_items = [areas[i][1] for i in range(len(areas))] # Unchanged, used for indexing and logging post-sorting

    unplaced_items = copy.deepcopy(sorted_items) # Remove item from unplaced every time it is placed

    # initialise the return variables
    bin_dict = {'0':[]}
    objects =  [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]
    
    waste = 0
    w = BIN_WIDTH * BIN_HEIGHT / 20

    # Set pointer to the current object
    current_object = 0

    # Set a index for the current item, note that this is with respect to the post-sorting order
    current_item = 0
    
    failed = []
    failed_2d = []
    while len(unplaced_items) > 0:
        placed_items = []
        # Fill object to at least 1/3 capacity
        for current_item in range(len(unplaced_items)):
            if np.count_nonzero(objects[current_object][0]) >= (BIN_WIDTH * BIN_HEIGHT / 3):
                break
            else:
                item = unplaced_items[current_item]
                j = (2 * (current_item) + 1) % 10

                object, success_flag = placement.bottom_left(objects[current_object], item, j)
                if success_flag == 1:
                    placed_items.append(unplaced_items[current_item])
                    objects[current_object] = object
                    bin_dict[f'{current_object}'].append(unplaced_items[current_item])
                    logging.info(f'{unplaced_items[current_item]} added in third filling')
                else:
                    failed.append(unplaced_items[current_item])
                    logging.info(f'updated failed: {failed}')
        for i in placed_items:
            unplaced_items.remove(i)
        
        waste_flag = 0
        while True:
            # Try pieces 1-by-1
            items, object, failed_list, alg2_flag, placed_item = alg2(unplaced_items, objects[current_object], failed, waste, BIN_WIDTH, BIN_HEIGHT)
            unplaced_items = items
            objects[current_object] = object
            failed = failed_list

            if alg2_flag == 1:
                waste_flag = 1
                logging.info(f'{placed_item} placed by 1-grouping')
                waste = 0
                # Update return variable
                bin_dict[f'{current_object}'].append(placed_item)
                continue

            else:
                items, object, failed_list, failed_list_2d, alg3_flag, placed_item, second_placed_item = alg3(unplaced_items, objects[current_object], failed, failed_2d, waste, BIN_WIDTH, BIN_HEIGHT)
                unplaced_items = items
                objects[current_object] = object
                failed = failed_list
                failed_2d = failed_list_2d

                if alg3_flag == 1:
                    waste_flag = 1
                    logging.info(f'{placed_item} placed by 2-grouping')
                    logging.info(f'{second_placed_item} placed by 2-grouping')
                    waste = 0
                    # Update return variable
                    bin_dict[f'{current_object}'].append(placed_item)
                    bin_dict[f'{current_object}'].append(second_placed_item)
                    continue
                else:
                    break

        object_free_area =  BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(objects[current_object][0])
        if waste_flag == 0 and waste < object_free_area:
            waste += w
            logging.info(f'Waste is {waste}')
        # Next object
        else: 
            logging.info(f'Piece placed, resetting and going to next object')
            if len(unplaced_items) > 0:
                current_object += 1
                objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])
                bin_dict[f'{current_object}'] = []
                failed = []
                failed_2d = []
                placed_items = []

    # Reformat bin_dict to consider indices of pieces in original items list, not actual piece dimensions
    new_bin_dict = {key:[] for key in bin_dict}
    for key in bin_dict:
        for rectangle in bin_dict[key]:
            new_rectangle = rectangles.index(rectangle)
            new_bin_dict[key].append(new_rectangle)

    return objects, new_bin_dict
    

