import scipy.stats as stats

learner_name = "Thompson_Sampling"

class Patient():
    def __init__(self,index,p_tp,p_fp):
        self.index = index
        self.p_call_est = 0.5
        self.p_tp = p_tp
        self.p_fp = p_fp
        self.alpha = 1
        self.beta = 1

		
class LearnerAgent():
    def __init__(self,env):
		#self.ucb_coeff = 1.0
        self.n = env.n
        self.k = env.k
        self.patients = self.initialize_prod(env)
		
    def initialize_prod(self,env):
        patients = [None for i in range(env.n)]
        for i in range(env.n):
            pat = env.patients[i]
            patients[pat.index] = Patient(pat.index,pat.p_tp,pat.p_fp)
        return patients

    def estimate_adh(self,pat,p_call):
        return (p_call - pat.p_fp)/(pat.p_tp - pat.p_fp)

    def choose_patients(self,round_no):
        # if(round_no<(self.n+self.k-1)/self.k):
        #     return [(round_no*self.k+j)%self.n for j in range(self.k)]
        # temp = self.patients.copy()
        dict_patients = {}
        for i in range(len(self.patients)):
            p_call = stats.beta.rvs(self.patients[i].alpha,self.patients[i].beta)
            p_call = max(p_call,self.patients[i].p_fp)
            p_call = min(p_call,self.patients[i].p_tp)
            dict_patients[self.patients[i].index] = self.estimate_adh(self.patients[i],p_call)
        
        patients_sorted = sorted(dict_patients.items(), key = lambda kv: kv[1])[:self.k]
        return [k[0] for k in patients_sorted]
        
    def update(self,realizations,round_no):
        for pat in realizations:
            if(realizations[pat] == 1):
                self.patients[pat].alpha += 1
            else:
                self.patients[pat].beta += 1

        # for pat in self.patients:
        #     pat.p_call_est = stats.beta.rvs(pat.alpha,pat.beta)
        return

    def print_estimates(self):
        for i in range(self.n):
            print('(',self.patients[i].alpha,',',self.patients[i].beta,')',sep="",end=" ")
        print()
