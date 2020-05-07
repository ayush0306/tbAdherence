import scipy.stats as stats
import numpy as np
from scipy.stats import bernoulli
import matplotlib.pyplot as plt 

def myPlot(df,title,filepath):
	plt.plot(df)
	plt.title(title)
	plt.savefig(filepath+".png")
	plt.close()

n_rounds = 20
n_iters = 50000
p = 1.0
q = 0.6
r = 0.5
pc = p*q+(1-p)*r

alphas = []
betas = []

for i in range(n_rounds):
	print("round: ",i)
	alpha = 1
	beta = 1
	for j in range(n_iters):
		rnd = bernoulli.rvs(size=1,p=pc)[0]
		p_sample = stats.beta.rvs(alpha,beta)
		if(rnd == 0):
			beta += 1
		if(rnd == 1):
			p_ac = (2*p_sample)/(1+p_sample)
			rnd2 = bernoulli.rvs(size=1,p=p_ac)[0]
			if(rnd2 == 0):
				beta += 1
			else:
				alpha += 1
	alphas.append(alpha)
	betas.append(beta)
	print(float(alpha)/float(alpha + beta))

alphas = np.array(alphas,dtype=float)
betas = np.array(betas,dtype=float)
means = alphas/(alphas+betas)
print(means)
myPlot(means,"empirical_means","./sample3.png")