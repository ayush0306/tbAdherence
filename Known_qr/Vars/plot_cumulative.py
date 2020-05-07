import pickle as pl
import matplotlib.pyplot as plt
import math
import numpy as np


filename = ["Regret_learner1_40_40_39_UCB_v1", "Regret_learner1_40_40_39_Thompson_Sampling_v1"]
# filename = ["regret__50_50.0_50000","regret__100_50.0_100000","regret__250_50.0_50000"]
legend = ["UCB1","Thompson Sampling"]
# legend = ["n=50","n=100","n=150"]
colors = ['--r','-g']
out_fil = "cum_regrets.png"
# epsilon = [10,20,50,100]
# tau = [1.5*i*i*math.log(100000) for i in epsilon]

ind = 0
for files,color in zip(filename,colors):
	with open(files,'rb') as f:
		regret = pl.load(f)

	# print(len(regret),regret[0:10],type(regret))
	cum_regret = np.cumsum(regret)
	T = len(cum_regret)
	print(T)
	# dfx = [math.log(i+1) for i in range(T)]
	# print(dfx[-1])
	# cum_regret = [0.0 for i in range(len(regret))]
	# for i in range(1,len(regret)):
	# 	cum_regret[i] = float(regret[i])/100.0 + cum_regret[i-1]
	# # plt.plot(regret[0:50000],color)
	# plt.plot(dfx,cum_regret,color)
	plt.plot(cum_regret,color)
# 	plt.plot(regret[0:5000],color)

plt.title("CumReg vs t")
# plt.xlabel("Rounds(t)")
plt.xlabel("T")
plt.ylabel("Cumulative Regret")
plt.legend(legend,loc='lower right')
plt.savefig(out_fil, dpi=300)
# plt.show()
