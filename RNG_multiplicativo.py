import numpy as np

class RNG_multiplicativo:
    def __init__(self, a, m, X_0):
        self.a = a
        self.m = m
        self.X = np.zeros(m, dtype='int64')
        self.X[0] = X_0
        self.X_acc = np.int64(X_0)

    def get_random_seq(self):
        for i in range(0, self.m-1):
            self.X[i+1] = np.mod((self.a * self.X[i]), self.m)

    def get_random(self):
        self.X_acc = np.mod((self.a * self.X_acc), self.m)
        return self.X_acc