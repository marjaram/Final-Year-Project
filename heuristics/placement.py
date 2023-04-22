# BOTTOM LEFT HEURISTIC FUNCTION

# Takes a bin tuple: (matrix, empty_flag, colour) and item (width, height)
# If item can be placed:
    # Returns a bin tuple: (updated matrix, success_flag=1)
# Otherwise:
    # Returns a bin tuple: (original matrix, success_flag = 0)

import logging
import copy
logger = logging.getLogger('my_module_name')
logging.basicConfig(filename='log.log',filemode='w', encoding='utf-8', level=logging.DEBUG)

def bottom_left(bin, item, i):
    object = copy.deepcopy(bin[0])
    BIN_HEIGHT = len(object)
    BIN_WIDTH = len(object[0])
    
    if bin[1] is None: # Bin is empty, insert shape into bottom left
        object[BIN_HEIGHT-item[1]:BIN_HEIGHT, :item[0]] += i
        # Define points to help with future placement
        rightmost = (item[0] - 1, BIN_HEIGHT - item[1]) # rightmost: the highest point of the furthest right shape
        uppermost = (item[0] - 1, BIN_HEIGHT - item[1]) # uppermost: the furthest right point of the tallest shape
        upperrightmost = (rightmost[0], uppermost[1]) # theoretical position, such that no shapes are beyond this point
        empty_flag = (rightmost, uppermost, upperrightmost)
        return [object,empty_flag], 1
    else:
        rightmost = (BIN_WIDTH-1, 0)
        uppermost = (BIN_WIDTH-1, 0)
        upperrightmost = (BIN_WIDTH-1, 0)
        current_pos = (BIN_WIDTH-1, 0)
        object[:item[1], BIN_WIDTH-item[0]:] += i # insert new piece
        
        # Check if piece can be placed
        col = object[current_pos[1]: current_pos[1]+ item[1], current_pos[0]-item[0]+1] % 2
        row = object[current_pos[1] + item[1] - 1, current_pos[0]-item[0]+1:current_pos[0]+1] % 2
        if 0 in row or 0 in col:
            object[:item[1], BIN_WIDTH-item[0]:] -= i
            return [object, bin[1]], 0

        stable = False
        while not stable:
            prev_pos = current_pos

            # Move piece down
            not_break = True
            while not_break and (current_pos[1] + item[1] < BIN_HEIGHT):
                object[current_pos[1] + item[1], current_pos[0]-item[0]+1:current_pos[0]+1] += i
                row = object[current_pos[1] + item[1], current_pos[0]-item[0]+1:current_pos[0]+1]%2
                if 0 in row: # clash detected; move piece back up
                    object[current_pos[1] + item[1], current_pos[0]-item[0]+1:current_pos[0]+1] -= i
                    not_break = False
                else:
                    object[current_pos[1], current_pos[0]-item[0]+1:current_pos[0]+1] = 0
                    current_pos = (current_pos[0],current_pos[1]+1)

            # Move piece left
            not_break = True
            while not_break and (current_pos[0] - item[0] >= 0):
                object[current_pos[1]: current_pos[1]+ item[1], current_pos[0]-item[0]] += i
                col = object[current_pos[1]: current_pos[1]+ item[1], current_pos[0]-item[0]]%2
                if 0 in col:
                    object[current_pos[1]: current_pos[1]+ item[1], current_pos[0]-item[0]] -= i
                    not_break = False
                else:
                    object[current_pos[1]: current_pos[1]+ item[1], current_pos[0]] = 0
                    current_pos = (current_pos[0] - 1, current_pos[1])
            
            # Stop when stable position reached
            if prev_pos == current_pos:
                stable = True
                if current_pos[0] >= rightmost[0]:
                    rightmost = current_pos
                    upperrightmost = (rightmost[0], uppermost[1])
                if current_pos[1] <= uppermost[1]:
                    uppermost = current_pos
                    upperrightmost = (rightmost[0], uppermost[1])

        return [object,bin[1]],1
       