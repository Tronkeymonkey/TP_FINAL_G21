from vehiculos.Vehiculos import * 
from typing import override
import random as rnd

class Auto(Vehiculos):

    def __init__(self, velocidad_viajes, identificador):
        super().__init__(velocidad_viajes, identificador)
        """
        Inicializa una instancia de Auto con velocidad de viaje e identificador único.

        params:
            - velocidad_viajes: Velocidad a la que se desplaza el auto (km/h).
            - identificador: Identificador único del auto.

        returns:
            None. Inicializa una instancia de Auto heredando de Vehiculos.
        """
           
        
    @override   
    def despachar(self, distancia): 
            """
            Simula el despacho del auto a una distancia dada calculando el tiempo de viaje.

        params:
            - distancia: Distancia a recorrer (en kilómetros).

        precon (opcional):
            - distancia debe ser un número positivo.
            - velocidad_viajes no debe ser cero para evitar división por cero.

        returns:
            Tiempo total estimado del viaje considerando un nivel de tráfico aleatorio.
            """

            nivel_trafico = rnd.randint(0, 3)
            
            if self.velocidad_viajes == 0:
                raise ValueError("La velocidad del vehículo no puede ser cero.")
            tiempo = (distancia / self.velocidad_viajes) +nivel_trafico
            self.registro_viajes.append({
                'distancia': distancia,
                'nivel_trafico': nivel_trafico,
                'tiempo': tiempo
            })
            # FIX: Usar = en lugar de ==
            self.disponibilidad = "Disponible"
            return tiempo
