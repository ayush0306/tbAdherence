import random
import numpy as np
random.seed(10)

n = 20
mu,sigma = 50,20
s = np.random.normal(mu, sigma, n)
print(n)
for i in range(n):
	# prob_adhering = float(random.randint(10,90))/100.0
	prob_adhering = int(s[i])/float(100)
	print(prob_adhering)