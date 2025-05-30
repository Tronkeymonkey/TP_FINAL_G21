from pacientes.Receptores import Receptores
from pacientes.Donantes import Donantes
from cirujanos.Cirujanos import Cirujanos
from centro_salud.Centro_Salud import CentroSalud
from organos.Organos import *
from datetime import datetime
class INCUCAI:

    def __init__(self, centros = []):
        """
    Inicializa una instancia de INCUCAI.

    params:
        - centros: Una lista de objetos CentroSalud que representa los centros de salud asociados.
    
    precon (opcional):
        - centros debe ser una lista (puede estar vacía) cuyos elementos sean instancias de CentroSalud.
    
    returns:
        None. Este método inicializa los atributos de la instancia.
        """
        self.lista_receptores: list[Receptores] = [] #listas para almacenar los receptores y donantes (vacias) 
        self.lista_donantes: list[Donantes] = []
        self.centros_salud: list[CentroSalud] = centros
    
    def clasificar_centros_salud(self):
        
        """
        INCUCAI procesa todos los pacientes registrados en los centros de salud.
        Clasifica a cada paciente como receptor o donante, los agrega a sus respectivas listas
        y gestiona todo el proceso de búsqueda de compatibilidad, asignación de vehículo,
        y ejecución de la cirugía por parte del centro de salud.
        """
        for centro in self.centros_salud: #por cada lista de centro de salud, se verifica si los pacientes son receptor o donante y se agrega a la lista correspondiente
            for paciente in centro.lista_pacientes:
                if isinstance(paciente, Receptores): #verificar si es receptor o donante en base a la clase
                    self.lista_receptores.append(paciente)
                    if self.buscar_compatibilidad_receptor_a_donante(paciente): 
                        tiempo = centro.asignar_y_mandar_vehiculo(paciente) 
                        if tiempo is not None:
                            centro.asignar_cirujano_y_operar(paciente, tiempo)

                elif isinstance(paciente, Donantes): #misma logica que los receptores, pero aplicado a los donantes
                    self.lista_donantes.append(paciente)
                    receptor_encontrado = self.buscar_compatibilidad_donante_a_receptor(paciente)  #como los organos del donante son los que van al receptor, esta funcion devuelve dicho receptor encontrado que necesita del organo
                    if receptor_encontrado is not None: #si encuentra un receptor, entra a las demas funciones
                        tiempo = centro.asignar_y_mandar_vehiculo(receptor_encontrado)
                        if tiempo is not None:
                            centro.asignar_cirujano_y_operar(receptor_encontrado, tiempo)

                else:
                    raise ValueError("El paciente debe ser un receptor o un donante.")

    def buscar_compatibilidad_receptor_a_donante(self, receptor: Receptores):  # Verificar si el órgano que el receptor necesita está en la lista de órganos que el donante puede donar    
            """
            Busca donantes compatibles para un receptor dado y realiza la transferencia del órgano si es posible.

    params:
        - receptor: Un objeto Receptores que contiene la información del receptor que necesita un órgano.
    
    precon (opcional):
        - receptor debe tener los atributos 'organo_a_recibir' (str) y 'Tsangre' (tipo de sangre).
        - Los donantes en self.lista_donantes deben tener una lista 'organos_a_donar' con órganos disponibles.
    
    returns:
        - True si se encontró un donante compatible y se realizó la transferencia del órgano.
        - False si no se encontró ningún donante compatible.
            """
            #Usar estado por defecto si no está definido
            estado_receptor = getattr(receptor, 'estado', 'estable').lower()

            if estado_receptor == "inestable": #la jerarquia de busqueda de pacientes se da primero en inestables, si bien las listas se ordenan ademas de mas joven a mas viejo, es evidente que primero tiene que haber un match mas alla de la edad
                for donante in self.lista_donantes:
                    #Comparar correctamente con los órganos del donante
                    for organo in donante.organos_a_donar:
                        if (receptor.organo_a_recibir.lower() == organo.tipo_de_organo.lower() and
                                receptor.Tsangre == donante.Tsangre):
                            organo.fecha_ablacion = datetime.now() # setea en "0hs" la fecha de ablacion del organo
                            receptor.organos_a_disposicion.append(organo) 
                            donante.organos_a_donar.remove(organo) 
                            return True 

            else:  
                for donante in self.lista_donantes:
                    for organo in donante.organos_a_donar[:]:  # Crear copia para iterar seguro
                        if (receptor.organo_a_recibir.lower() == organo.tipo_de_organo.lower() and
                                receptor.Tsangre == donante.Tsangre):
                            organo.fecha_ablacion = datetime.now()
                            receptor.organos_a_disposicion.append(organo)
                            donante.organos_a_donar.remove(organo)
                            return True

            return False

    def buscar_compatibilidad_donante_a_receptor(self, donante: Donantes) -> Receptores:
            """
            Busca receptores compatibles para un donante dado y realiza la transferencia del órgano si es posible.

    params:
        - donante: Un objeto Donantes que contiene la información del donante y los órganos disponibles para donar.

    precon (opcional):
        - donante debe tener una lista 'organos_a_donar' con órganos disponibles.
        - Los receptores en self.lista_receptores deben tener los atributos 'organo_a_recibir' (str) y 'Tsangre'.

    returns:
        - El objeto Receptores compatible que recibió un órgano del donante.
        - None si no se encontró ningún receptor compatible.
            """
            #segun la consigna, el matcheo es distinto si ingresa un receptor o un donante
            for receptor in self.lista_receptores:
                #Iterar sobre una copia de la lista para evitar modificar durante iteración
                for organo in donante.organos_a_donar[:]:
                    if (organo.tipo_de_organo.lower().__eq__(receptor.organo_a_recibir.lower()) and
                            donante.Tsangre.__eq__(receptor.Tsangre)): #metodo magico eq (==)
                        organo.fecha_ablacion = datetime.now() 
                        receptor.organos_a_disposicion.append(organo)
                        donante.organos_a_donar.remove(organo)

                        if not donante.organos_a_donar:
                            if donante in self.lista_donantes:
                                self.lista_donantes.remove(donante)

                        return receptor

            return None

