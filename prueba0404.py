from random import expovariate
from statistics import mean
from math import inf as Infinity

# Parámetros
lamda = 1.3  # Tasa de llegada (Lambda)
mu = 2.0  # Tasa de salida (Mu)
Num_Pkts = 100000  # Número de paquetes a simular
count = 0  # Contador de paquetes simulados
clock = 0  # Reloj del sistema
N = 0  # Variable de estado; número de paquetes en el sistema

Arr_Time = expovariate(lamda)
Dep_Time = Infinity

# Variables de salida
Arr_Time_Data = []  # Recopilar tiempos de llegada
Dep_Time_Data = []  # Recopilar tiempos de salida
Delay_Data = []  # Recopilar retrasos individuales de paquetes

while count < Num_Pkts:
    if Arr_Time < Dep_Time:  # Evento de llegada
        clock = Arr_Time
        Arr_Time_Data.append(clock)
        N += 1
        Arr_Time = clock + expovariate(lamda)
        if N == 1:
            Dep_Time = clock + expovariate(mu)
    else:  # Evento de salida
        clock = Dep_Time
        Dep_Time_Data.append(clock)
        N -= 1
        count += 1  # Paquete simulado
        if N > 0:
            Dep_Time = clock + expovariate(mu)
        else:
            Dep_Time = Infinity

for i in range(Num_Pkts):
    d = Dep_Time_Data[i] - Arr_Time_Data[i]
    Delay_Data.append(d)

print("Average Delay =", round(mean(Delay_Data), 4))
