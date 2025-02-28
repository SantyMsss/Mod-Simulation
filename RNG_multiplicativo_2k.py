from RNG_multiplicativo import RNG_multiplicativo

def RNG_multiplicativo_2k(t, k, X_0):
    a = 8 * t + 3
    m = 2 ** k
    T = 2 ** (k - 2)
    RNG_base = RNG_multiplicativo(a, m, X_0)
    RNG_base.get_random_seq()
    return (RNG_base.X, m, T)

t = 1
k = 4
X_0 = 1
(sequence, modulo, periodo) = RNG_multiplicativo_2k(t, k, X_0)
sequence_norm = sequence / modulo
print("secuencia:", sequence)
print("periodo de la secuencia:", periodo)
print("secuencia normalizada:", sequence_norm)