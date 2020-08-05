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

#Generate the true (synthetic) data we want to fit our curves to
#If using real-world data, we don't need this step
sol = generateData(time, initVec, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho)
S, E, A, M, R, D = sol

#This is the function we want to model - it returns only the dead curve as a function of time
def extractDead(time, initVec = initVec, N = N, beta1 = beta1, beta2 = beta2, tLock = tLock, gamma1 = gamma1, gamma2 = gamma2, 
				eta = eta, mu = mu, delta = delta, alpha = alpha, rho = rho):
	'''Get the number of dead from the given parameters'''
	return generateData(time, initVec, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho)[5]

#Generate a model for the function we want to fit
seirModel = lmfit.Model(extractDead)
params = lmfit.Parameters()

#Fit the function to the true (synthetic) data
#For each variable, we need to either give it a hint about a minimum and maximum value so it has a range to compute over
# or we need to fix its value and set vary = False

#Add vars that do vary
params.add('beta1', min = 3, max = 7)
params.add('beta2', min = 0, max = 2)
params.add('tLock', min = 10, max = 20)

#Add constant vars that don't vary
params.add('N', value = N, vary = False)
# params.add('beta1', min = 3, max = 7)
# params.add('beta2', value = beta2, vary = False)
# params.add('tLock', value = tLock, vary = False)
params.add('gamma1', value = gamma1, vary = False)
params.add('gamma2', value = gamma2, vary = False)
params.add('eta', value = eta, vary = False)
params.add('mu', value = mu, vary = False)
params.add('delta', value = delta, vary = False)
params.add('alpha', value = alpha, vary = False)
params.add('rho', value = rho, vary = False)

#Fit extractDead to our true dead D using our parameters and the independent variable time
result = seirModel.fit(D, params, method = 'least_squares', time = time)

#Output the best parameters
# lmfit.report_fit(result.params, show_correl = False)

# print('-------------------------------')

#Output the best parameters
print('Parameter     Value      Stderr      Vary')
for name, param in result.params.items():
    print('{:7s} {:11.5f} {:11.5f} {:>9s}'.format(name, param.value, param.stderr, str(param.vary)))
