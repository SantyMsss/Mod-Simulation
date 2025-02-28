import random
import numpy as np

p = 7
b = 3

b_pow = np.array([(b**i) % p for i in range(0,p-1)])
print("b_pow",b_pow)

p_model_set = np.array([i for i in range(1,p)])
print("p_model_set",p_model_set)

b_sort = np.sort(b_pow) # quick sort by default 0(n^2)
print(b_sort)

comparison = b_sort == p_model_set
print("comparison", comparison)

equal_arrays = comparison.all()
print("is p a primitive root of b?:", equal_arrays)