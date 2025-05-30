from vehiculos.Vehiculos import *
from typing import override


class Helicoptero(Vehiculos):
    
    
    def __init__(self, velocidad_viajes, identificador):
        super().__init__(velocidad_viajes, identificador) 
        """
        Inicializa una instancia de Helicoptero con velocidad de viaje e identificador único.

        params:
            - velocidad_viajes: Velocidad a la que vuela el helicóptero (km/h).
            - identificador: Código único del helicóptero.

        returns:
            None. Inicializa la instancia heredando de Vehiculos.
        """
        
    @override
    def despachar(self, distancia, nivel_trafico=None):
        """
        Calcula y registra el tiempo de despacho para el helicóptero a una distancia dada.

        params:
            - distancia: Distancia que debe recorrer el helicóptero (km).
            - nivel_trafico: Parámetro opcional para compatibilidad, no afecta el cálculo.

        precon (opcional):
            - distancia debe ser un valor positivo.
            - nivel_trafico puede ser None o un entero, pero se ignora.

        returns:
            Tiempo estimado del viaje calculado por el método protegido _despacho_default().
        """
        self.disponibilidad = "Disponible"
        return self._despacho_default(distancia, nivel_trafico) #metodo protegido default para helicpotero  
        
    