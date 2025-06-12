

class Node():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.visited = False

    def set_value(self, value):
        self.value = value
    
class StackFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    



class NodeArray():
    def __init__(self):
        self.width = 330
        self.height = 250
        self.grid = [[Node(x, y, 0) for x in range(self.width)] for y in range(self.height)] # each node knows it's coordinate
        

    def update_grid(self, img):
        for x,y in range(self.width), range(self.height):
            self.grid[x][y].set_value(img[x][y]) # sets the value with the corresponding image cluster values