from math import sin, cos, pi

import numpy as np


# controller for attitude

class LQR_controller_attitude():					# 1D linear controller. create, and call with 'feedback()'

	def __init__(self,control_variable,set_point,dt):

		K = np.array([[0,7.5,2.5,0],[0,-7.5,-2.5,0]])           # this will need to be calculated, I pulled it out of my ass cause I can. 

		self.INTEGRATOR_CLAMP = pi/6

		self.control_variable = control_variable 	# controlled variable (X,X_dot,X_ddot)
		self.set_point = set_point  				# setpoint (R, R_dot, R_ddot)
		self.Euler_history = control_variable		# variable at t[k-1], assume theta_dot = 0 at t = 0 (still works if this is false)
		self.K = K									# gain matrix (steering/control law)
		self.E = np.array([0,0,0,0])				# error to minimize
		self.timestep = dt
		self.U = np.zeros(2)

	def error_calc(self):
		Error = np.array([0,0,0])

		for i in range(0,2):
			Error[i] = self.set_point[i] - self.control_variable[i]
		return Error


	def integrator(self,control_variable):

		# -1 order error
		self.Euler_history = self.control_variable[0]
		self.control_variable = control_variable

		# clamp integrator if error is extreme
		if ((self.E[1] < self.INTEGRATOR_CLAMP) and (self.E[1] > -self.INTEGRATOR_CLAMP)):
			self.E[0] = self.E[0] + (self.timestep/2) * ((self.set_point[0] - self.Euler_history) + (self.set_point[0] - self.control_variable[0]))

		self.E[1], self.E[2], self.E[3] = self.error_calc()


	def feedback(self, control_variable):
		# U = -K * E 
		U = np.array([0,0])

		self.integrator(control_variable)

		for i in range(0,3):
			U[0] += -self.K[0][i]*self.E[i]
			U[1] += -self.K[1][i]*self.E[i]


	# scale motor outputs, eliminate dumb motor signals. assume motor speed range 0-100

		leftMotorspeed = U[0]
		rightMotorspeed = U[1]
		if (U[0] <= 0):
			leftMotorspeed = 0
		
		if (U[0] >= 100):
			leftMotorspeed = 100

		if(U[1] <= 0):
			rightMotorspeed = 0
	
		if (U[1] >= 100):
			rightMotorspeed = 100


		return int(leftMotorspeed), int(rightMotorspeed)

# controller for altitude, only use when drone in small angle (< 30 deg, <15 deg for best results)

class PID_controller_altitude():

	def __init__(self, X, altitude_set,dt,kP,kI,kD):

		self.altitude_set = altitude_set	# desired altitude
		self.timestep = dt 					# simulation timestep
		self.X = X							# body state of drone
		self.altitude = self.X[1][0]		# just the altitude
		self.integrated_altitude = 0 		# integrator term
		self.vert_speed = 0 				# just the vertical speed
		self.thrust_ret = 0 				# return variable for total thrust

		# PID gains
		self.kP = kP
		self.kI = kI
		self.kD = kD

	def PID(self,X,altitude_set):



		# book keeping
		self.altitude_set = altitude_set
		self.X = X
		altitude_last = self.altitude

		# 0 order alt
		self.altitude = self.X[1][0]

		# 1st order alt
		self.vert_speed = self.X[1][1]

		# -1st order alt /w/ clamping
		if(abs(self.integrated_altitude + (self.timestep/2) * ((self.altitude_set - altitude_last) + (self.altitude_set - self.altitude))) < 10):
			self.integrated_altitude = self.integrated_altitude + (self.timestep/2) * ((self.altitude_set - altitude_last) + (self.altitude_set - self.altitude))
		print(self.integrated_altitude)


		self.thrust_ret = (self.kP * (self.altitude_set - self.altitude)) + \
					 (self.kD * self.vert_speed) + \
					 (self.kI * self.integrated_altitude)

		

		if(self.thrust_ret > 100): self.thrust_ret = 100
		if(self.thrust_ret  < 0): self.thrust_ret = 0
		return int(self.thrust_ret)


# controller for position


