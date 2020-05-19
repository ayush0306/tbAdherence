import numpy as np
from scipy.stats import bernoulli

class Patient():
	def __init__(self,index,p_adhere,p_tp,p_fp):
		self.index = index
		self.p_adhere = p_adhere
		if(abs(p_tp-p_fp) <= 0.1):
			p_tp = 0.55
			p_fp = 0.45
		self.p_fp = min(p_tp,p_fp)
		self.p_tp = max(p_tp,p_fp)
		self.p_call = self.p_adhere*self.p_tp + (1-self.p_adhere)*self.p_fp
		self.adh_since_last = 0
		self.tp_since_last = 0

class Environment():
	def __init__(self,n,k):
		self.n = n
		self.k = k
		self.T = 0
		self.patients = []
		self.optimal_reward = 0
		self.mu = 50
		self.sigma = 25

	def nearest_two(self,arr):
		for i in range(len(arr)):
			arr[i] = int(arr[i])/float(100)
			arr[i] = min(arr[i],0.99)
			arr[i] = max(0.01,arr[i])
		return arr

	def reset(self,j):
		self.patients = []
		np.random.seed(j)
		s = np.random.normal(self.mu, self.sigma, self.n)
		q = np.random.random(self.n)*100
		r = np.random.random(self.n)*100
		s,q,r = self.nearest_two(s),self.nearest_two(q),self.nearest_two(r)

		for i in range(self.n):
			self.patients.append(Patient(i,s[i],q[i],r[i]))
		self.optimal_reward = self.get_optimal_reward()
		print("Optimal Reward is : ", self.optimal_reward)

	def get_optimal_reward(self):
		temp = [self.patients[i].p_adhere for i in range(self.n)]
		temp.sort()
		print(temp)
		print(sum([1-temp[i] for i in range(self.k)]))
		return sum([1-temp[i] for i in range(self.k)])

	def realize(self,selected,round_no):
		call_realizations, q_info = {},{}
		for pat in self.patients:
			if pat.index not in selected:
				if_adh = bernoulli.rvs(size=1,p=pat.p_adhere)[0]
				if(round_no < self.n):
					if_adh = 1
				if(if_adh):
					pat.adh_since_last += 1 
					if_call = bernoulli.rvs(size=1,p=pat.p_tp)[0]
					call_realizations[pat.index] = if_call
					if(if_call):
						pat.tp_since_last += 1
				else:
					call_realizations[pat.index] = bernoulli.rvs(size=1,p=pat.p_fp)[0]
			
			else:
				q_info[pat.index] = (pat.tp_since_last,pat.adh_since_last)
				pat.tp_since_last = 0
				pat.adh_since_last = 0
				
		return call_realizations,q_info

	def get_regret(self,selected):
		curr_reward = sum([1-self.patients[i].p_adhere for i in selected])
		if(curr_reward > self.optimal_reward+0.0001):
			print(curr_reward,self.optimal_reward)
			print(selected)
			print([1-self.patients[i].p_adhere for i in selected])
			exit(0)
		# print("current reward is :",curr_reward)
		return self.optimal_reward - curr_reward

	def print_estimates(self):
		for i in range(self.n):
			print(i,self.patients[i].p_adhere,self.patients[i].p_tp,self.patients[i].p_fp,self.patients[i].p_call,sep=",")


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