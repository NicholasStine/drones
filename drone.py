# ALRIGHT LET'S DO THIS, leeeeeroooooooyy JEEEEENNKKIIIIIINNNNS!!!
# WITH THE JAZZIEST PLEASURE, I
# INTRODUCE, MY MAN, DUKE SILVER!!!
from physics import Position, Vector, BodyState
from controller import LQR_controller_attitude, PID_controller_altitude
import pygame
from numpy import array

DRONE_PATH = 'images/drone_medium.png'

# move this into your config or whatever
# initial positions

X = [[1200,0,0],[750,0,0]]
theta = [30,0,0]
theta_set = [0,0,0]
altitude_set = 150

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
       -x < ------ o ------ > +x [0]
                   |
                   |
                   |
                   v
                  +y
                  [1]

                  So the transform is fixed. 

                  In vector notation, the indexes of X are 0 = x, 1 = y

                    accels[0,1,2] = accels[ 0 = acceleration x (body coordinates), 
                                            1 = acceleration y (body coordinates),
                                            2 = angular acceleration (body) 
                                          ]

                    body.X[i][j]  = vector i, derivative j. SO for body[0][1], 
                    this would be the first derivative of the 0 direction. 
                    In this case, 0 = X, so X[0][1] would be the velocity
                    in the x direction, whereas X[1][2] would be the acceleration 
                    in the y direction. 


        """

        # Physics
        self.body = BodyState(X, theta) # body state
        self.pos_x = self.body.X[0][0]  # reference position X
        self.pos_y = self.body.X[1][0]  # reference position Y
        self.mass = .5                 # mass
        self.inertia = 5             # moment of inertia
        self.accels = array([0,0,0])    # initial accelerations (thrust induced)
        self.leftPropPos = 15          # length from center of mass to left propeller
        self.rightPropPos = 15       # length from center of mass to right propeller

        # attach attitude controller
        self.controller = LQR_controller_attitude(self.body.Theta,theta_set,(1/120)) 

        # attach altitude autopilot
        self.auto_alt = PID_controller_altitude(self.body.X,altitude_set,(1/120),-3,-5,4)

        # Dimensions
        self.strut = (100, 10)

    def Motormixing(self,leftThrust,rightThrust):
        # motor mixing algorithm
        leftThrust = leftThrust * 1500
        rightThrust = rightThrust * 1500

        self.accels[0] = 0# no thrust in the x direction, only in y
        self.accels[1] = -(leftThrust + rightThrust) / self.mass # F = ma
        self.accels[2] = -((leftThrust * self.leftPropPos)/self.inertia) + ((rightThrust * self.rightPropPos)/self.inertia)


    def render(self, gravity):

        """ LOOK AT ME!!!! How to use this function? self.Motormixing(leftSpeed,rightSpeed) 
        = mix the thrust from a left an right propeller spinning at speeds leftSpeed and rightSpeed
        So replace the dummy constants with your controller output!

        Do you want me to write a controller???
        This 2D case is very easy as there is no navigation problem. 

        """
        lms, rms = self.controller.feedback(self.body.Theta)            # get left/right offset

        vert_thrust = self.auto_alt.PID(self.body.X,altitude_set)       # get combined thrust term
        lms += vert_thrust
        rms += vert_thrust
        if(lms < 0): lms = 0
        if(lms > 200): lms = 200
        if(rms < 0): rms = 0
        if(rms > 200): rms = 200
        print(lms,rms,int(self.pos_y),int(self.body.X[1][1]))
        self.Motormixing(lms,rms) 


        self.body.timeStep(self.accels,(1/120),gravity)
        self.pos_x = self.body.X[0][0]
        self.pos_y = self.body.X[1][0]
        draw_img = pygame.transform.rotate(self.drone_img,self.body.Theta[0])
        self.screen.blit(draw_img, (self.pos_x - (draw_img.get_width() / 2), self.pos_y - (draw_img.get_height() / 2)))

    def drawStrut(self):
        w, h = self.strut
        half_height = h / 2
        half_width = w / 2
        return (self.pos_x - half_width, self.pos_y - half_height, w, h)

class Thruster():
    def __init__(self):
        pass
