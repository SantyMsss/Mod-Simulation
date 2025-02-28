import random
import numpy as np
import matplotlib.pyplot as plt


# Desarrollado por: Santiago Martinez Serna
# Laura Sofia Toro 
# Santiago Alejandro Santacruz 


N = 300000  # Número de iteraciones (simulaciones)
probabilidad_acierto = 0.8  # Probabilidad de marcar un penalti
max_intentos = 5  # Número máximo de intentos que nos interesa analizar

# Inicialización de variables
casos = np.array([i for i in range(1, max_intentos + 1)])  # Intentos desde 1 hasta 5
f_absoluta = np.zeros(len(casos))  # Frecuencia absoluta de cada caso
f_relativa = np.zeros(len(casos))  # Frecuencia relativa de cada caso

# Simulación
for j in range(N):
    intentos = 0
    while True:
        intentos += 1
        if random.random() < probabilidad_acierto:  # Si acierta
            if intentos <= max_intentos:
                f_absoluta[intentos - 1] += 1
            break  # Termina la simulación para este lanzamiento

# Cálculo de la frecuencia relativa
f_relativa = f_absoluta / N

# Resultados
print("Distribución de probabilidad:", f_relativa)

# Gráfica de la distribución de probabilidad
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.bar(casos, f_relativa)
plt.xlabel("Número de intentos hasta el primer acierto")
plt.ylabel("Distribución de probabilidad")
plt.title("Distribución de probabilidad del primer acierto en un penalti")
plt.show()

# Función de distribución de probabilidad acumulada
fr_acumulada = np.zeros_like(f_relativa)

for i in range(len(fr_acumulada)):
    for j in range(0, i + 1):
        fr_acumulada[i] += f_relativa[j]

print("Distribución de probabilidad acumulada:", fr_acumulada)

# Gráfica de la distribución de probabilidad acumulada
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.bar(casos, fr_acumulada)
plt.xlabel("Número de intentos hasta el primer acierto")
plt.ylabel("Distribución de probabilidad acumulada")
plt.title("Distribución de probabilidad acumulada del primer acierto en un penalti")
plt.show()