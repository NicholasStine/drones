# Worldly class of worlds
from physics import Vector
from drone import Drone
import sys, pygame
pygame.init()

speed = [2, 2]
black = 0, 0, 0

class World():
    def __init__(self, width=1920, height=1080):
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.drone = Drone(self.screen)
        self.gravity = Vector(100, 'DOWN')

    def runWorld(self, frames=10000):
        for i in range(frames):
            self.renderStep()

    def renderStep(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        self.screen.fill(black)
        self.drone.render(self.gravity)
        self.clock.tick(120) # FIXED FPS
        pygame.display.flip()