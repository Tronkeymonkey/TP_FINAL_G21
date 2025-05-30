from abc import ABC, abstractmethod #uso clase abstracta

class Vehiculos(ABC):
    def __init__(self, velocidad_viajes, identificador):
        """
        Inicializa un vehículo con su velocidad de viaje y un identificador único.

        params:
            - velocidad_viajes: Velocidad a la que puede desplazarse el vehículo (por ejemplo, km/h).
            - identificador: Identificador único del vehículo (patente, nombre de helicóptero o código de avión).

        precon (opcional):
            - velocidad_viajes debe ser un número positivo.
            - identificador debe ser una cadena no vacía.

        returns:
            None. Inicializa una instancia de Vehiculos con los atributos proporcionados.
        """
        self.velocidad_viajes = velocidad_viajes
        self.identificador = identificador #El número de patente de una ambulancia. Un nombre de helicóptero ("HELI01", "HELI02") ,Código de un avión de transporte.
        self.registro_viajes = [] #lista donde guardo los datos de cada viaje que hace el vehiculo
        self.disponibilidad = "Disponible"
        
    @abstractmethod    
    def despachar(self, distancia, nivel_trafico=3): #abstract method que se implementa o se sobreescribe por las subclases
        """
        Calcula y registra el tiempo de viaje para despachar el vehículo a una distancia dada.

    params:
        - distancia: La distancia que debe recorrer el vehículo (en kilómetros).
        - nivel_trafico: Nivel de tráfico en la ruta, afecta el tiempo de viaje (por defecto 3).

    precon (opcional):
        - distancia debe ser un número positivo.
        - nivel_trafico debe ser un entero entre 1 (bajo) y 5 (alto).

    returns:
        None. Debe registrar internamente el viaje realizado y actualizar el estado del vehículo.
        """
        pass 
    
    def _despacho_default(self, distancia, nivel_trafico): # creo un metodo protegido por default para avion y helicoptero (reutilizan el comportamiento sin sobreescribir)
        """
        Método protegido que calcula y registra el tiempo de viaje para despacho estándar.

    params:
        - distancia: Distancia a recorrer por el vehículo (en kilómetros).
        - nivel_trafico: Nivel de tráfico en la ruta que podría afectar el viaje.

    precon (opcional):
        - distancia debe ser un valor positivo.
        - nivel_trafico debe ser un entero válido representando el nivel de tráfico.

    returns:
        Tiempo estimado de viaje calculado como distancia dividida por la velocidad del vehículo.
        """
        tiempo = distancia.__truediv__(self.velocidad_viajes) #metodo magico truediv (/)
        self.registro_viajes.append({
        'distancia': distancia,
        'nivel_trafico': nivel_trafico,
        'tiempo': tiempo
    })
        return tiempo
    
    def __str__(self): #metodo magico que ayuda al orden del codigo si quiero imprimirlo: print(vehiculo1) tengo que crear un vehiculo
        """
        Método mágico que devuelve una representación legible del vehículo.
        Sirve para imprimir objetos de esta clase de forma clara usando `print(vehiculo)`. 
        Retorna un string con el identificador y la velocidad del vehículo.
        """
        return f"Vehículo {self.identificador} - Velocidad: {self.velocidad_viajes} km/h" 