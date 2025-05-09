# Estimating the steady-state probability distribution (P[N = k]).

from random import expovariate  
from math import inf as Infinity  

# Parameters  
lambda_ = 1.3  # Cambiado a lambda_ porque lambda es palabra reservada
mu = 2.0  
Num_Pkts = 100000000  
count = 0  
clock = 0  
N = 0  

Arr_Time = expovariate(lambda_)  
Dep_Time = Infinity  
Prev_Event_Time = 0.0  

Data = {} # Dictionary to store time intervals per state

while count < Num_Pkts:  
    if Arr_Time < Dep_Time:  
        clock = Arr_Time
        # Length of time interval
        delta = clock - Prev_Event_Time
        if N in Data: 
            Data[N] += delta
        else:    
            Data[N] = delta

        Prev_Event_Time = clock
        N = N + 1.0
        Arr_Time = clock + expovariate(lambda_)
        if N == 1:
            Dep_Time = clock + expovariate(mu)
    else:
        clock = Dep_Time
        # Length of time interval
        delta = clock - Prev_Event_Time
        if N in Data: 
            Data[N] += delta
        else:    
            Data[N] = delta

        Prev_Event_Time = clock
        N = N - 1.0
        count = count + 1
        if N > 0:
            Dep_Time = clock + expovariate(mu)
        else:
            Dep_Time = Infinity

# Compute probabilities
for (key, value) in Data.items():
    Data[key] = value / clock

# Check total probability is 1.0
print("Sum of Prob's = ", sum(Data.values()))

# Check expectation
mean = 0.0
for (key, value) in Data.items():
    mean = mean + key * value

print("E[N] = ", mean)