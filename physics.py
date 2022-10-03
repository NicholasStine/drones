# Positions, Vectors & Miscellaneous Mathematics, Oh My!
from math import sin, cos, pi

DIRECTIONS = {
    'UP': 3 * pi / 2,
    'DOWN': pi / 2,
    'LEFT': pi,
    'RIGHT': 0
}

class Position():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
    
    def applyVectors(self, *vectors):
        for vector in vectors:
            vector_x, vector_y = vector.getComponents()
            self.dx += vector_x
            self.dy += vector_y

    def moveStep(self):
        self.x += self.dx
        self.y += self.dy

class Vector():
    def __init__(self, initial_mag=0, initial_theta='DOWN'):
        if (initial_theta not in ['UP', 'DOWN', 'LEFT', 'RIGHT', None]):
            return Exception("INVALID GLOBAL DIRECTION")
        self.mag = initial_mag
        self.theta = DIRECTIONS[initial_theta]
    
    def getComponents(self):
        x = cos(self.theta) * self.mag # cah
        y = sin(self.theta) * self.mag # soh

        return x, y
        
        
    