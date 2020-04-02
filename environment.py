import numpy as np
from scipy.stats import bernoulli

class Patient():
	def __init__(self,index,p_adhere):
		self.index = index
		self.p_adhere = p_adhere

class Environment():
	def __init__(self,n,k):
		self.n = n
		self.k = k
		self.T = 0
		self.patients = []
		self.optimal_reward = 0
		self.mu = 50
		self.sigma = 25

	def reset(self):
		s = np.random.normal(self.mu, self.sigma, self.n)
		for i in range(self.n):
			s[i] = int(s[i])/float(100)
			s[i] = min(s[i],0.99)
			s[i] = max(0.01,s[i])

		for i in range(self.n):
			self.patients.append(Patient(i,s[i]))
		self.optimal_reward = self.get_optimal_reward()
		print("Optimal Reward is : ", self.optimal_reward)

	def get_optimal_reward(self):
		temp = [self.patients[i].p_adhere for i in range(self.n)]
		temp.sort()
		return sum([1-temp[i] for i in range(self.k)])

	def realize(self,selected):
		realizations = {}
		for pat in self.patients:
			if pat.index not in selected:
				realizations[pat.index] = bernoulli.rvs(size=1,p=pat.p_adhere)[0]
		return realizations

	def get_regret(self,selected):
		curr_reward = sum([1-self.patients[i].p_adhere for i in selected])
		# print("current reward is :",curr_reward)
		return self.optimal_reward - curr_reward


	# def generate_qualities(self,prod,quant):
	# 	avg_quality = sum(bernoulli.rvs(size=int(quant),p=prod.q))
	# 	# reward = self.R*int(avg_quality) - quant*prod.c 
	# 	# print(reward)
	# 	return avg_quality

	# def get_regret(self,x,opt_reward):
	# 	reward = self.get_expected_reward(x)
	# 	print("Reward : ",reward)
	# 	print("Regret : ",opt_reward-reward)
	# 	return opt_reward-reward

	# def get_qualities(self,x):
	# 	#[(index of producer, quantity allocated, realized total qualities)]
	# 	qualities = [[i,0,0] for i in range(self.n)]  
	# 	for i in range(self.n):
	# 		qualities[i][1] = x[i]
	# 		self.T += x[i]
	# 		qualities[i][2] = self.generate_qualities(self.producers[i],x[i])
	# 	return qualities

	# def get_expected_reward(self,x):
	# 	reward = 0
	# 	for i in range(self.n):
	# 		prod = self.producers[i]
	# 		reward += x[i]*(prod.r)
	# 	return reward		

	# def get_optimal(self,error_margin):
	# 	return get_optimal_allocation(self.producers,self.n,self.alpha-error_margin)

	# def reset(self):
	# 	for prod in self.producers:
	# 		prod.k_rem = prod.k

	# def get_max_revenue(self):
	# 	max_rev = 0
	# 	for i in range(self.n):
	# 		prod = self.producers[i]
	# 		max_rev += max(0,prod.r)
	# 	return max_rev