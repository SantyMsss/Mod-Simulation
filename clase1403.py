import random
import numpy as np
import matplotlib.pyplot as plt

N = 20000
datos = np.zeros(N)
exp_datos = np.zeros(N)
Lamda = -1.5

for i in range(N):
	datos[i] = random.random()
	exp_datos[i] = (1 / Lamda) * np.log(datos[i])
	print(datos[i])

plt.hist(exp_datos, bins=400, density=True)
plt.show()