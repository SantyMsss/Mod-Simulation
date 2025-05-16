import numpy as np
import matplotlib.pyplot as plt

Ns = 100
Eo = 5.0
R = 1000
C = 47e-6
tau = R*C
E = np.array([Eo for i in range(Ns)])
t = np.array([0.0 for i in range(Ns)])
Iout = np.array([0.0 for i in range(Ns)])
Iout[0] = Eo/R
print("Iout: ", Iout)
f = Iout[0]

fi = 0.0
dt = tau/5
clock = 0.0
t[0] = clock

for i in range(1,Ns):
    clock += dt
    df = f*dt/(-R*C)
    f = f + df
    Iout[i] = f
    t[i] = clock

print("Iout: ", Iout)
fig, axs = plt.subplots(ncols=1, nrows=2)
axs[0].plot(t, E, 'tab:blue')
axs[1].plot(t, Iout, 'tab:green')
plt.show()