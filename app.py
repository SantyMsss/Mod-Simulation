import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import geom

# Probabilidad de éxito (marcar un penalti)
p = 0.8

# Número de ensayos hasta el primer éxito
k = 5

# Calcular la probabilidad de que el primer éxito ocurra en el quinto intento
prob = (1 - p) ** (k - 1) * p
print(f"Probabilidad de marcar por primera vez en el quinto penalti: {prob:.5f}")

# Simulación de la distribución geométrica
x = np.arange(1, 11)
probs = geom.pmf(x, p)
cum_probs = geom.cdf(x, p)

# Graficar la distribución de probabilidad
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.bar(x, probs, color='blue')
plt.title('Distribución de Probabilidad')
plt.xlabel('Número de Penaltis')
plt.ylabel('Probabilidad')

# Graficar la distribución de probabilidad acumulada
plt.subplot(1, 2, 2)
plt.step(x, cum_probs, where='post', color='red')
plt.title('Distribución de Probabilidad Acumulada')
plt.xlabel('Número de Penaltis')
plt.ylabel('Probabilidad Acumulada')

plt.tight_layout()
plt.show()