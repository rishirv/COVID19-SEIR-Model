from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def SEIR(currentVec, time, N, betaLockdown, gamma1, gamma2, eta, mu, delta, alpha, rho):
	'''
	Calculates the Riemann sum by return the change in each variable at the current time

	N = The total population
	betaLockdown(time) = Average number of people an asymptotic person infects every day as a function of the current time
	D = Number of days it takes for an asymptomatic person to recover (1/gamma1)
	gamma1 = Proportion of asymptomatic people who recover each day (1/D)
	gamma2 = Proportion of miserable people who recover each day
	eta = Proportion of miserable people who become asymptotic each day
	delta = Expected number of days of incubation
	mu = Proportion of asymptotic people that become miserable
	alpha = Fatality rate = Proportion of miserable people that die 
	rho = Proportion of miserable people who die each day (one divided by the number of days it takes for an infected person to die)
	R0 = Total number of people an asymptomatic person will infect (beta/gamma1) 

	S = Susceptible --> No prior interaction with virus (Can become exposed)
	E = Exposed --> Virus is incubating --> Can not infect others (Will become asymptomatic)
	A = Asymptomatic --> No symptoms --> Can infect others (Can become recovered or miserable)
	M = Miserable --> Hospitalized --> Can not infect others (Can become recovered or dead)
	R = Recoved --> Immunity
	D = Dead
	'''
	S, E, A, M, R, D = currentVec

	beta = betaLockdown(time)

	dS = -beta*A*S/(N - D)
	dE = beta*A*S/(N - D) - delta*E
	dA = delta*E - gamma1*(1-mu)*A - mu*eta*A
	dM = mu*eta*A - gamma2*(1-alpha)*M - rho*alpha*M
	dR = gamma2*(1-alpha)*M + gamma1*(1-mu)*A
	dD = rho*alpha*M

	return [dS, dE, dA, dM, dR, dD]

time = np.linspace(0, 49, 150) #Equally spaced time values in the range

def getBeta(beta1, beta2, tLock):
	'''	
	Returns a variable beta as a function of time
	beta1 = Average number of people an asymptotic person infects every day before lockdown
	beta2 = Average number of people an asymptotic person infects every day before lockdown
	tLock = Day that lockdown is first implemented
	'''
	def betaLockdown(time):
		if(time <= tLock):
			return beta1
		else:
			return beta2
	return betaLockdown

#Initialize the parameters
N = 10000
beta1 = 1
beta2 = .3
gamma1 = gamma2 = eta = 1/6
mu = 1/2
delta = 3
alpha = 0.05
rho = 1/6
tLock = 15
betaLockdown = getBeta(beta1, beta2, tLock)

initVec = [N-1, 1, 0, 0, 0, 0] #Begin with N-1 susceptible, 1 exposed, 0 asymp/miserable, and no recovered or dead

#Integrate the differential equations
sol = odeint(SEIR, initVec, time, args = (N, betaLockdown, gamma1, gamma2, eta, mu, delta, alpha, rho))
S, E, A, M, R, D = sol.T

#Plot the results
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
ax.axvline(ls = '--', x = tLock) #Plot a vertical line for when the lockdown occurs
Splt, = ax.plot(time, S, 'b', label = 'Susceptible')
Eplt, = ax.plot(time, E, 'c', label = 'Exposed')
Aplt, = ax.plot(time, A, 'r', label = 'Asymptotic')
Mplt, = ax.plot(time, M, 'y', label = 'Miserable')
Rplt, = ax.plot(time, R, 'g', label = 'Recovered')
Dplt, = ax.plot(time, D, 'k', label = 'Dead')
Tplt, = ax.plot(time, S + E + A + M + R + D, '--', label = 'Total') #Mark total with a dashed line
ax.set(xlabel = 'Time (days)', ylabel = "People", title = 'Disease Spread')
plt.legend()

#Add sliders for input parameters
sliderColor = 'green'

betaAx = plt.axes([0.25, 0.15, 0.65, 0.03])
betaSlider = Slider(betaAx, 'Beta1 (expected number of people infected per day before lockdown)', 1, 10, valinit = 4, valstep = 1, color = sliderColor)

muAx = plt.axes([0.25, 0.10, 0.65, 0.03])
muSlider = Slider(muAx, 'proportion of people getting miserable', 0, 1, valinit = 1/2, valstep = 1/10, color = sliderColor)

DAx = plt.axes([0.25, 0.20, 0.65, 0.03])
DSlider = Slider(DAx, 'Days to transition (E->A orA->M) (1/Gamma) (1/Gamma)', 1, 15, valinit = 10, valstep = 1, color = sliderColor)

deltaAx = plt.axes([0.25, 0.05, 0.65, 0.03])
deltaSlider = Slider(deltaAx, 'Days of incubation (delta)', 1, 15, valinit = 3, valstep = 1, color = sliderColor)

def reset(event):
	'''Reset all of the sliders'''
	betaSlider.reset()
	DSlider.reset()
	deltaSlider.reset()
	muSlider.reset()

resetAx = fig.add_axes([0.45, 0.025, 0.1, 0.04])
resetButton = Button(resetAx, 'Reset', color = 'gray')
resetButton.on_clicked(reset)

def model(event):
	'''Update the parameters and plots'''
	beta1 = betaSlider.val
	gamma1 = gamma2 = eta = 1/DSlider.val
	delta = deltaSlider.val
	mu = muSlider.val
	betaLockdown = getBeta(beta1, beta2, tLock)

	#Differentiate the equations again
	sol = odeint(SEIR, initVec, time, args = (N, betaLockdown, gamma1, gamma2, eta, mu, delta, alpha, rho))
	S, E, A, M, R, D = sol.T

	#Change the y-data on each of the plots
	Splt.set_ydata(S)
	Eplt.set_ydata(E)
	Aplt.set_ydata(A)
	Mplt.set_ydata(M)
	Rplt.set_ydata(R)
	Dplt.set_ydata(D)
	Tplt.set_ydata(S + E + A + M + R + D)

	#Redraw the plots
	fig.canvas.draw_idle()

setAx = fig.add_axes([0.6, 0.025, 0.1, 0.04])
setButton = Button(setAx, 'Model', color = 'gray')
setButton.on_clicked(model)

plt.show()
