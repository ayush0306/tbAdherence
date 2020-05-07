import pickle as pl
import matplotlib.pyplot as plt
import math


filename = ["Regret_learner1_100_twTh"]
# filename = ["regret__50_50.0_50000","regret__100_50.0_100000","regret__250_50.0_50000"]
legend = ["UCB1"]
# legend = ["n=50","n=100","n=150"]
colors = ['--r']
out_fil = "regrets.png"
# epsilon = [10,20,50,100]
# tau = [1.5*i*i*math.log(100000) for i in epsilon]

ind = 0
for files,color in zip(filename,colors):
	with open(files,'rb') as f:
		regret = pl.load(f)

	print(len(regret),regret[0:10])
	# cum_regret = [0.0 for i in range(len(regret))]
	# for i in range(1,len(regret)):
	# 	cum_regret[i] = float(regret[i])/100.0 + cum_regret[i-1]
	# # plt.plot(regret[0:50000],color)
	# plt.plot(cum_regret[0:100000],color)
	plt.plot(regret[0:15000],color)

plt.title("Reg(T) vs t")
plt.xlabel("Rounds(t)")
plt.ylabel("Regret")
plt.legend(legend,loc='lower right')
plt.savefig(out_fil, dpi=300)
# plt.show()
