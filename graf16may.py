from random import expovariate
from bisect import insort_right

# Parameters
lamda = 0.5  # Changed from 'lambda' (Python keyword) to 'lamda'
mu = 0.7
n = 100  # Number of packets to be simulated

# Initialization
clock = 0.0  # Simulation clock
evList = []  # Event list
count = 0    # Count number of packets simulated so far
N = 0        # State variable (number of packets in system)

# Insert an event into the event list
def insert(ev):
    insort_right(evList, ev)  # Changed from 'insert_right' to 'insort_right'

# Event generator for the arrival event
def Gen_Arr_Ev(clock):
    global count
    count += 1
    if count <= n:
        ev = (clock + expovariate(lamda), Handle_Arr_Ev)  # Fixed 'Lamda' to 'lamda'
        insert(ev)

# Event generator for the departure event
def Gen_Dep_Ev(clock):
    ev = (clock + expovariate(mu), Handle_Dep_Ev)
    insert(ev)

# Event handler for the arrival event
def Handle_Arr_Ev(clock):
    global N
    N = N + 1  # Update state variable
    Gen_Arr_Ev(clock)  # Generate next arrival event
    if N == 1:
        Gen_Dep_Ev(clock)

# Event handler for the departure event
def Handle_Dep_Ev(clock):
    global N
    N = N - 1
    if N > 0:
        Gen_Dep_Ev(clock)

# Initialize state variables and generate initial events
N = 0  # State variable
Gen_Arr_Ev(0.0)  # Initial event

# Simulation loop
while evList:
    ev = evList.pop(0)
    clock = ev[0]
    ev[1](clock)  # Handle event
    print(f"Clock: {clock:.2f}, N: {N}, Count: {count}")
    
