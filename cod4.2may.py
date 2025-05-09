import numpy as np
from random import uniform, seed
from matplotlib.pyplot import *
from statistics import mean

def simulacion_cine(tiempo_control_media, tiempo_control_var, n_personas=100, n_replicas=5):
    resultados = {
        'tiempo_total': [],
        'tiempo_espera_promedio': [],
        'max_cola': []
    }
    
    for _ in range(n_replicas):
        seed()  # Reiniciamos la semilla aleatoria para cada réplica
        
        # Variables de estado
        tiempo_actual = 0
        tiempo_llegadas = [0]
        tiempo_servicios = []
        tiempo_salidas = []
        cola = 0
        max_cola = 0
        
        # Generar tiempos de llegada (uniforme entre 0 y 120 segundos)
        for _ in range(n_personas - 1):
            tiempo_llegadas.append(tiempo_llegadas[-1] + uniform(0, 120))
        
        # Procesar cada persona
        for i in range(n_personas):
            # Tiempo de servicio (uniforme alrededor de la media)
            servicio = uniform(tiempo_control_media - tiempo_control_var, 
                              tiempo_control_media + tiempo_control_var)
            
            if tiempo_actual < tiempo_llegadas[i]:
                tiempo_actual = tiempo_llegadas[i]
                cola = 0
            else:
                cola = sum(1 for t in tiempo_salidas if t > tiempo_llegadas[i])
                if cola > max_cola:
                    max_cola = cola
            
            tiempo_servicios.append(servicio)
            tiempo_salida = tiempo_actual + servicio
            tiempo_salidas.append(tiempo_salida)
            tiempo_actual = tiempo_salida
        
        # Calcular métricas
        tiempos_espera = [max(0, tiempo_salidas[i] - tiempo_llegadas[i] - tiempo_servicios[i]) 
                          for i in range(n_personas)]
        
        resultados['tiempo_total'].append(tiempo_salidas[-1])
        resultados['tiempo_espera_promedio'].append(mean(tiempos_espera))
        resultados['max_cola'].append(max_cola)
    
    return resultados

# Parámetros del problema
n_personas = 100
n_replicas = 5

# Escenario 1: Control de entrada de 70 +/- 30 segundos
escenario1 = simulacion_cine(70, 30, n_personas, n_replicas)

# Escenario 2: Control de entrada de 50 +/- 30 segundos
escenario2 = simulacion_cine(50, 30, n_personas, n_replicas)

# Resultados
print("=== Escenario 1 (70±30 segundos) ===")
print(f"Tiempo total promedio: {mean(escenario1['tiempo_total']):.1f} segundos")
print(f"Tiempo de espera promedio: {mean(escenario1['tiempo_espera_promedio']):.1f} segundos")
print(f"Máximo tamaño de cola promedio: {mean(escenario1['max_cola']):.1f} personas")
print("\n=== Escenario 2 (50±30 segundos) ===")
print(f"Tiempo total promedio: {mean(escenario2['tiempo_total']):.1f} segundos")
print(f"Tiempo de espera promedio: {mean(escenario2['tiempo_espera_promedio']):.1f} segundos")
print(f"Máximo tamaño de cola promedio: {mean(escenario2['max_cola']):.1f} personas")

# Visualización
figure(figsize=(12, 6))
subplot(1, 2, 1)
boxplot([escenario1['tiempo_total'], escenario2['tiempo_total']])
title('Tiempo total para entrar')
xticks([1, 2], ['70±30s', '50±30s'])
ylabel('Segundos')

subplot(1, 2, 2)
boxplot([escenario1['tiempo_espera_promedio'], escenario2['tiempo_espera_promedio']])
title('Tiempo promedio de espera')
xticks([1, 2], ['70±30s', '50±30s'])
ylabel('Segundos')

tight_layout()
show()