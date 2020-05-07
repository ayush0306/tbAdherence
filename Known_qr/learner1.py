import math

learner_name = "UCB"

class Patient():
	def __init__(self,index,p_tp,p_fp):
		self.index = index
		self.p_call_est = 0.5
		self.call_freq = 0
		self.p_call_pos = 1.0
		self.p_call_history = [self.p_call_pos]
		self.p_tp = p_tp
		self.p_fp = p_fp

class LearnerAgent():
	def __init__(self,env):
		self.ucb_coeff = 0.5
		self.n = env.n
		self.k = env.k
		self.patients = self.initialize_prod(env)
		# self.fixed_indexed_patients = self.initialize_prod(env)

	def initialize_prod(self,env):
		patients = [None for i in range(env.n)]
		for i in range(env.n):
			pat = env.patients[i]
			patients[pat.index] = Patient(pat.index,pat.p_tp,pat.p_fp)
		return patients

	def estimate_adh(self,pat):
		return (pat.p_call_pos - pat.p_fp)/(pat.p_tp - pat.p_fp)

	def choose_patients(self,round_no):
		if(round_no<self.n):
			return [(round_no+j)%self.n for j in range(self.k)]
		temp = self.patients.copy()
		# temp.sort(reverse=True) 
		temp.sort(key=lambda x: self.estimate_adh(x))
		# for i in range(self.n):
		# 	print('(',temp[i].index,',',temp[i].p_call_pos,',',self.estimate_adh(temp[i]),')',sep="",end=" ")
		# print()
		return [temp[i].index for i in range(self.k)]

	def update(self,realizations,round_no):
		# print("updating")
		# print("updating realized records")
		for pat in realizations:
			# print("for pat : ",pat)
			curr_est = self.patients[pat].p_call_est
			curr_freq = self.patients[pat].call_freq
			# print("current estimate : ",curr_est,curr_freq)
			self.patients[pat].p_call_est = (curr_est*curr_freq + realizations[pat])/(curr_freq+1)
			self.patients[pat].call_freq += 1

		if(round_no<self.n):
			return

		for pat in self.patients:
			pat.p_call_pos = pat.p_call_est + self.ucb_coeff*math.sqrt((2*math.log(round_no+1))/(pat.call_freq))
			pat.p_call_pos = min(pat.p_call_pos,pat.p_tp)
			pat.p_call_pos = max(pat.p_call_pos,pat.p_fp)
			# pat.p_call_history.append(pat.p_call_pos)
			# print("new estimate : ", self.patients[pat].p_record_est	
		return

	def print_estimates(self):
		for i in range(self.n):
			print('(',self.patients[i].p_call_pos,',',self.patients[i].call_freq,')',sep="",end=" ")
		print()
