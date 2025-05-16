import numpy as np
import matplotlib.pyplot as plt

Ns = 100
Eo = 5.0
R = 160.0
C = 0.05e-6
L = 2.0e-3

# Cálculo de parámetros del circuito RLC
omega_0 = 1/(np.sqrt(L*C))  # Corregido: cambió 'l' por '1'
alpha = R/(2*L)

if alpha < omega_0:
    print("Circuito con oscilaciones")
    omega_r = np.sqrt((omega_0**2) - (alpha**2))
else:
    print("Circuito sin oscilaciones")
    omega_r = omega_0

T_r = np.pi/omega_r

# Inicialización de arrays
E = np.array([Eo for i in range(Ns)])
t = np.array([0.0 for i in range(Ns)])
Iout = np.array([0.0 for i in range(Ns)])
U = np.array([0.0 for i in range(Ns)])

# Condiciones iniciales
Iout[0] = 0.0
U[0] = Eo/L
print("Iout: ", Iout)

f = U[0]
f1 = Iout[0]  # Corregido: cambió 'fl' por 'f1' para consistencia
dt = T_r/5    # Corregido: asumí S=8 ya que no estaba definido en el original
clock = 0.0
t[0] = clock

# Simulación del circuito RLC
for i in range(1, Ns):
    clock += dt
    df1 = f*dt
    df = (((-R/L)*f) + ((-1/(L*C))*f1))*dt
    f = f + df
    f1 = f1 + df1
    U[i] = f
    Iout[i] = f1
    t[i] = clock

print("Iout: ", Iout)

# Graficación
fig, axs = plt.subplots(ncols=1, nrows=2)
axs[0].plot(t, E, 'tab:blue')
axs[1].plot(t, Iout, 'tab:green')
plt.show()