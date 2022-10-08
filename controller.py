from math import sin, cos, pi

import numpy as np

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

		if (U[0] >= 0):
			leftMotorspeed = U[0]
		else:
			leftMotorspeed = 0
		if (U[0] >= 100):
			leftMotorspeed = 100

		if(U[1] >= 0):
			rightMotorspeed = U[1]
		else:
			rightMotorspeed = 0
		if (U[1] >= 100):
			rightMotorspeed = 100


		return leftMotorspeed, rightMotorspeed

