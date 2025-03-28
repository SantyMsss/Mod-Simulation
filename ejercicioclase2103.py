import numpy as np
import matplotlib.pyplot as plt

# Transformada inversa para el caso A: Distribución A
def F_inv_a(u, a=1, b=3):
    mid = (a + b) / 2
    return a + np.sqrt(u * (b - a) ** 2 / 2) if u < 0.5 else b - np.sqrt((1 - u) * (b - a) ** 2 / 2)

# CDF para la distribución triangular
def CDF_a(x, a=1, b=3):
    mid = (a + b) / 2
    if x < a:
        return 0
    elif x < mid:
        return ((x - a)**2) / ((b - a)**2 / 2)
    elif x < b:
        return 1 - ((b - x)**2) / ((b - a)**2 / 2)
    else:
        return 1

# Transformada inversa para el caso B: Distribución Beta
def F_inv_b(u, b):
    return 1 - (1 - u) ** (1 / (b + 1))

# CDF para la distribución Beta
def CDF_b(x, b):
    if x < 0:
        return 0
    elif x > 1:
        return 1
    else:
        return 1 - (1 - x)**(b + 1)

# Transformada inversa para el caso C: Distribución Trapezoidal ajustada
def F_inv_c(u):
    return np.sqrt(200 * u) if u < 0.5 else 20 - np.sqrt(200 * (1 - u))

# CDF para la distribución trapezoidal
def CDF_c(x):
    if x < 0:
        return 0
    elif x < 10:
        return x**2 / 200
    elif x < 20:
        return 1 - ((20 - x)**2 / 200)
    else:
        return 1

# Función para generar el histograma, PDF y CDF acumulada experimental
def generar_histograma(distribucion, b_param=None):
    num_samples = 1000000
    uniform_samples = np.random.random(num_samples)

    if distribucion == "A":
        data = np.array([F_inv_a(u) for u in uniform_samples])
        title = "Distribución Triangular"
        x_vals = np.linspace(1, 3, 1000)
        pdf_vals = np.where(x_vals < 2, (4 / (3 - 1) ** 2) * (x_vals - 1), (4 / (3 - 1) ** 2) * (3 - x_vals))
        cdf_vals = [CDF_a(x) for x in x_vals]
    elif distribucion == "B":
        data = np.array([F_inv_b(u, b_param) for u in uniform_samples])
        title = f"Distribución Beta (b={b_param})"
        x_vals = np.linspace(0, 1, 1000)
        pdf_vals = (b_param + 1) * (1 - x_vals) ** b_param
        cdf_vals = [CDF_b(x, b_param) for x in x_vals]
    elif distribucion == "C":
        data = np.array([F_inv_c(u) for u in uniform_samples])
        title = "Distribución Trapezoidal"
        x_vals = np.linspace(0, 20, 1000)
        pdf_vals = np.where(x_vals < 10, x_vals / 100, (20 - x_vals) / 100)
        cdf_vals = [CDF_c(x) for x in x_vals]
    else:
        print("❌ Opción no válida. Intenta de nuevo.")
        return

    # Crear histograma de frecuencia relativa
    hist, bin_edges = np.histogram(data, bins=100, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2  # Obtener los puntos centrales

    # Cálculo de la CDF acumulada experimental
    fr_acumulada = np.cumsum(hist) * (bin_edges[1] - bin_edges[0])

    # Gráfico 1: Histograma y PDF
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    axs[0].hist(data, bins=100, density=True, alpha=0.75, color='blue', label="Histograma de muestras")
    axs[0].plot(x_vals, pdf_vals, 'r-', label="Función de densidad teórica (PDF)")
    axs[0].set_title(f'Histograma y PDF - {title}')
    axs[0].set_xlabel('Valor')
    axs[0].set_ylabel('Densidad')
    axs[0].legend()

    # Gráfico 2: CDF acumulada experimental
    axs[1].bar(bin_centers, fr_acumulada, width=(bin_edges[1] - bin_edges[0]), alpha=0.6, color='purple', label="CDF experimental acumulada")
    axs[1].plot(x_vals, cdf_vals, 'g-', label="CDF teórica")
    axs[1].set_title(f'CDF acumulada experimental - {title}')
    axs[1].set_xlabel('Valor')
    axs[1].set_ylabel('Probabilidad acumulada')
    axs[1].legend()

    # Mostrar gráficos en la misma ventana
    plt.tight_layout()
    plt.show()

# Menú interactivo para seleccionar la distribución
def menu():
    while True:
        print("\nSELECCIONA UNA DISTRIBUCIÓN PARA GENERAR NÚMEROS ALEATORIOS:")
        print("1 - Caso A (Distribución Triangular)")
        print("2 - Caso B (Distribución Beta, dos valores de b)")
        print("3 - Caso C (Distribución Trapezoidal)")
        print("0 - Salir")
        
        opcion = input("Ingresa una opción (1/2/3/0): ").strip()

        if opcion == "1":
            generar_histograma("A")
        elif opcion == "2":
            print("\nGenerando gráfico para b=5:")
            generar_histograma("B", b_param=5)
            print("\nGenerando gráfico para b=2:")
            generar_histograma("B", b_param=2)
        elif opcion == "3":
            generar_histograma("C")
        elif opcion == "0":
            print("👋 Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Entrada inválida. Inténtalo de nuevo.")

if __name__ == "__main__":
    menu()
