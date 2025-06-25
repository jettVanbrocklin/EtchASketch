import numpy as np


def findPath(x_coords, y_coords, start_x, start_y):
    stack = [(start_x, start_y)]
    pixels = set(zip(x_coords, y_coords))
    path = []
    visited = set()
    iterator = 0

    while stack:
        iterator = iterator + 1
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        path.append((x, y))

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:  # 4-connected
            nx, ny = x + dx, y + dy
            if (nx, ny) in pixels and (nx, ny) not in visited:
                stack.append((nx, ny))
    print("THIS IS THE ITERATOR: " + str(iterator))
    return path

        
