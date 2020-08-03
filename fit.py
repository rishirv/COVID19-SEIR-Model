import numpy as np
import lmfit
from seir import generateData

def extractDead(initVec, N, gamma1, gamma2, eta, mu, delta, alpha, rho):
	'''Set parameters for variables that won't vary'''
	def setParams(time, beta1, beta2, tLock):
		'''Fit variables that do vary'''
		return generateData(initVec, time, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho).T[5]
	return setParams


time = np.linspace(0, 49, 150) #Equally spaced time values in the range

#Initialize the parameters
N = 10000
beta1 = 5
beta2 = 1
gamma1 = gamma2 = eta = 1/6
mu = 1/2
delta = 1/9
alpha = 0.05
rho = 1/6
tLock = 15

initVec = [N-1, 1, 0, 0, 0, 0] #Begin with N-1 susceptible, 1 exposed, 0 asymp/miserable, and no recovered or dead

#Integrate the differential equations
sol = generateData(initVec, time, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho)
S, E, A, M, R, D = sol

#Fit the curves
seirModel = lmfit.Model(extractDead(initVec, N, gamma1, gamma2, eta, mu, delta, alpha, rho))
params = seirModel.make_params()
result = seirModel.fit(D, params, method = 'least_squares', time = time, beta1 = 7, beta2 = 3, tLock = 10)

#Output the best parameters
print(result.best_values)