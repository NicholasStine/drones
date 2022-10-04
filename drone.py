# ALRIGHT LET'S DO THIS, leeeeeroooooooyy JEEEEENNKKIIIIIINNNNS!!!
# WITH THE JAZZIEST PLEASURE, I
# INTRODUCE, MY MAN, DUKE SILVER!!!
from physics import Position, Vector, BodyState
import pygame
from numpy import array

DRONE_PATH = 'images/drone_medium.png'

# move this into your config or whatever
# initial positions

X = [[500,0,0],[250,0,0]]
theta = [0,0,0]

# simulation timestep, link this to your pygame step size



class Drone():
    def __init__(self, screen):
        # Drawerz and imgz
        self.screen = screen
        self.drone_img = pygame.image.load(DRONE_PATH).convert_alpha()

        """

                  -y
                   ^
                   |
                   |
                   |
       -x < ------ o ------ > +x
                   |
                   |
                   |
                   v
                  +y
        """

        # Physics
        self.body = BodyState(X, theta) # body state
        self.pos_x = self.body.X[0][0]  # reference position X
        self.pos_y = self.body.X[1][0]  # reference position Y
        self.mass = 3                 # mass
        self.inertia = 15             # moment of inertia
        self.accels = array([0,0,0])    # initial accelerations (thrust induced)
        self.leftPropPos = 50          # length from center of mass to left propeller
        self.rightPropPos = 50       # length from center of mass to right propeller

        # Dimensions
        self.strut = (100, 10)

    def Motormixing(self,leftThrust,rightThrust):
        # motor mixing algorithm

        self.accels[0] = 0# no thrust in the x direction, only in y
        self.accels[1] = (leftThrust + rightThrust) / self.mass # F = ma
        self.accels[2] = ((leftThrust * self.leftPropPos)/self.inertia) - ((rightThrust * self.rightPropPos)/self.inertia)


    def render(self, gravity):
        self.Motormixing(0,0)
        self.body.timeStep(self.accels,(1/60),gravity)
        self.pos_x = self.body.X[0][0]
        self.pos_y = self.body.X[1][0]
        draw_img = pygame.transform.rotate(self.drone_img,self.body.Theta[0])
        # pygame.draw.rect(self.screen, (90, 2, 33), pygame.Rect(*self.drawStrut()))
        self.screen.blit(draw_img, (self.pos_x - (draw_img.get_width() / 2), self.pos_y - (draw_img.get_height() / 2)))

    def drawStrut(self):
        w, h = self.strut
        half_height = h / 2
        half_width = w / 2
        return (self.pos_x - half_width, self.pos_y - half_height, w, h)

class Thruster():
    def __init__(self):
        pass
