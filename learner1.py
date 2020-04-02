import math

class Patient():
	def __init__(self,index):
		self.index = index
		self.p_adhere_est = 0.5
		self.adhere_freq = 0
		self.p_adhere_pos = 1.0
		self.p_adhere_history = [self.p_adhere_pos]

class LearnerAgent():
	def __init__(self,env):
		self.ucb_coeff = 1.0
		self.n = env.n
		self.k = env.k
		self.patients = self.initialize_prod(env)
		# self.fixed_indexed_patients = self.initialize_prod(env)

	def initialize_prod(self,env):
		patients = [None for i in range(env.n)]
		for i in range(env.n):
			pat = env.patients[i]
			patients[pat.index] = Patient(pat.index)
		return patients

	def choose_patients(self,round_no):
		if(round_no<(self.n+self.k-1)/self.k):
			return [(round_no*self.k+j)%self.n for j in range(self.k)]
		temp = self.patients.copy()
		# temp.sort(reverse=True) 
		temp.sort(key=lambda x: x.p_adhere_pos)
		return [temp[i].index for i in range(self.k)]

	def update(self,realizations,round_no):
		# print("updating")
		# print("updating realized records")
		for pat in realizations:
			# print("for pat : ",pat)
			curr_est = self.patients[pat].p_adhere_est
			curr_freq = self.patients[pat].adhere_freq
			# print("current estimate : ",curr_est,curr_freq)
			self.patients[pat].p_adhere_est = (curr_est*curr_freq + realizations[pat])/(curr_freq+1)
			self.patients[pat].adhere_freq += 1

		if(round_no<(self.n+self.k-1)/self.k):
			return

		for pat in self.patients:
			pat.p_adhere_pos = pat.p_adhere_est + self.ucb_coeff*math.sqrt((2*math.log(round_no+1))/(pat.adhere_freq))
			pat.p_adhere_pos = min(pat.p_adhere_pos,1.0)
			# pat.p_adhere_history.append(pat.p_adhere_pos)
			# print("new estimate : ", self.patients[pat].p_record_est	
		return

	def print_estimates(self):
		for i in range(self.n):
			print(self.patients[i].p_adhere_est)
