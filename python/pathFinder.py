import numpy as np

import sys
sys.setrecursionlimit(100000)

X_MAX = 330
Y_MAX = 250

def findPath(x_coords, y_coords, x, y):
    pixels = set(zip(x_coords, y_coords))
    path = []
    visited = set()

    def search(x, y, depth=0):
        print("Recursion depth:", depth)
        #Needs to go through the grid, starting at the point given, and recursively call itself, 
        # passing in neighboring pixels and the set of the current path

        if(x < 0 or x >= X_MAX or y < 0 or y >= Y_MAX):
            return False
        if (x,y) not in pixels: # base case
            return False
        path.append((x, y)) # add the current coordinate to the path

        first_visit = (x,y) not in visited
        if first_visit:
            visited.add((x, y))
        
        if visited == pixels: # All pixels in the cluster have been visited
            return True
        for dx, dy in [(-1,0), (1,0), (0,-1), (0, 1)]:
            if (x+dx, y+dy) in visited:
                continue
            if(search(x + dx, y + dy, depth=depth+1)):
                return True
        for dx, dy in [(-1,0), (1,0), (0,-1), (0, 1)]:
            if(search(x + dx, y + dy, depth = depth+1)):
                return True
        
        if first_visit:
            visited.remove((x,y))
        path.pop()
        return False

    search(x, y)
    return path