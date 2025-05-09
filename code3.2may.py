# Performing multiple independent simulation runs of the simulation model of the single-server queueing system.

# simLib is your simulation library, which you will reuse
# in your homework and projects.
# It is available in the github repository

from simLib import mm1
from random import seed
from statistics import mean

lamda = 1.3
mu = 2
n = 100000  # Number of packets to be simulated

Num_Repl = 50  # Number of replications (repetitions)
Delay = []     # Data set for storing delay results

for i in range(Num_Repl):
    seed()  # Reseed RNG for each replication
    d = mm1(lamda, mu, n)  # Run simulation
    Delay.append(d)

# Estimate of performance measure
print("Average Delay = ", round(mean(Delay), 4))