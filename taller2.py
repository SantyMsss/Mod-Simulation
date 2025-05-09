import numpy as np
import matplotlib.pyplot as plt
import queue

# --- PUNTO 1: Transformada Inversa y Gráficos ---

# Transformada inversa para f(x) = (3/2) * sqrt(x)
def F_inv(u):
    return u ** (2 / 3)

# PDF teórica
def pdf_teorica(x):
    return (3 / 2) * np.sqrt(x)

# CDF teórica
def cdf_teorica(x):
    return x ** (3 / 2)

# Generación y visualización
def generar_histograma():
    n = 1000000
    muestras = F_inv(np.random.rand(n))

    # Histograma con 500 bins
    hist, bins = np.histogram(muestras, bins=500, density=True)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    frec_acumulada = np.cumsum(hist) * (bins[1] - bins[0])

    x_vals = np.linspace(0, 1, 1000)
    pdf_vals = pdf_teorica(x_vals)
    cdf_vals = cdf_teorica(x_vals)

    # Gráficos
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Histograma + PDF
    axs[0].hist(muestras, bins=500, density=True, alpha=0.6, label="Histograma")
    axs[0].plot(x_vals, pdf_vals, 'r-', label="PDF teórica")
    axs[0].set_title("Histograma y PDF")
    axs[0].legend()

    # CDF
    axs[1].bar(bin_centers, frec_acumulada, width=(bins[1] - bins[0]), alpha=0.6, label="CDF experimental")
    axs[1].plot(x_vals, cdf_vals, 'g-', label="CDF teórica")
    axs[1].set_title("CDF acumulada")
    axs[1].legend()

    plt.tight_layout()
    plt.show()

# --- PUNTO 2: Sistema M/M/1 ---

# Parámetros del sistema M/M/1
lambd = 0.4
mu = 0.8
rho = lambd / mu

# Funciones para incisos a, b y c
def probabilidad_cola_vacia():
    return 1 - rho

def probabilidad_n_clientes(n):
    return (1 - rho) * (rho ** n)

def tiempo_promedio_espera():
    return 1 / (mu - lambd)

# Simulación M/M/1
def simular_mm1(tiempo_simulacion=2000):
    reloj = 0
    cola = queue.Queue()
    tiempos_espera = []

    tiempo_llegada = np.random.exponential(1 / lambd)
    tiempo_siguiente_servicio = None

    print(f"{'Tiempo':>7} | {'Cola':>4} | {'Llegada':>8} | {'Salida':>8}")
    print("-" * 40)

    while reloj < tiempo_simulacion:
        if tiempo_siguiente_servicio is None or tiempo_llegada <= tiempo_siguiente_servicio:
            reloj = tiempo_llegada
            cola.put(reloj)
            tiempo_llegada += np.random.exponential(1 / lambd)

            if cola.qsize() == 1:
                tiempo_siguiente_servicio = reloj + np.random.exponential(1 / mu)
        else:
            reloj = tiempo_siguiente_servicio
            llegada = cola.get()
            espera = reloj - llegada
            tiempos_espera.append(espera)

            if cola.qsize() > 0:
                tiempo_siguiente_servicio = reloj + np.random.exponential(1 / mu)
            else:
                tiempo_siguiente_servicio = None

        print(f"{reloj:7.2f} | {cola.qsize():4} | {tiempo_llegada:8.2f} | {tiempo_siguiente_servicio if tiempo_siguiente_servicio else 0:8.2f}")

    promedio_espera = np.mean(tiempos_espera) if tiempos_espera else 0
    print(f"\nTiempo promedio de espera (simulado): {promedio_espera:.4f}")

    # Se ha eliminado el histograma de tiempos de espera que estaba aquí

# Submenú Punto 2
def menu_punto2():
    while True:
        print("\n--- Sistema de Colas M/M/1 ---")
        print("a. Probabilidad de que la cola esté vacía (P0)")
        print("b. Probabilidad de que haya 42 clientes (P42)")
        print("c. Tiempo promedio de espera (W)")
        print("d. Simular sistema M/M/1")
        print("e. Volver al menú principal")

        opcion = input("Seleccione una opción: ").lower()

        if opcion == 'a':
            print(f"P0 = {probabilidad_cola_vacia():.4f}")
        elif opcion == 'b':
            prob = probabilidad_n_clientes(42)
            print(f"P42 = {prob:.2e}  (notación científica)")
        elif opcion == 'c':
            print(f"W = {tiempo_promedio_espera():.4f} unidades de tiempo")
        elif opcion == 'd':
            simular_mm1()
        elif opcion == 'e':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Menú principal
def menu_principal():
    while True:
        print("\n======= MENÚ PRINCIPAL =======")
        print("1. Punto 1: Transformada inversa y gráficos")
        print("2. Punto 2: Sistema de colas M/M/1")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            generar_histograma()
        elif opcion == '2':
            menu_punto2()
        elif opcion == '3':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

# Ejecutar el menú principal
if __name__ == "__main__":
    menu_principal()