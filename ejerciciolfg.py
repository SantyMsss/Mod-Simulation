def lfg_multiplication(modulo, j, k, initial_values, num_cycles):
    sequence = initial_values.copy()
    cycle_length = 0
    cycle_start = 0
    
    while True:
        next_value = (sequence[-j] * sequence[-k]) % modulo
        sequence.append(next_value)
        
        # Detectar el inicio de un ciclo
        if sequence[-k:] == sequence[:k]:
            cycle_length = len(sequence) - k
            cycle_start = k
            break
    
    # Imprimir dos ciclos completos
    full_sequence = sequence[cycle_start:cycle_start + 2 * cycle_length]
    print("Secuencia completa para dos ciclos:", full_sequence)
    return full_sequence

# Parámetros del LFG
modulo = 7
j = 1
k = 2
initial_values = [3, 2]
num_cycles = 2

# Generar y imprimir la secuencia
sequence = lfg_multiplication(modulo, j, k, initial_values, num_cycles)