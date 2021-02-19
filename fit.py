import numpy as np
import lmfit
from seir import generateData
import matplotlib.pyplot as plt

#Data from France from Our World in Data starting from 02/26/2020
trueDead = np.cumsum([0,1,0,0,0,0,1,1,0,3,2,1,9,11,3,15,13,18,12,36,21,27,69,128,78,112,112,186,240,231,365,299,319,292,418,499,509,471,2004,1053,518,833,1417,541,1341,987,635,561,574,762,1438,753,761,642,395,547,531,544,516,389,369,242,437,367,427,289,218,166,135,306,330,278,178,243,80,70,263,348,83,351,130,88,68,186,125,110,83,74,43,35,65,98,66,66,52,57,31,31,107,81,44,46,31,13,54,87,23,27,28,24,9,29,111,28,28,14,16,7,23,57,11,21,26,0,0,35,30,18,14,18,0,0,27,13,32,14,25,0])

time = np.linspace(0, len(trueDead)-1, len(trueDead)) #Equally spaced time values in the range

#Initialize the parameters using the best known estimates currently available
N = 67000000 #Country dependent
beta1 = 5 #Country dependent
beta2 = 1 #Country dependent
gamma1 = 1/3
gamma2 = 1/6.5
eta = 1/12
mu = 0.05
delta = 1/9
alpha = 0.3
rho = 1/7.5
tLock = 30 #Country dependent

initVec = [N-1, 1, 0, 0, 0, 0] #Begin with N-1 susceptible, 1 exposed, 0 asymp/miserable/recovered/dead

#Generate the true (synthetic) data we want to fit our curves to
#If using real-world data, we don't need this step
# sol = generateData(time, initVec, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho)
# S, E, A, M, R, D = sol

#This is the function we want to model - it returns only the dead curve as a function of time
def extractDead(time, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho):
	'''Get the number of dead from the given parameters'''
	return generateData(time, initVec, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho)[5]

#Generate a model for the function we want to fit
seirModel = lmfit.Model(extractDead)
params = lmfit.Parameters()

#Fit the function to the true (synthetic) data
#For each variable, we need to either give it a hint about a minimum and maximum value so it has a range to compute over
# or we need to fix its value and set vary = False

#Add vars that do vary
params.add('beta1', min = 1, max = 6)
params.add('beta2', min = 0.05, max = 2)
params.add('tLock', min = 25, max = 35)
# params.add('gamma1', min = 1/4, max = 1/2)
# params.add('gamma2', min = 1/8, max = 1/4)
# params.add('eta', min = 1/8, max = 1/4)
# params.add('mu', min = 1/4, max = 3/4)
# params.add('delta', min = 0, max = 1)
# params.add('alpha', min = 0, max = 0.1)
# params.add('rho', min = 1/8, max = 1/4)

#Add constant vars that don't vary
params.add('N', value = N, vary = False)
# params.add('beta1', value = beta1, vary = False)
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
result = seirModel.fit(trueDead, params, method = 'least_squares', time = time)

#Output the best parameters
# lmfit.report_fit(result.params, show_correl = False)

# print('-------------------------------')

#Output the best parameters
print('Parameter     Value      Stderr      Vary')
for name, param in result.params.items():
    print('{:7s} {:11.5f} {:11.5f} {:>9s}'.format(name, param.value, (param.stderr if param.stderr else 0), str(param.vary)))

plt.xlabel('Time (days)') 
plt.ylabel("Number of Deaths")
plt.title('Comparing Predicted and Actual Deaths in France')
plt.plot(time, trueDead, label = "France Deaths")
plt.plot(time, result.eval(), label = "Model Predicted Deaths")
plt.axvline(ls = '--', x = result.params['tLock'].value) #Plot a vertical line for when the lockdown occurs
plt.legend()
plt.show()
