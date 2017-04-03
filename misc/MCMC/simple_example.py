import random as rnd
import math 

def sample(n,mu,sigma):
    
    samples=[]
    for i in range(n):
        samples.append(rnd.gauss(mu,sigma))

    return samples

class Theta_prior:

    def __init__(self,mu_range,sigma_range):
        self.mu_range=mu_range
        self.sigma_range=sigma_range

    def get_mu(self):
        return rnd.uniform(-self.mu_range,self.mu_range)

    def get_sigma(self):
        return rnd.uniform(0,self.sigma_range)

    def get_mu_pdf(self):
        return 1/(2*self.mu_range)

    def get_sigma_pdf(self):
        return 1/self.sigma_range

def accept(p_proposed,p_current):

    print p_proposed,p_current,
    
    if p_proposed==0:
        return False
    if p_proposed>p_current:
        return True
    if rnd.random()<p_proposed/p_current:
        return True
    return False

class Normal_pdf:
    def __init__(self,mu,sigma):
        self.mu=mu
        self.sigma=sigma
        self.normalize=1./math.sqrt(2*math.pi)

    def __call__(self,x):
        return self.normalize*1/self.sigma*math.exp(-pow(x-self.mu,2)/(2.*pow(self.sigma,2)))

#make some data

mu=0.7
sigma=1.1
n=250

print mu,sigma

sampled_data=sample(n,mu,sigma)

#initial conditions for MCMC

mu_range=2.
sigma_range=2.

theta_prior=Theta_prior(mu_range,sigma_range)

mu=theta_prior.get_mu()
sigma=theta_prior.get_sigma()

print mu,sigma


stride_mu=0.5
stride_sigma=0.25


burn_in_n=5000
big_n=10000+burn_in_n

p=0
mus=[]
sigmas=[]

markov_c=0

while markov_c<big_n:

    proposed_mu=rnd.gauss(mu,stride_mu)
    proposed_sigma=rnd.gauss(sigma,stride_sigma)

    print markov_c,proposed_mu,proposed_sigma,


    proposed_p=1


    if proposed_mu>mu_range or proposed_mu<-mu_range or proposed_sigma>sigma_range or proposed_sigma<0:
        proposed_p=0
    else:

        pdf=Normal_pdf(proposed_mu,proposed_sigma)

        for x in sampled_data:
            proposed_p*=pdf(x)
        proposed_p*=theta_prior.get_mu_pdf()*theta_prior.get_sigma_pdf()


    if accept(proposed_p,p):
        print "A"
        mu=proposed_mu
        sigma=proposed_sigma
        p=proposed_p
        markov_c+=1

        if markov_c>burn_in_n:
            mus.append(mu)
            sigmas.append(sigma)
    else:
        print "R"

print sum(mus)/float(len(mus)),sum(sigmas)/float(len(sigmas))










    

