import random
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# PRESENTACION DEL PARCIAL 1 DE MODELAMIENTO Y SIMULACION
# Programadores:
# Santiago Martinez Serna - 230222014
# Laura Sofia Toro Garcia - 230222021
# Santiago Alejandro Santacruz - 230222033

# Inicio de lógica pregunta 1

def simulate_dice_rolls(num_rolls=100000):
    results = [random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6) for _ in range(num_rolls)]
    return results

def theoretical_probabilities():
    outcomes = Counter()
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            for d3 in range(1, 7):
                outcomes[d1 + d2 + d3] += 1
    
    total_possibilities = 6 * 6 * 6  # 216
    probabilities = {suma: count / total_possibilities for suma, count in outcomes.items()}
    return probabilities

def plot_results(simulated, theoretical):
    simulated_counts = Counter(simulated)
    simulated_probs = {suma: count / len(simulated) for suma, count in simulated_counts.items()}
    
    sums = sorted(set(list(simulated_probs.keys()) + list(theoretical.keys())))
    
    sim_values = [simulated_probs.get(s, 0) for s in sums]
    theo_values = [theoretical.get(s, 0) for s in sums]
    
    x = np.arange(len(sums))
    width = 0.4
    
    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, sim_values, width=width, label='Simulación', color='blue', alpha=0.6)
    plt.bar(x + width/2, theo_values, width=width, label='Teórico', color='red', alpha=0.6)
    plt.xticks(x, sums)
    plt.xlabel('Suma de los 3 dados')
    plt.ylabel('Probabilidad')
    plt.title('Distribución de la Suma de Tres Dados')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def question1():
    num_simulations = 100000
    simulated_results = simulate_dice_rolls(num_simulations)
    theoretical_results = theoretical_probabilities()

    # Calcular probabilidades simuladas
    simulated_counts = Counter(simulated_results)
    simulated_probs = {suma: count / num_simulations for suma, count in simulated_counts.items()}

    # Mostrar primeros 50 resultados simulados
    print("Resultados simulados (primeros 50 valores):", simulated_results[:50])

    # Mostrar comparación de probabilidades teóricas y simuladas
    print("\nComparación de Probabilidades:")
    print(f"{'Suma':<10}{'Teórico':<15}{'Simulación'}")
    print("-" * 40)

    for suma in sorted(set(theoretical_results.keys()).union(simulated_probs.keys())):
        prob_teorica = theoretical_results.get(suma, 0)
        prob_simulada = simulated_probs.get(suma, 0)
        print(f"{suma:<10}{prob_teorica:<15.4f}{prob_simulada:.4f}")

    # Graficar los resultados
    plot_results(simulated_results, theoretical_results)


# Probabilidades teóricas de obtener dobles en los intentos 1, 2 o 3
def theoretical_doubles_probabilities():
    p = 6 / 36  # Probabilidad de obtener dobles en un intento (1/6)
    q = 1 - p   # Probabilidad de NO obtener dobles

    p1 = p  # Probabilidad en el primer intento
    p2 = q * p  # Probabilidad en el segundo intento
    p3 = q * q * p  # Probabilidad en el tercer intento

    return {1: p1, 2: p2, 3: p3}

# Simulación de obtener dobles en 3 intentos
def simulate_doubles_attempts(num_simulations=100000):
    success_counts = Counter()

    for _ in range(num_simulations):
        for attempt in range(1, 4):  # Solo 3 intentos
            if random.randint(1, 6) == random.randint(1, 6):  # Verifica si es un doble
                success_counts[attempt] += 1
                break  # Sale del bucle si obtiene dobles

    probabilities = {attempt: success_counts.get(attempt, 0) / num_simulations for attempt in range(1, 4)}

    return probabilities

# Comparación gráfica entre la teoría y la simulación
def plot_doubles_comparison(simulated_probs, theoretical_probs):
    attempts = [1, 2, 3]
    sim_values = [simulated_probs.get(attempt, 0) for attempt in attempts]
    theo_values = [theoretical_probs.get(attempt, 0) for attempt in attempts]

    x = np.arange(len(attempts))
    width = 0.4

    plt.figure(figsize=(8, 5))
    plt.bar(x - width/2, sim_values, width=width, label='Simulación', color='blue', alpha=0.7)
    plt.bar(x + width/2, theo_values, width=width, label='Teórico', color='red', alpha=0.7)

    plt.xticks(x, attempts)
    plt.xlabel("Intento en el que se logró dobles")
    plt.ylabel("Probabilidad")
    plt.title("Comparación de Probabilidad de Obtener Dobles en Tres Intentos")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def question2():
    print("Ejecutando simulación de obtención de dobles en tres intentos...")

    # Obtener datos de simulación y teoría
    simulated_probs = simulate_doubles_attempts()
    theoretical_probs = theoretical_doubles_probabilities()

    # Mostrar valores en la terminal
    print("\nProbabilidades Simuladas:")
    for attempt, prob in simulated_probs.items():
        print(f"Intento {attempt}: {prob:.4f}")

    print("\nProbabilidades Teóricas:")
    for attempt, prob in theoretical_probs.items():
        print(f"Intento {attempt}: {prob:.4f}")

    # Generar la gráfica comparativa
    plot_doubles_comparison(simulated_probs, theoretical_probs)

def mostrar_menu():
    print("Menú:")
    print("1. Simular y graficar la distribución de la suma de tres dados")
    print("2. Simular la probabilidad de obtener dobles en tres intentos")
    print("""
    Programadores: 
    Santiago Martinez Serna - 230222014 
    Laura Sofia Toro Garcia - 230222021
    Santiago Alejandro Santacruz - 230222033
    """)
    print("0. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")
        
        match opcion:
            case '1':
                question1()
            case '2':
                question2()
            case '0':
                print("Saliendo del programa...")
                break
            case _:
                print("Opción no válida, por favor intenta de nuevo.")

if __name__ == "__main__":
    main()
