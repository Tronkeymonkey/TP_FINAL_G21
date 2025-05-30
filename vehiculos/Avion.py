from vehiculos.Vehiculos import * 
from typing import override


class Avion(Vehiculos):
    
    
    def __init__(self, velocidad_viajes, identificador):
        """
        Inicializa una instancia de Avion con velocidad de viaje e identificador único.

        params:
            - velocidad_viajes: Velocidad a la que vuela el avión (por ejemplo, km/h).
            - identificador: Código único del avión.

        returns:
            None. Inicializa una instancia de Avion con los atributos heredados de Vehiculos.
        """
        super().__init__(velocidad_viajes, identificador) 
     
    @override  #sobreescribo el metodo de mi clase madre
    def despachar(self, distancia, nivel_trafico=None):
        """
        Calcula y registra el tiempo de despacho para el avión a una distancia dada.

        params:
            - distancia: Distancia que debe recorrer el avión (en kilómetros).
            - nivel_trafico: Parámetro opcional para compatibilidad, no afecta el cálculo.

        precon (opcional):
            - distancia debe ser un número positivo.
            - nivel_trafico puede ser None o un entero, pero se ignora.

        returns:
            Tiempo estimado del viaje calculado por el método protegido _despacho_default().
        """
        self.disponibilidad = "Disponible"
        return self._despacho_default(distancia, nivel_trafico) 
    