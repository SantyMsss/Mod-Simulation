import random
from math import inf as infinity

def mm1_simulation():
    # Parámetros del sistema
    lambda_ = 0.4  # Tasa de llegada
    mu = 0.8       # Tasa de servicio
    simulation_time = 200  # Tiempo total de simulación
    
    # Variables de estado
    clock = 0
    N = 0  # Número de clientes en el sistema
    next_arrival = random.expovariate(lambda_)
    next_departure = infinity
    
    # Estadísticas
    arrival_times = []
    departure_times = []
    queue_lengths = []
    
    print("Simulación del sistema M/M/1")
    print("Tiempo\tN\tEvento")
    
    while clock <= simulation_time:
        # Registrar el estado actual
        queue_lengths.append((clock, N))
        
        if next_arrival < next_departure:
            # Evento de llegada
            clock = next_arrival
            N += 1
            arrival_times.append(clock)
            print(f"{clock:.2f}\t{N}\tLlegada")
            
            # Programar próxima llegada
            next_arrival = clock + random.expovariate(lambda_)
            
            # Si es el único cliente, programar su salida
            if N == 1:
                next_departure = clock + random.expovariate(mu)
        else:
            # Evento de salida
            clock = next_departure
            N -= 1
            departure_times.append(clock)
            print(f"{clock:.2f}\t{N}\tSalida")
            
            # Si quedan clientes, programar próxima salida
            if N > 0:
                next_departure = clock + random.expovariate(mu)
            else:
                next_departure = infinity
    
    # Calcular tiempos de espera
    wait_times = []
    num_customers = min(len(arrival_times), len(departure_times))
    
    for i in range(num_customers):
        wait_time = departure_times[i] - arrival_times[i]
        wait_times.append(wait_time)
    
    # Resultados
    avg_wait = sum(wait_times)/len(wait_times) if wait_times else 0
    
    print("\nResultados finales:")
    print(f"a) Probabilidad teórica cola vacía (P0): {1 - lambda_/mu:.4f}")
    print(f"b) Probabilidad teórica 42 clientes (P42): {(1-lambda_/mu)*(lambda_/mu)**42:.2e}")
    print(f"c) Tiempo promedio teórico de espera (W): {1/(mu - lambda_):.4f}")
    print(f"\nResultados de la simulación:")
    print(f"Número total de clientes atendidos: {num_customers}")
    print(f"Tiempo promedio de espera simulado: {avg_wait:.4f}")

# Ejecutar la simulación
mm1_simulation()