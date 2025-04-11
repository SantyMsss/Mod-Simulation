import random
import statistics
import matplotlib.pyplot as plt
from math import inf as Infinity

class MM1QueueSimulator:
    def __init__(self, arrival_rate, service_rate, simulation_time):
        """
        Inicializa el simulador de cola M/M/1
        
        Parámetros:
        - arrival_rate (λ): Tasa media de llegadas (clientes/unidad de tiempo)
        - service_rate (μ): Tasa media de servicio (clientes/unidad de tiempo)
        - simulation_time: Tiempo total de simulación
        """
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.simulation_time = simulation_time
        
        # Variables de estado
        self.clock = 0.0
        self.num_in_system = 0
        
        # Programación de eventos
        self.next_arrival = self.generate_interarrival()
        self.next_departure = Infinity
        
        # Estadísticas
        self.arrival_times = []
        self.departure_times = []
        self.queue_lengths = []
        self.event_times = [0.0]
        
        # Para cálculo de áreas
        self.area_under_q = 0.0
        self.area_under_system = 0.0
        self.last_event_time = 0.0
        
    def generate_interarrival(self):
        """Genera tiempo entre llegadas exponencial"""
        return random.expovariate(self.arrival_rate)
    
    def generate_service(self):
        """Genera tiempo de servicio exponencial"""
        return random.expovariate(self.service_rate)
    
    def run_simulation(self):
        """Ejecuta la simulación"""
        while self.clock <= self.simulation_time:
            # Determinar el próximo evento
            if self.next_arrival < self.next_departure:
                self.handle_arrival()
            else:
                self.handle_departure()
            
            # Actualizar áreas para métricas
            time_since_last_event = self.clock - self.last_event_time
            self.area_under_system += self.num_in_system * time_since_last_event
            self.area_under_q += max(0, self.num_in_system - 1) * time_since_last_event
            self.last_event_time = self.clock
            
            # Registrar estado actual
            self.queue_lengths.append(self.num_in_system)
            self.event_times.append(self.clock)
    
    def handle_arrival(self):
        """Procesa un evento de llegada"""
        self.clock = self.next_arrival
        self.arrival_times.append(self.clock)
        self.num_in_system += 1
        
        # Si es el único cliente, programar su salida
        if self.num_in_system == 1:
            self.next_departure = self.clock + self.generate_service()
        
        # Programar próxima llegada
        self.next_arrival = self.clock + self.generate_interarrival()
    
    def handle_departure(self):
        """Procesa un evento de salida"""
        self.clock = self.next_departure
        self.departure_times.append(self.clock)
        self.num_in_system -= 1
        
        # Si quedan clientes, programar próxima salida
        if self.num_in_system > 0:
            self.next_departure = self.clock + self.generate_service()
        else:
            self.next_departure = Infinity
    
    def calculate_metrics(self):
        """Calcula métricas de rendimiento"""
        # Verificar que hayan clientes que completaron el servicio
        if not self.departure_times:
            return {
                'avg_system_customers': 0,
                'avg_queue_customers': 0,
                'avg_system_time': 0,
                'avg_queue_time': 0,
                'server_utilization': 0
            }
        
        # Tiempos en el sistema (W)
        system_times = [d - a for a, d in zip(self.arrival_times, self.departure_times)]
        avg_system_time = statistics.mean(system_times) if system_times else 0
        
        # Tiempos en cola (Wq) = Tiempo en sistema - tiempo de servicio
        avg_queue_time = avg_system_time - (1 / self.service_rate)
        
        # Número promedio de clientes en sistema (L) y en cola (Lq)
        avg_system_customers = self.area_under_system / self.clock
        avg_queue_customers = self.area_under_q / self.clock
        
        # Utilización del servidor (ρ)
        server_utilization = 1 - (self.area_under_system - self.area_under_q) / self.clock
        
        return {
            'avg_system_customers': avg_system_customers,
            'avg_queue_customers': avg_queue_customers,
            'avg_system_time': avg_system_time,
            'avg_queue_time': avg_queue_time,
            'server_utilization': server_utilization
        }
    
    def plot_results(self):
        """Grafica la evolución del número de clientes en el sistema"""
        plt.figure(figsize=(12, 6))
        plt.step(self.event_times[:-1], self.queue_lengths, where='post')
        plt.xlabel('Tiempo de simulación')
        plt.ylabel('Número de clientes en el sistema')
        plt.title(f'Evolución del sistema M/M/1 (λ={self.arrival_rate}, μ={self.service_rate})')
        plt.grid(True)
        plt.show()

# Parámetros de simulación
arrival_rate = 1.3  # λ (clientes/tiempo)
service_rate = 2.0   # μ (clientes/tiempo)
simulation_time = 1000  # Tiempo total de simulación

# Crear y ejecutar simulación
simulator = MM1QueueSimulator(arrival_rate, service_rate, simulation_time)
simulator.run_simulation()

# Calcular y mostrar métricas
metrics = simulator.calculate_metrics()
print("\nMétricas de rendimiento:")
print(f"Número promedio de clientes en el sistema (L): {metrics['avg_system_customers']:.4f}")
print(f"Número promedio de clientes en la cola (Lq): {metrics['avg_queue_customers']:.4f}")
print(f"Tiempo promedio en el sistema (W): {metrics['avg_system_time']:.4f}")
print(f"Tiempo promedio en la cola (Wq): {metrics['avg_queue_time']:.4f}")
print(f"Utilización del servidor (ρ): {metrics['server_utilization']:.4f}")

# Mostrar evolución del sistema
simulator.plot_results()