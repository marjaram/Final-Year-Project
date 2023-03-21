import random

# Basic Structure
# 1) Generate training set of of e.g. 100 shapes, testing set of 50 shapes
# 2) Selection heuristic function: first find way to sort shapes in decreasing area (trivial), then find way to check if shape fits (difficult)
    # First fit/ first fit decreasing: consider opened objects and put item into first one that fits
    # Next fit: Put piece in current open object, if not open new object and put piece there
    # Best fit: Put piece into opened object where it leaves the minimum wasted area
    # Worst fit: Opposite of above
    # Djang and Fitch: Take items in decreasing size, place objects until bin is at least 1/3 full. Initialise w, 

# 3) Placement heuristics, with representation of bin


# GENERATE RANDOM REGULAR POLYGON (AND PLOT ON MATPLOTLIB)

# Shape
class Shape:
    x = 0
    y = 0

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.num_sides = random.randint(3,12)
        self.edge_length = random.randint()
        # To add: rotation (random integer)

class Object:
    def __init__(self) -> None:
        pass


