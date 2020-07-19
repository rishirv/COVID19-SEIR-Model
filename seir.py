from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def SEIR(currentVec, time, N, beta, gamma):
	'''
	N = The total population
	beta = Average number of people an infected person infects every day
	gamma = Proportion of infected people who recover each day (1/D)
	D = Number of days it takes for an infected person to recover (1/gamma)
	R0 = Total number of people an infected person will infect (beta/gamma)
	'''
	S, I, R = currentVec

	dS = -beta*I*S/N
	dI = beta*I*S/N - gamma*I
	dR = gamma*I

	return [dS, dI, dR]

time = np.linspace(0, 49, 50) #Equally spaced time values in the range

#Initialize the parameters
N = 1000
beta = 1
gamma = 1/5
initVec = [N-1, 1, 0] #Begin with N-1 susceptible, 1 infected, and no recovered

#Integrate the differential equations
sol = odeint(SEIR, initVec, time, args = (N, beta, gamma))
S, I, R = sol.T

#Plot the results
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
Splt, = ax.plot(time, S, 'b', label = 'Susceptible')
Iplt, = ax.plot(time, I, 'r', label = 'Infected')
Rplt, = ax.plot(time, R, 'g', label = 'Recovered')
Tplt, = ax.plot(time, S+I+R, '--', label = 'Total') #Mark total with a dashed line
ax.set(xlabel = 'Time (days)', ylabel = "People", title = 'Disease Spread')
plt.legend()

#Add sliders for input parameters
sliderColor = 'green'
betaAx = plt.axes([0.25, 0.1, 0.65, 0.03])
betaSlider = Slider(betaAx, 'Beta', 1, 10, valinit = 3, valstep = 1, color = sliderColor)

DAx = plt.axes([0.25, 0.15, 0.65, 0.03])
DSlider = Slider(DAx, 'Days to recover (1/Gamma)', 1, 15, valinit = 5, valstep = 1, color = sliderColor)

def reset(event):
	'''Reset all of the sliders'''
	betaSlider.reset()
	DSlider.reset()
resetAx = fig.add_axes([0.45, 0.025, 0.1, 0.04])
resetButton = Button(resetAx, 'Reset', color = 'gray')
resetButton.on_clicked(reset)

def model(event):
	'''Update the parameters and plots'''
	beta = betaSlider.val
	gamma = 1/DSlider.val

	#Differentiate the equations again
	sol = odeint(SEIR, initVec, time, args = (N, beta, gamma))
	S, I, R = sol.T

	#Change the y-data on each of the plots
	Splt.set_ydata(S)
	Iplt.set_ydata(I)
	Rplt.set_ydata(R)
	Tplt.set_ydata(S + I + R)

	#Redraw the plots
	fig.canvas.draw_idle()
setAx = fig.add_axes([0.6, 0.025, 0.1, 0.04])
setButton = Button(setAx, 'Model', color = 'gray')
setButton.on_clicked(model)

plt.show()