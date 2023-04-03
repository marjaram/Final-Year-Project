############################################################################# Imports and setup #####################################################################################################
import numpy as np
import matplotlib.pyplot as plt
import sys
np.set_printoptions(threshold=sys.maxsize)

def bottom_left(bin, item, BIN_WIDTH, BIN_HEIGHT, NUM_POINTS):
    # Check if UR point has been defined (i.e if objects[i][1] == None)
        # If yes, insert piece into bottom left and return bin

    # If no, try to insert piece above and right UR
        # If posible, insert piece and update UR then return bin

    # If no, try to insert piece in top right and update UR then return bin

    # If no, return piece and bin and new bin flag
    fig, axs = plt.subplots(NUM_POINTS+1,NUM_POINTS+1)
    fig.set_figwidth(10)
    fig.set_figheight(10)