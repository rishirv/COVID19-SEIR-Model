from scipy.integrate import odeint

def SEIR(currentVec, time, N, betaLockdown, gamma1, gamma2, eta, mu, delta, alpha, rho):
	'''
	Calculates the Riemann sum by return the change in each variable at the current time

	N = The total population
	betaLockdown(time) = Average number of people an asymptotic person infects every day as a function of the current time
	D = Number of days it takes for an asymptomatic person to recover (1/gamma1)
	gamma1 = Proportion of asymptomatic people who recover each day (1/D)
	gamma2 = Proportion of miserable people who recover each day
	eta = Proportion of asymptotic people that become miserable each day
	delta = Proportion of exposed people that become asymptotic each day
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

def getBeta(beta1, beta2, tLock):
	'''	
	Returns a variable beta as a function of time

	beta1 = Average number of people an asymptotic person infects every day before lockdown
	beta2 = Average number of people an asymptotic person infects every day after lockdown
	tLock = Day that lockdown is first implemented
	'''
	def betaLockdown(time):
		if(time <= tLock):
			return beta1
		else:
			return beta2
	return betaLockdown

def generateData(time, initVec, N, beta1, beta2, tLock, gamma1, gamma2, eta, mu, delta, alpha, rho):
	'''Given all of the parameters, generates the data SEAMRD'''
	betaLockdown = getBeta(beta1, beta2, tLock) #Get the lockdown function
	#Integrate the differential equations and return the data
	return odeint(SEIR, initVec, time, args = (N, betaLockdown, gamma1, gamma2, eta, mu, delta, alpha, rho)).T
