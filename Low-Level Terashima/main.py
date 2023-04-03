import numpy as np
import matplotlib.pyplot as plt
import sys
import generator
import placement
np.set_printoptions(threshold=sys.maxsize)

BIN_HEIGHT = 100
BIN_WIDTH = 100
NUM_RECTANGLES = 20 

items, label = generator.create_rectangles(BIN_WIDTH, BIN_HEIGHT, NUM_RECTANGLES)
object = np.zeros((BIN_HEIGHT, BIN_WIDTH))
objects = [(object, None)]
print(f'Allocating {len(items)} items into {BIN_WIDTH}x{BIN_HEIGHT} bins. Label: {label}')
# placement.bottom_left(item)
# Open empty bin
# Call generator to get rectangle set and 8-digit code
# While rectangle set not empty:
    # Select bin calling one of the following:
        # First Fit: Consider the opened objects in turn in a fixed order and place the item in the first one where it fits.
        # First Fit Decreasing (FFD). Sort pieces in decreasing order, and the largest one is placed according to FF.
        # First Fit Increasing (FFI). Sort pieces in increasing order, and the smallest one is placed according to FF.
        # Filler + FFD. This places as many pieces as possible within the open objects. If at least one piece has been placed, the algorithm stops. The FFD algorithm is applied, otherwise.
        # Next Fit (NF). Use the current object to place the next piece, otherwise open a new one
        # and place the piece there.
        # Next Fit Decreasing (NFD). Sort the pieces in decreasing order, and the largest one is
        # placed according to NF.
        # Best Fit (BF). This places the item in the opened object where it best fits, that is, in the
        # object that leaves minimum waste.
        # BestFitDecreasing(BFD).Sameasthepreviousone,butsortingthepiecesindecreasing
        # order.
        # Worst Fit (WF). It places the item in the opened object where it worst fits (that is, with
        # the largest available room).
        # Djang and Fitch (DJD). It places items in an object, taking items by decreasing size, until
        # the object is at least one-third full. Then, it initializes w, a variable indicating the allowed waste,
        # and looks for combinations of one, two, or three items producing a waste w. If any combination fails,
        # it increases w accordingly. We adapted this heuristic to consider the initial filling different to a third,
        # and the combinations for getting the allowed waste up to five items.
    # Call placement heuristic
    # If rectangle can be placed in bin: repeat
    # Else: open new bin and repeat
