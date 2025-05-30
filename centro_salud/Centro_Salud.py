from vehiculos.Helicoptero import *
from vehiculos.Avion import *
from vehiculos.Auto import *
from pacientes.Receptores import Receptores
from cirujanos.Cirujanos import Cirujanos
from pacientes.Donantes import Donantes
from pacientes.Pacientes import Pacientes
import random as rnd 

class CentroSalud:
    
    def __init__(self, nombre, direccion, telefono, partido, provincia, lista_cirujanos = [], lista_vehiculos= [], lista_pacientes= []):
        """
        Constructor de la clase CentroSalud.
        Inicializa un centro de salud con su nombre, dirección, ubicación (partido y provincia), 
        y listas vacías o dadas de cirujanos, vehículos y pacientes. Estas listas se utilizarán para asignar recursos
        en el proceso de trasplantes.
        """
        
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.partido = partido
        self.provincia = provincia
        self.lista_cirujanos: list[Cirujanos] = lista_cirujanos if isinstance(lista_cirujanos, list) else [lista_cirujanos] #lista de cirujanos
        self.lista_vehiculos: list[Auto | Helicoptero | Avion] = lista_vehiculos if isinstance(lista_vehiculos, list) else [lista_vehiculos] 
        self.lista_pacientes: list[Receptores | Donantes] = []
        self.pacientes_fallidos: list[Receptores] = []
        self.pacientes_exitosos: list[Receptores] = []

    def __str__(self):
        """
        Método mágico que devuelve una representación legible del centro de salud.
        Permite mostrar el nombre del centro cuando se convierte el objeto a string.
        """
        return f"{self.nombre}"
        
    def asignar_pacientes(self, pacientes: list[Receptores | Donantes]):
        """
        Asigna una lista de pacientes (donantes o receptores) al centro de salud.
        Además de agregar los pacientes a la lista interna, actualiza su centro, partido y provincia
        para reflejar que están vinculados con esta institución.
        """
        self.lista_pacientes.extend(pacientes)
        for paciente in pacientes:    
            paciente.centro_de_salud = self
            paciente.partido = self.partido
            paciente.provincia = self.provincia

        
