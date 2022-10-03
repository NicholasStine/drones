# ALRIGHT LET'S DO THIS, leeeeeroooooooyy JEEEEENNKKIIIIIINNNNS!!!
# WITH THE JAZZIEST PLEASURE, I
# INTRODUCE, MY MAN, DUKE SILVER!!!
from physics import Position, Vector
import pygame

class Drone():
    def __init__(self, screen):
        # Screen (for drawing)
        self.screen = screen
        
        # Physics
        self.pos = Position(300, 20)
        self.vel = Vector(0)
        
        # Dimensions
        self.strut = (100, 10)

    def render(self, gravity):
        self.pos.applyVectors(self.vel, gravity)
        self.pos.moveStep()
        pygame.draw.rect(self.screen, (90, 2, 33), pygame.Rect(*self.drawStrut()))

    def drawStrut(self):
        w, h = self.strut
        half_height = h / 2
        half_width = w / 2
        return (self.pos.x - half_width, self.pos.y - half_height, w, h)

class Thruster():
    def __init__(self):
        pass