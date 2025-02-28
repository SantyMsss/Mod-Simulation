import matplotlib.pyplot as plt
import numpy as np

multiplicador = 7**5
modulo = 2**31 - 1
semilla = 42  # Elige un valor distinto de cero como semilla

def generator_congruente_multiplicativo(semilla, n):
    numeros = []
    for _ in range(n):
        semilla = (multiplicador * semilla) % modulo
        numeros.append(semilla / modulo)
    return numeros

n = 1000000  # Número de muestras
numeros_aleatorios = generator_congruente_multiplicativo(semilla, n)

plt.hist(numeros_aleatorios, bins=50)
plt.xlabel('valor')
plt.ylabel('Frecuencia')
plt.title('Histograma de números aleatorios')
plt.show()