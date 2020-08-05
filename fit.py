import numpy as np
import lmfit
from seir import generateData

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

initVec = [N-1, 1, 0, 0, 0, 0] #Begin with N-1 susceptible, 1 exposed, 0 asymp/miserable/recovered/dead

#Integrate the differential equations
sol = generateData(time, initVec, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho)
#Generate the true data
S, E, A, M, R, D = sol

def extractDead(time, initVec = initVec, N = N, beta1 = beta1, beta2 = beta2, tLock = tLock, gamma1 = gamma1, gamma2 = gamma2, 
				eta = eta, mu = mu, delta = delta, alpha = alpha, rho = rho):
	'''Get the number of dead from the given parameters'''
	return generateData(time, initVec, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho)[5]

#Fit the function to the true (synthetic) data
seirModel = lmfit.Model(extractDead)
params = lmfit.Parameters()

#Add vars that do vary
params.add('beta1', min = 3, max = 7)

#Add constant vars that don't vary
params.add('N', value = N, vary = False)
params.add('beta2', value = beta2, vary = False)
params.add('tLock', value = tLock, vary = False)
params.add('gamma1', value = gamma1, vary = False)
params.add('gamma2', value = gamma2, vary = False)
params.add('eta', value = eta, vary = False)
params.add('mu', value = mu, vary = False)
params.add('delta', value = delta, vary = False)
params.add('alpha', value = alpha, vary = False)
params.add('rho', value = rho, vary = False)

#Fit extractDead to our true dead D
result = seirModel.fit(D, params, method = 'least_squares', time = time)

#Output the best parameters
lmfit.report_fit(result)