import math
import random

learner_name = "UCB"

class Patient():
	def __init__(self,index,p_fp):
		self.index = index
		self.call_freq = 0
		self.adhere_freq = 0
		self.p_call_est = 0.5
		self.p_call_pos = 1.0
		self.p_tp_est = 0.5
		self.p_tp_neg = 0.00
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
			patients[pat.index] = Patient(pat.index,pat.p_fp)
		return patients

	def estimate_adh(self,pat):
		deno = max(0.01,pat.p_tp_neg - pat.p_fp)
		temp = (pat.p_call_pos - pat.p_fp)/(deno)
		temp = min(temp,1)
		temp = max(0,temp)
		return temp

	def choose_patients(self,round_no):
		if(round_no<self.n):
			return [(round_no+j)%self.n for j in range(self.k)]
		temp = self.patients.copy()
		random.shuffle(temp)
		# temp.sort(reverse=True) 
		temp.sort(key=lambda x: self.estimate_adh(x))
		# for i in range(self.n):
		# 	print('(',temp[i].index,',',temp[i].p_call_pos,',',self.estimate_adh(temp[i]),')',sep="",end=" ")
		# print()
		return [temp[i].index for i in range(self.k)]

	def update(self,realizations,q_info,round_no):
		for pat in realizations:
			curr_est = self.patients[pat].p_call_est
			curr_freq = self.patients[pat].call_freq
			# print("current estimate : ",curr_est,curr_freq)
			self.patients[pat].p_call_est = (curr_est*curr_freq + realizations[pat])/(curr_freq+1)
			self.patients[pat].call_freq += 1

		for pat in q_info:
			curr_est = self.patients[pat].p_tp_est
			curr_freq = self.patients[pat].adhere_freq
			if(q_info[pat][1] == 0):
				continue
			self.patients[pat].adhere_freq  += q_info[pat][1]
			self.patients[pat].p_tp_est = (curr_est*curr_freq + q_info[pat][0])/(self.patients[pat].adhere_freq)
			self.patients[pat].p_tp_neg = self.patients[pat].p_tp_est - self.ucb_coeff*math.sqrt((2*math.log(round_no+1))/(self.patients[pat].adhere_freq))

		if(round_no<self.n):
			return

		for pat in self.patients:
			pat.p_call_pos = pat.p_call_est + self.ucb_coeff*math.sqrt((2*math.log(round_no+1))/(pat.call_freq))
			# pat.p_call_pos = min(pat.p_call_pos,pat.p_tp)
			# pat.p_call_pos = max(pat.p_call_pos,pat.p_fp)
			# pat.p_call_history.append(pat.p_call_pos)
			# print("new estimate : ", self.patients[pat].p_record_est	
		return

	def print_estimates(self):
		for i in range(self.n):
			print('(',end="")
			pat = self.patients[i]
			print(pat.p_call_est,pat.p_call_pos,pat.call_freq,pat.p_tp_neg,pat.adhere_freq,sep=",",end="")
			print(')',end=",")
		print()
