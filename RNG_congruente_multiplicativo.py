import numpy as np

def RNG_multiplicativo(a, m, X_0):
    X = np.zeros(m)
    X[0] = X_0
    for i in range(0, m-1):
        X[i+1] = np.mod((a * X[i]), m)
    return X

modulo = 10
sequence = RNG_multiplicativo(2, modulo, 3)
sequence_norm = sequence / modulo
print("X_n", sequence)
print("u_n", sequence_norm)