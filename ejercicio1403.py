import matplotlib.pyplot as plt
import numpy as np

# Parámetros del generador congruencial multiplicativo
multiplicador = 7**5
modulo = 2**31 - 1
semilla = 42  # Semilla inicial distinta de cero
Lamda = -1.5  # Parámetro para la distribución exponencial
N = 20000  # Número de muestras

def generator_congruente_multiplicativo(semilla, n):
    numeros = []
    for _ in range(n):
        semilla = (multiplicador * semilla) % modulo
        numeros.append(semilla / modulo)
    return numeros

# Generamos números aleatorios uniformes
datos_uniformes = generator_congruente_multiplicativo(semilla, N)

# Transformamos los datos para seguir una distribución exponencial
exp_datos = [(1 / Lamda) * np.log(x) for x in datos_uniformes]

# Graficamos el histograma
plt.hist(exp_datos, bins=400, density=True, alpha=0.75, color='blue')
plt.xlabel('Valor')
plt.ylabel('Densidad de Frecuencia')
plt.title('Histograma de Distribución Exponencial')
plt.show()
