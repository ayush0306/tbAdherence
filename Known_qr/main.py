import environment
from learner2 import *
import matplotlib.pyplot as plt 
import numpy as np
import pickle
import numpy as np

def get_inputs():
	n = int(input("Enter the number of patients"))
	print("Now, for each manufacturer, enter its probability of adherence and probability of calling if not")
	prob_adherence = []
	for i in range(n):
		a = input()
		prob_adherence.append(float(a))
	return n,prob_adherence

def myPlot(df,title,filepath):
	plt.plot(df)
	plt.title(title)
	plt.savefig(filepath+".png")
	plt.close()

def mybarPlot(dfx,dfy,title,filepath):
	plt.bar(dfx,dfy)
	plt.title(title)
	plt.savefig(filepath+".png")
	plt.close()

def saveVar(var,filename):
	with open(filename,'wb') as f:
		pickle.dump(var,f)

# n,prob_adherence = get_inputs()
# k = int(n/3)
n = 10
k = 9
env = environment.Environment(n,k)

nrounds = 100
nsim = 25000
suffix = "_" + str(n) + "_" + str(k) + "_" + str(learner_name) + "_trial4"

regrets = np.array([0.0 for i in range(nsim)])
count_arm = np.array([0.0 for i in range(n)])

for j in range(nrounds):
	env.reset(j*3+6)
	env.print_estimates()
	learner = LearnerAgent(env)
	for i in range(nsim):
		print("round no. ",j," iter no. ",i)
		selection = learner.choose_patients(i)
		# print("selection", selection,env.optimal_reward)
		for arm in selection:
			count_arm[arm]+=1
		realizations = env.realize(selection)
		# print(realized_records,realized_calls)
		learner.update(realizations,i)
		# env.print_estimates()
		# learner.print_estimates()
		regret = env.get_regret(selection)
		print("regret: ",regret)
		print()
		regrets[i] = regrets[i]+regret
learner.print_estimates()

myPlot(regrets[n:]/float(nrounds),'Regret Analysis','./Plots/Regret_'+str(n)+suffix)
dfx = np.array([i for i in range(n)])
# mybarPlot(dfx,count_arm/float(nrounds),'Count of selection','./Vars/Count_'+str(n)+suffix)
saveVar(regrets/float(nrounds),'./Vars/Regret_learner1_'+str(n)+suffix)
# saveVar(count_arm/float(nrounds),'./Vars/Count_'+str(n)+suffix)

