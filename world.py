# Worldly class of worlds
from physics import Vector
from drone import Drone
import sys, pygame
pygame.init()

speed = [2, 2]
black = 0, 0, 0
scale_screen = 0.8

class World():
    def __init__(self, width=int(scale_screen * 1920), height=int(scale_screen * 1080)):
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.drone = Drone(self.screen)
        self.gravity = Vector(150, 'DOWN')
        self.pos = [500,500]

    def runWorld(self, frames=10000):
        for i in range(frames):
            self.renderStep()

    def renderStep(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        left, middle, right = pygame.mouse.get_pressed()

        if left: self.pos = pygame.mouse.get_pos()


        self.screen.fill(black)
        self.drone.render(self.gravity,self.pos)
        self.clock.tick(120) # FIXED FPS
        pygame.display.flip()