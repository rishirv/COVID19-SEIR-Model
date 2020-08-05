import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
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

initVec = [N-1, 1, 0, 0, 0, 0] #Begin with N-1 susceptible, 1 exposed, 0 asymp/miserable, and no recovered or dead

#Integrate the differential equations
sol = generateData(time, initVec, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho)
S, E, A, M, R, D = sol

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

	#Differentiate the equations again
	sol = generateData(time, initVec, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho)
	S, E, A, M, R, D = sol

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
