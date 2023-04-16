import numpy as np
import placement
import logging
import copy
import sys
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
        print('arrives here')
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


def djd(items, BIN_WIDTH, BIN_HEIGHT):
    waste = 0
    w = BIN_WIDTH * BIN_HEIGHT / 20

    objects = [[np.zeros((BIN_HEIGHT, BIN_WIDTH)), None]]
    bin_dict =  {'0':[]}

    colour = 1

    pieces_to_place = len(items)

    current_object = 0
    item = 0 # Don't modify items, use pointer rather than changing the list

    failed = []

    while pieces_to_place > 0:
        # Fill object until 1/3 area is covered
        while np.count_nonzero(objects[current_object][0]) < (BIN_WIDTH * BIN_HEIGHT / 3):
            object, fail_flag = placement.bottom_left(objects[current_object], items[item], BIN_WIDTH, BIN_HEIGHT, colour)
            colour = (2 * colour + 1) % 10
            if fail_flag == 0:
                failed.append(item)
            else:
                bin_dict[f'{current_object}'].append(item)
                item += 1
            objects[0] = object
        break
    return objects, bin_dict




# def djd(items, objects, BIN_WIDTH, BIN_HEIGHT, bin_dict, NUM_RECTANGLES):
#     waste = 0
#     w = BIN_WIDTH * BIN_HEIGHT / 20
#     colour = 1
#     all_items = copy.deepcopy(items) # doesn't change
#     current_object = 0
#     failed = []
#     unplaced_items = copy.deepcopy(items) # only contains unplaced items

#     while len(unplaced_items) > 0:
#         print(current_object, bin_dict)
#         logging.info(f'Waste:{waste}')
#         # item = items.pop(0)
#         placed_this_round = 0
    
#         while np.count_nonzero(objects[current_object][0]) < (BIN_WIDTH * BIN_HEIGHT / 3):
#             if current_object == 0:
#                 item = items.pop(0)
#                 object, fail_flag = placement.bottom_left(objects[current_object], item, BIN_WIDTH, BIN_HEIGHT, colour)
#                 colour = (2 * colour + 1) % 10
#                 if fail_flag == 0:
#                     failed.append(item)
#                 else:
#                     unplaced_items.remove(item)
#                     bin_dict[f'{current_object}'].append(item)
#             else:
#                 logging.info(f'Object {current_object}')
#                 item = unplaced_items.pop(0)
#                 object, fail_flag = placement.bottom_left(objects[current_object], item, BIN_WIDTH, BIN_HEIGHT, colour)
#                 colour = (2 * colour + 1) % 10
#                 if fail_flag == 0:
#                     failed.append(item)
#                     unplaced_items.insert(0,item)
#                 else:
#                     bin_dict[f'{current_object}'].append(item)
#             # item = items.pop(0)

#             logging.info(f'Initial filling: item {all_items.index(item)}: {item}')
#         # items.insert(0,item)
        
#         # Trying to place pieces one-by-one
#         break_out = False
#         while not break_out:
#             for item in unplaced_items: 
#                 logging.info(f'Considering item {all_items.index(item)}: {item}')
#                 free_space = BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(objects[current_object][0])
#                 logging.info(f'Free space is {free_space}')

#                 if (free_space) - item[0]*item[1] > waste:
#                     break_out = True
#                     logging.info(f'item {all_items.index(item)}: {item} has area {item[0]*item[1]} < Free space {free_space} - waste {waste} = {free_space-waste}. Largest item is too small')
#                     break # piece is too small
#                 if item[0]*item[1] > (BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(objects[current_object][0])):
#                     logging.info(f'item {all_items.index(item)}: {item} has area {item[0]*item[1]} > {(BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(objects[current_object][0]))}')
#                     continue # piece too big
#                 if item in failed:
#                     logging.info(f'item {all_items.index(item)}: {item} in failed list')
#                     continue # piece too big
#                 object, fail_flag = placement.bottom_left(objects[current_object], item, BIN_WIDTH, BIN_HEIGHT, colour)
#                 colour = (2 * colour + 1) % 10
#                 if fail_flag == 1:
#                     unplaced_items.remove(item)
#                     bin_dict[f'{current_object}'].append(item)
#                     placed_this_round = 1
#                     break_out = True
#                     break
#                 else:
#                     failed.append(item)
#                     logging.info(f'Failed list is {failed}')
#             if break_out:
#                 break
#             if fail_flag == 0:
#                 waste = 0 # start again trying pieces one-by-one                                                NEED TO ADD THIS CONDITION IN
#             else:
#                 break_out = True
#                 break

#         # Try pieces two by two
#         # for all pieces in order of decreasing size:
#         #   if objectFreeArea - pieceArea - largestPieceArea > waste:
#         #       break
#         #   if piece failed to fit or pieceArea + smallestPieceArea > freeSpace:
#         #       continue
#         #   try to place piece
#         #   if piece cannot be placed:
#         #       register in memory

#         #   else: (selecting second piece)
#         #   for all remaining pieces:
#         #   if objectFreeArea - area of 2 pieces > waste:
#         #       break
#         #   if piece or pair of pieces has failed to fit or area of 2 pieces > free space:
#         #       continue
#         #   try to place second piece
#         #   if piece could be placed
#         #       return
#         #   else:
#         #       unplace first piece and register that pair of pieces doesn't fit

#         # Try pieces three by three
#         # for all pieces in decreasing size:
#         #   if object free area - piece's area - area of 2 largest pieces > waste:
#         #       break
#             # if piece failed to fit or piece's area + 2 smallest pieces area > free space:
#             #   continue
#             # try to place piece 1
#             # if piece could not be placed:
#             #   register in memory
#             # else:
#         #       for all remaining pieces:
#         #           if object free area - area of 2  pieces - area of largest piece > waste:
#         #               break
#         #           if (piece or pair of pieces failed to fit) or area of 2 pieces + area of smallest piece > object free area:
#         #               continue
#         #           try to palce piece 2
#         #           if piece cannot be placed:
#         #               unplace first piece and register that pair doesn't fit
#         #           else:
#         #               for all remaining pieces:
#         #                   if object free area - area of 3 pieces > waste:
#         #                       break
#         #                   if (any piece, pair, or 3-piece group of pieces failed to fit) or area of 3 pieces > object free area:
#         #                       continue
#         #                   try to place 3rd piece in object
#         #                   if piece could be placed:
#         #                       return
#         #                   else:
#         #                       unplace first 2 pieces and register that 3-piece group does not fit  

#         if placed_this_round == 0 and waste < (BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(current_object)): #(BIN_WIDTH * BIN_HEIGHT - np.count_nonzero(current_object)) <= waste
#             logging.info(f'Incrementing waste')
#             waste += w
#         else:
#             objects.append([np.zeros((BIN_HEIGHT, BIN_WIDTH)), None])# open new object
#             current_object += 1
#             logging.info(f'New object {current_object}')
#             bin_dict[f'{current_object}'] = []
#             failed = []
#             print(items, len(items))
#     return objects


