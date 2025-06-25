import pathFinder
import numpy as np
import iterativePathFinder

# Define your 4x4 array using a list of lists
# Replace the values below with 1s and 0s as you like
test3 = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
]




# Convert it to a NumPy array
array = np.array(test3)
y_coords, x_coords = np.nonzero(array == 1)

print(pathFinder.findPath(x_coords, y_coords, x_coords[0], y_coords[0]))


