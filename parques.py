import random
import numpy as np
import matplotlib.pyplot as plt

N = 300000  # Número de iteraciones
cantidad_lanzamientos = 6

casos = np.array([i for i in range(0, cantidad_lanzamientos + 1)])
f_absoluta = np.zeros(len(casos))
f_relativa = np.zeros(len(casos))
total_lanzamientos = 0

for j in range(0, N):
    dado = [random.randint(1, 6) for k in range(0, cantidad_lanzamientos)]
    
    if dado[0] == 1:
        f_absoluta[0] += 1
    elif dado[1] == 1:
        f_absoluta[1] += 1
    elif dado[2] == 1:
        f_absoluta[2] += 1
    elif dado[3] == 1:
        f_absoluta[3] += 1
    elif dado[4] == 1:
        f_absoluta[4] += 1
    elif dado[5] == 1:
        f_absoluta[5] += 1

f_relativa = f_absoluta / N

print(f_relativa)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.bar(casos, f_relativa)
plt.xlabel("cantidad de lanzamientos antes del acierto")
plt.ylabel("distribución de probabilidad")
plt.show()

# Función de distribución de probabilidad acumulada
fr_acumulada = np.zeros_like(f_relativa)

for i in range(len(fr_acumulada)):
    for j in range(0, i + 1):
        fr_acumulada[i] += f_relativa[j]

print("Distribución de probabilidad acumulada", fr_acumulada)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.bar(casos, fr_acumulada)
plt.xlabel("cantidad de lanzamientos antes del acierto")
plt.ylabel("distribución de probabilidad acumulada")
plt.show()