#La logica es que el centro es el del donante

    def asignar_y_mandar_vehiculo(self, receptor : Receptores):
        """
        Determina qué tipo de vehículo utilizar para transportar un órgano, 
        según la ubicación del receptor comparada con la del centro.
        Si el partido es diferente se usa helicoptero, si la provincia es diferente, usa avión, y si estan en el mismo 
        y provincia usa el auto mas veloz. Marca el vehiculo como "ocupado" y lo despaca con una distancia aleatoria 
        correspondiente al tipo de viaje. 
        """
        '''
        if receptores.partido != self.partido: #condicion para llamar al helicopter
            distancia = rnd.randint(20,300) #distancia en km
            for i in self.lista_vehiculos:
                if isinstance(i, Helicoptero): # si pertenece a la clase helicoptero
                    if i.disponibilidad == "Disponible":
                        i.disponibilidad = "Ocupado"
                        return i.despachar(distancia)
                
        elif receptores.provincia != self.provincia: #condicion para llamar al avion
            distancia = rnd.randint(300,1700) #distancia en km
            for i in self.lista_vehiculos:
                if isinstance(i,Avion): #si pertenece  a la clase avion
                    if i.disponibilidad == "Disponible":
                        i.disponibilidad = "Ocupado"
                        return i.despachar(distancia)

        elif receptores.partido == self.partido and receptores.provincia == self.provincia: #condicion para llamar al terrestre (y mas veloz)
            distancia = rnd.randint(1,20) #distancia en km
            autos_disponibles = [i for i in self.lista_vehiculos
                                 if isinstance(i, Auto) and i.disponibilidad == "Disponible"]

            if autos_disponibles:
                auto_mas_rapido = max(autos_disponibles, key=lambda i: i.velocidad_viajes)
                auto_mas_rapido.disponibilidad = "Ocupado"
                return auto_mas_rapido.despachar(distancia)
        '''
        # Verificar que el receptor no sea None
        if receptor is None:
            print("Error: No se puede asignar vehículo, receptor es None")
            return None

        # Verificar que el receptor tenga atributos de ubicación
        if not hasattr(receptor, 'partido') or not hasattr(receptor, 'provincia'):
            print(f"Error: El receptor {receptor.nombre} no tiene información de ubicación")
            return None

        if receptor.partido != self.partido:
            distancia = rnd.randint(20, 300)
            for vehiculo in self.lista_vehiculos:
                if isinstance(vehiculo, Helicoptero) and vehiculo.disponibilidad == "Disponible":
                    vehiculo.disponibilidad = "Ocupado"
                    return vehiculo.despachar(distancia)
            print("No hay helicópteros disponibles")
            return None

        elif receptor.provincia != self.provincia:
            distancia = rnd.randint(300, 1700)
            for vehiculo in self.lista_vehiculos:
                if isinstance(vehiculo, Avion) and vehiculo.disponibilidad == "Disponible":
                    vehiculo.disponibilidad = "Ocupado"
                    return vehiculo.despachar(distancia)
            print("No hay aviones disponibles")
            return None

        elif receptor.partido == self.partido and receptor.provincia == self.provincia:
            distancia = rnd.randint(1, 20)
            autos_disponibles = [vehiculo for vehiculo in self.lista_vehiculos
                                 if isinstance(vehiculo, Auto) and vehiculo.disponibilidad == "Disponible"]

            if autos_disponibles:
                auto_mas_rapido = max(autos_disponibles, key=lambda vehiculo: vehiculo.velocidad_viajes)
                auto_mas_rapido.disponibilidad = "Ocupado"
                return auto_mas_rapido.despachar(distancia)
            else:
                print("No hay autos disponibles")
                return None

        return None

    def obtener_cirujanos_disponibles(self):
        """
        Obtiene una lista de cirujanos que están realmente disponibles.
        Verifica automáticamente si han cumplido las 24 horas de recuperación.
        """
        cirujanos_disponibles = []
        for cirujano in self.lista_cirujanos:
            if cirujano.verificar_disponibilidad():
                cirujanos_disponibles.append(cirujano)
        return cirujanos_disponibles

    def obtener_mejor_cirujano_para_organo(self, organo_necesario):
        """
        Busca el mejor cirujano disponible para un órgano específico.
        Prioriza especialistas sobre cirujanos generales.
        """
        cirujanos_disponibles = self.obtener_cirujanos_disponibles()

        if not cirujanos_disponibles:
            return None

        organo_necesario = organo_necesario.lower()

        # Primero buscar especialistas compatibles
        for cirujano in cirujanos_disponibles:
            especialidad = cirujano.especialidad.lower()
            if especialidad != "general":  # No es general
                organos_compatibles = cirujano.get_organos_compatibles()
                if organo_necesario in organos_compatibles:
                    return cirujano  # Encontrado especialista compatible

        # Si no hay especialistas, buscar cirujano general
        for cirujano in cirujanos_disponibles:
            if cirujano.especialidad.lower() == "general":
                return cirujano

        # Si no hay generales, devolver cualquier cirujano disponible
        return cirujanos_disponibles[0] if cirujanos_disponibles else None

    def mostrar_estado_cirujanos(self):
        """
        Muestra el estado actual de todos los cirujanos del centro.
        solo para monitoreo.
        """
        print(f"\n--- Estado de Cirujanos en {self.nombre} ---")
        for i, cirujano in enumerate(self.lista_cirujanos, 1):
            print(f"{i}. {cirujano}")
        print("-" * 50)

    def asignar_cirujano_y_operar(self, receptor: Receptores, tiempo):
        """
        Busca un cirujano disponible del centro considerando el tiempo de recuperación de 24 horas.
        Prioriza especialistas sobre cirujanos generales para mejorar las probabilidades de éxito.
        Marca al cirujano como "Ocupado" y ejecuta el método `realizar_cirujia`.
        """
        # FIX: Verificar que los parámetros no sean None
        if receptor is None:
            print("Error: No se puede operar, receptor es None")
            return

        if tiempo is None:
            print("Error: No se puede operar, tiempo es None")
            return

        # NUEVO: Buscar el mejor cirujano disponible para el órgano específico
        cirujano_asignado = self.obtener_mejor_cirujano_para_organo(receptor.organo_a_recibir)

        if cirujano_asignado is None:
            print(f"❌ No hay cirujanos disponibles en {self.nombre}")
            # Mostrar información sobre cuándo estarán disponibles
            print("Estado actual de cirujanos:")
            for cirujano in self.lista_cirujanos:
                tiempo_restante = cirujano.tiempo_restante_recuperacion()
                if tiempo_restante > 0:
                    print(f"  - {cirujano.especialidad.title()}: Disponible en {tiempo_restante} horas")
                else:
                    print(f"  - {cirujano.especialidad.title()}: Disponible ahora")
            return

        # Realizar la cirugía
        print(f"🩺 Asignando cirujano {cirujano_asignado.especialidad.title()} para {receptor.organo_a_recibir}")

        resultado_cirugia = cirujano_asignado.realizar_cirujia(tiempo, receptor)

        if resultado_cirugia:
            self.pacientes_exitosos.append(receptor)
            print(f"✅ Paciente {receptor.nombre} agregado a lista de exitosos")
        else:
            self.pacientes_fallidos.append(receptor)
            print(f"❌ Paciente {receptor.nombre} agregado a lista de fallidos")

            
