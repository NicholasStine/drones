# Positions, Vectors & Miscellaneous Mathematics, Oh My!
from math import sin, cos, pi
import numpy as np

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

class BodyState(): # integrate EOM for a 3 DOF rigid body in free space
    def __init__(self, X, Theta):
        # positional state vector
        self.X = np.array([[0,0,0],[0,0,0]]) # [vector][state
        self.X = X

        # angular state vector 
        self.Theta = np.array([0,0,0])
        self.Theta = Theta                
 
    def timeStep(self,accels,dt,gravity): # calculate accelerations externally
        gravity_x, gravity_y = gravity.getComponents()
        self.X[0][2] = accels[0]*cos(self.Theta[0]) - accels[1]*sin(self.Theta[0]) + gravity_x# (2D transform)
        self.X[0][1] = self.X[0][1] + (self.X[0][2] * dt)   # integrate velocity x
        self.X[0][0] = self.X[0][0] + (self.X[0][1] * dt)   # integrate position x

        self.X[1][2] = accels[1]*cos(self.Theta[0]) + accels[0]*sin(self.Theta[0]) + gravity_y
        self.X[1][1] = self.X[1][1] + (self.X[1][2] * dt)   # integrate velocity y
        self.X[1][0] = self.X[1][0] + (self.X[1][1] * dt)   # integrate position y

        self.Theta[2] = accels[2]
        self.Theta[1] = self.Theta[1] + self.Theta[2] * dt
        self.Theta[0] = self.Theta[0] + self.Theta[1] * dt

        

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
        
        
    