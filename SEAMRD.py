from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def SEIR(currentVec, time, N, beta, gamma1, gamma2, miu, delta, alpha, rho):
	'''
	N = The total population
	beta = Average number of people an asymptotic person infects every day
	gamma1 = Proportion of asymptomatic people who recover each day (1/D)
	gamma2 = Proportion of miserable people who recover each day
	delta = Expected number of days of incubation
	miu = proportion of asymptotic people that become miserable( = 1-gamma1)
	alpha = Fatality rate = Proportion of miserable people that die 
	rho = Proportion of miserable people who die each day (one divided by the number of days it takes for an infected person to die)
	D = Number of days it takes for an asymptomatic person to recover (1/gamma1)
	R0 = Total number of people an asymptomatic person will infect (beta/gamma) 
	IN THIS MODEL WE ASSUME MISERABLE PPL DONT INFECT ANYONE
	'''
	S, E, A, M, R, D = currentVec

	dS = -beta*E*S/N
	dE = beta*E*S/N - delta*E
	dA = delta*E -gamma1*A-miu*A
	dM = miu*A-gamma2*(1-alpha)*M - rho*alpha*M
	dR = (gamma2)*(1-alpha)*M+gamma1*A
	dD = rho*alpha*M

	return [dS, dE, dA, dM, dR, dD]

time = np.linspace(0, 49, 100) #Equally spaced time values in the range

#Initialize the parameters
N = 10000
beta = 4
gamma1 = gamma2= 1/12
miu = 1/2
delta = 3
alpha = 0.05
rho = 1/6

initVec = [N-100, 100, 0, 0, 0, 0] #Begin with N-1 susceptible, 1 exposed, 0 asymp/miserable, and no recovered or dead

#Integrate the differential equations
sol = odeint(SEIR, initVec, time, args = (N, beta, gamma1, gamma2, miu, delta, alpha, rho))
S, E, A, M, R, D = sol.T

#Plot the results
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
Splt, = ax.plot(time, S, 'b', label = 'Susceptible')
Eplt, = ax.plot(time, E, 'c', label = 'Exposed')
Aplt, = ax.plot(time, A, 'r', label = 'Asymptotic')
Mplt, = ax.plot(time, M, 'o', label = 'Miserable')
Rplt, = ax.plot(time, R, 'g', label = 'Recovered')
Dplt, = ax.plot(time, D, 'k', label = 'Dead')
Tplt, = ax.plot(time, S+E+A+M+R+D, '--', label = 'Total') #Mark total with a dashed line
ax.set(xlabel = 'Time (days)', ylabel = "People", title = 'Disease Spread')
plt.legend()

#Add sliders for input parameters
sliderColor = 'green'
betaAx = plt.axes([0.25, 0.15, 0.65, 0.03])
betaSlider = Slider(betaAx, 'Beta (expected number of people infected per day)', 1, 10, valinit = 4, valstep = 1, color = sliderColor)
miuAx = plt.axes([0.25, 0.10, 0.65, 0.03])
miuSlider = Slider(miuAx, 'proportion of people getting miserable', 0, 1, valinit = 1/2, valstep = 1/10, color = sliderColor)
DAx = plt.axes([0.25, 0.20, 0.65, 0.03])
DSlider = Slider(DAx, 'Days to transition (E->A orA->M) (1/Gamma) (1/Gamma)', 1, 15, valinit = 10, valstep = 1, color = sliderColor)
 # delta slider 
deltaAx = plt.axes([0.25, 0.05, 0.65, 0.03])
deltaSlider = Slider(deltaAx, 'Days of incubation (delta)', 1, 15, valinit = 3, valstep = 1, color = sliderColor)

def reset(event):
	'''Reset all of the sliders'''
	betaSlider.reset()
	DSlider.reset()
	deltaSlider.reset()
resetAx = fig.add_axes([0.45, 0.025, 0.1, 0.04])
resetButton = Button(resetAx, 'Reset', color = 'gray')
resetButton.on_clicked(reset)

def model(event):
	'''Update the parameters and plots'''
	beta = betaSlider.val
	gamma1 = gamma2 = 1/DSlider.val
	delta = deltaSlider.val
	miu = miuSlider.val

	#Differentiate the equations again
	sol = odeint(SEIR, initVec, time, args = (N, beta, gamma1, gamma2, miu, delta, alpha, rho))
	S, E, A, M, R, D = sol.T

	#Change the y-data on each of the plots
	Splt.set_ydata(S)
	Eplt.set_ydata(E)
	Aplt.set_ydata(A)
	Mplt.set_ydata(M)
	Rplt.set_ydata(R)
	Dplt.set_ydata(D)
	Tplt.set_ydata(S + E + A + M + R)

	#Redraw the plots
	fig.canvas.draw_idle()
setAx = fig.add_axes([0.6, 0.025, 0.1, 0.04])
setButton = Button(setAx, 'Model', color = 'gray')
setButton.on_clicked(model)

plt.show()

