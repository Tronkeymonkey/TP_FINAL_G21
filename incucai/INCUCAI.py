from pacientes.Receptores import Receptores
from pacientes.Donantes import Donantes
from cirujanos.Cirujanos import Cirujanos
from centro_salud.Centro_Salud import CentroSalud
from organos.Organos import *
from datetime import datetime
class INCUCAI:

    def __init__(self, centros = []):
        """
        Inicializa una instancia de INCUCAI con una lista de centros de salud proporcionada.
        Además, crea listas vacías para almacenar receptores y donantes.
        """
        self.lista_receptores: list[Receptores] = [] #listas para almacenar los receptores y donantes (vacias) 
        self.lista_donantes: list[Donantes] = []
        self.centros_salud: list[CentroSalud] = centros
    
    def clasificar_centros_salud(self):
        
        """
        Procesa todos los pacientes registrados en los centros de salud.
        Clasifica a cada paciente como receptor o donante, los agrega a sus respectivas listas
        y gestiona todo el proceso de búsqueda de compatibilidad, asignación de vehículo,
        y ejecución de la cirugía por parte del centro de salud.
        """
        for centro in self.centros_salud: #por cada lista de centro de salud, se verifica si los pacientes son receptor o donante y se agrega a la lista correspondiente
            for paciente in centro.lista_pacientes:
                if isinstance(paciente, Receptores): #verificar si es receptor o donante en base a la clase
                    self.lista_receptores.append(paciente)
                    if self.buscar_compatibilidad_receptor_a_donante(paciente): #busca compatibilidad entre el receptor y los donantes
                        tiempo = centro.asignar_y_mandar_vehiculo(paciente)
                        centro.asignar_cirujano_y_operar(paciente, tiempo)

                elif isinstance(paciente, Donantes):
                    self.lista_donantes.append(paciente)
                    receptor_encontrado = self.buscar_compatibilidad_donante_a_receptor(paciente)
                    if receptor_encontrado is not None:
                        tiempo = centro.asignar_y_mandar_vehiculo(receptor_encontrado)
                        if tiempo is not None:
                            centro.asignar_cirujano_y_operar(receptor_encontrado, tiempo)
                    # tiempo = centro.asignar_y_mandar_vehiculo(receptor_encontrado) #busca compatibilidad entre el donante y los receptores y manda el vehiculo
                    # centro.asignar_cirujano_y_operar(receptor_encontrado, tiempo)

                else:
                    raise ValueError("El paciente debe ser un receptor o un donante.")

    def buscar_compatibilidad_receptor_a_donante(self, receptor: Receptores):  # Verificar si el órgano que el receptor necesita está en la lista de órganos que el donante puede donar    
            """
            Busca donantes compatibles para un receptor dado.
            Si el receptor está en estado 'inestable', se le da prioridad.
            Si encuentra un donante con el órgano requerido y tipo de sangre compatible,
            transfiere el órgano al receptor, registra la fecha de ablación y lo elimina
            de la lista de órganos del donante.
            """

            ''''
            if receptor.estado.lower() == "inestable": #primero verifico si el receptor esta inestable para darle prioridad al trasplante, es indistinto el tiempo de espera, la situacion es critica y todos necesitan de la operacion
                for donante in self.lista_donantes:
                        if receptor.organo_a_recibir == donante.organos_a_donar and receptor.Tsangre == donante.Tsangre:
                            for i in range(len(donante.organos_a_donar)): #entro a la lista de organos a donar del donante
                                donante.organos_a_donar[i].fecha_ablacion = datetime.now() #seteamos la fecha de ablacion del organo en "0"
                                receptor.organos_a_disposicion.append(donante.organos_a_donar)  #coloco el organo del donante en la lista de organos a disposicion del receptor
                                donante.organos_a_donar.remove(donante.organos_a_donar[i]) #el donante no puede donar el organo que ya dono
                                return True

            else: #receptor.estado.lower() == "estable": #misma logica que el anterior, pero para los receptores estables
                for donante in self.lista_donantes:
                    if receptor.organo_a_recibir == donante.organos_a_donar and receptor.Tsangre == donante.Tsangre:
                        for i in range(len(donante.organos_a_donar)):
                            donante.organos_a_donar[i].fecha_ablacion = datetime.now() 
                            receptor.organos_a_disposicion.append(donante.organos_a_donar)
                            donante.organos_a_donar.remove(donante.organos_a_donar[i]) 
                            return True
            return False
            '''
            # FIX: Usar estado por defecto si no está definido
            estado_receptor = getattr(receptor, 'estado', 'estable').lower()

            if estado_receptor == "inestable":
                for donante in self.lista_donantes:
                    # FIX: Comparar correctamente con los órganos del donante
                    for organo in donante.organos_a_donar:
                        if (receptor.organo_a_recibir.lower() == organo.tipo_de_organo.lower() and
                                receptor.Tsangre == donante.Tsangre):
                            organo.fecha_ablacion = datetime.now()
                            receptor.organos_a_disposicion.append(organo)
                            donante.organos_a_donar.remove(organo)
                            return True

            else:  # estado estable
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
            #verifico si el donante es compatible con el receptor
            #logica exactamente igual a la del receptor, pero sin incluir la prioridad del estado
            """
            Busca receptores compatibles para un donante dado.
            Compara los órganos disponibles del donante con lo que necesitan los receptores
            y también verifica el tipo de sangre.
            Si hay compatibilidad, transfiere los órganos, registra la fecha de ablación,
            los elimina de la lista del donante y remueve al donante si ya no tiene órganos.
            Retorna el receptor compatible encontrado.
            """
            '''' 
            for receptor in self.lista_receptores:
                for i in donante.organos_a_donar:
                    if i.tipo_de_organo == receptor.organo_a_recibir and donante.Tsangre == receptor.Tsangre:
                        i.fecha_ablacion = datetime.now()
                        receptor.organos_a_disposicion.append(donante.organos_a_donar)                   
                        donante.organos_a_donar.remove(i)
                    if donante.organos_a_donar == []: 
                        self.lista_donantes.remove(donante) #si el donante se queda sin organos, se va de la lista de donantes
                        return receptor #retorna el receptor que coincide con el donante, esta hecho asi a diferencia de la otra funcion de compatibilidad, ya que la funcion del Centro de Salud recibe como argumento al receptor
            '''
            for receptor in self.lista_receptores:
                # FIX: Iterar sobre una copia de la lista para evitar modificar durante iteración
                for organo in donante.organos_a_donar[:]:
                    if (organo.tipo_de_organo.lower() == receptor.organo_a_recibir.lower() and
                            donante.Tsangre == receptor.Tsangre):
                        organo.fecha_ablacion = datetime.now()
                        receptor.organos_a_disposicion.append(organo)
                        donante.organos_a_donar.remove(organo)

                        # Si el donante se queda sin órganos, removerlo de la lista
                        if not donante.organos_a_donar:
                            if donante in self.lista_donantes:
                                self.lista_donantes.remove(donante)

                        return receptor

                # FIX: Retornar None explícitamente si no se encuentra compatibilidad
            return None

