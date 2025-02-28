import numpy as np
import matplotlib.pyplot as plt

def RNG_congruente_lineal(a, c, m, X_0, n_iterations):
    X = np.zeros(n_iterations)
    X[0] = X_0
    for i in range(0, n_iterations - 1):
        X[i + 1] = np.mod((a * X[i]) + c, m)
    return X

# Parámetros 
a = 106
M = 6075
c = 1283
X_0 = 5
n_iterations = 10000

# Generación de la secuencia
sequence = RNG_congruente_lineal(a, c, M, X_0, n_iterations)
sequence_norm = sequence / M

# Creación del histograma
plt.hist(sequence_norm, bins=100, density=True, alpha=0.75)
plt.title('Histograma de números generados por RNG congruencial lineal')
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.show()

# Cálculo del valor promedio
average_value = np.mean(sequence_norm)
print(f"El valor promedio de los números generados es: {average_value}")