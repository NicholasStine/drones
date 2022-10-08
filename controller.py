from math import sin, cos, pi,

import numpy as np

class LQR_controller_attitude():					# 1D linear controller. create, and call with 'feedback()'

	def __init__(self,K,control_variable,set_point,dt):

		K = np.array([0,0,0,0],[0,0,0,0])           # this will need to be calculated, I pulled it out of my ass cause I can. 

		self.control_variable = control_variable 	# controlled variable (X,X_dot,X_ddot)
		self.set_point = set_point  				# setpoint (R, R_dot, R_ddot)
		self.Euler_history = control_variable		# variable at t[k-1], assume theta_dot = 0 at t = 0 (still works if this is false)
		self.K = K									# gain matrix (steering/control law)
		self.E = np.array([0,0,0,0])				# error to minimize
		self.timestep = dt
		self.U = np.zeros(2)

	def error_calc(self):
		Error = np.array([0,0,0])

		for i in range (0:2):
			Error[i] = self.set_point[i] - self.control_variable[i]
		return Error


	def integrator(self,control_variable):

		# -1 order error
		self.Euler_history = self.control_variable
		self.control_variable = control_variable
		self.E[0] = self.E[0] + (self.timestep/2) * ((self.set_point[0] - self.Euler_history) + (self.set_point_[0] - self.control_variable))

		self.E[1], self.E[2], self.E[3] = error_calc()

	def feedback(self, control_variable):
		# U = -K * E 
		U = np.array([0,0])

		integrator(control_variable)

		for i in range(0,3):
			U[0] += -self.K[0][i]*self.E[i]
			U[1] += -self.K[1][i]*self.E[i]

		leftMotorspeed = U[0]
		rightMotorspeed = U[1]

		return leftMotorspeed, rightMotorspeed





class magicController():
	def __init__(self):


