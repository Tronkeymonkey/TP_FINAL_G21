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
    
    params:
        - nombre: Nombre del centro de salud.
        - direccion: Dirección física del centro de salud.
        - telefono: Número de teléfono de contacto del centro.
        - partido: Partido donde se encuentra el centro (división administrativa).
        - provincia: Provincia correspondiente al centro.
        - lista_cirujanos: Lista inicial de objetos Cirujano asociados al centro. Puede ser una lista vacía.
        - lista_vehiculos: Lista inicial de vehículos (Auto, Helicóptero o Avión) disponibles para traslados.
        - lista_pacientes: Lista inicial de pacientes (Receptores o Donantes), no se usa directamente en este constructor.
    
    precon:
        - Se espera que las listas proporcionadas sean instancias de `list` o un solo objeto del tipo correspondiente (se encapsula en lista).
    
    returns:
        No aplica. Este es un constructor, por lo tanto, inicializa los atributos del objeto CentroSalud.
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
    Asigna una lista de pacientes (Receptores o Donantes) al centro de salud.
    
    params:
        - pacientes: Lista de objetos que representan pacientes, ya sean de tipo Receptor o Donante.
    
    precon:
        - Cada objeto en la lista debe ser una instancia válida de Receptor o Donante.
    
    returns:
        No retorna ningún valor. Modifica el estado interno del centro y de los pacientes, 
        vinculándolos al centro actual y actualizando su información de ubicación (partido y provincia).
    """
        self.lista_pacientes.extend(pacientes)
        for paciente in pacientes:    
            paciente.centro_de_salud = self
            paciente.partido = self.partido
            paciente.provincia = self.provincia


 #La logica es que el centro es el del donante
    def asignar_y_mandar_vehiculo(self, receptor : Receptores):
        """
    Asigna y despacha un vehículo adecuado para transportar un órgano hacia el receptor,
    según la ubicación del paciente en relación con el centro de salud. Una vez encuentra, su disponibilidad es "ocupado".
    
    params:
        - receptor: Objeto de tipo Receptor que representa al paciente que recibirá el órgano.
    
    precon:
        - Debe haber al menos un vehículo disponible del tipo adecuado en la lista del centro.
    
    returns:
        El resultado del método `despachar(distancia)` del vehículo seleccionado si se encuentra uno disponible.
        Si no hay vehículos adecuados disponibles o el receptor es inválido, retorna `None`.
    """
    #Despues de hacer pruebas, el receptor siempre tendra atributos de partido y provincia y tampoco sera un valor nulo, es por eso que omitimos los ifs para corroborar que dichos casos no ocurran.

        if receptor.partido.__ne__(self.partido): #metodo magico ne (!=)
            distancia = rnd.randint(20, 300)
            for vehiculo in self.lista_vehiculos:
                if isinstance(vehiculo, Helicoptero) and vehiculo.disponibilidad.__eq__("Disponible"): #metodo magico eq (==) y ademas, utiliza isistance para chequear que los vehiculos de la lista del centro sean del tipo adecuado
                    vehiculo.disponibilidad = "Ocupado"
                    return vehiculo.despachar(distancia)
            print("No hay helicópteros disponibles")
            return None

        elif receptor.provincia.__ne__(self.provincia):
            distancia = rnd.randint(300, 1700)
            for vehiculo in self.lista_vehiculos:
                if isinstance(vehiculo, Avion) and vehiculo.disponibilidad.__eq__("Disponible"):
                    vehiculo.disponibilidad = "Ocupado"
                    return vehiculo.despachar(distancia)
            print("No hay aviones disponibles")
            return None

        elif receptor.partido.__eq__(self.partido) and receptor.provincia.__eq__(self.provincia):
            distancia = rnd.randint(1, 20)
            autos_disponibles = [vehiculo for vehiculo in self.lista_vehiculos
                                 if isinstance(vehiculo, Auto) and vehiculo.disponibilidad.__eq__("Disponible")]

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
    Retorna el mejor cirujano disponible para realizar un trasplante de un órgano específico.

    params:
        - organo_necesario: Cadena de texto que representa el nombre del órgano que se necesita trasplantar.

    precon:
        - `organo_necesario` debe ser una cadena válida y en un formato reconocible por los métodos de los cirujanos.
        - Se asume que cada cirujano tiene un método `get_organos_compatibles()` que devuelve una lista de órganos que puede operar.
        - La lista de cirujanos disponibles se obtiene a través del método `obtener_cirujanos_disponibles()`.

    returns:
        - Un objeto Cirujano compatible con el órgano requerido, priorizando especialistas por sobre cirujanos generales.
        - Si no se encuentra un especialista, retorna un cirujano general disponible.
        - Si no hay ninguno disponible, retorna el primer cirujano libre como último recurso.
        - Si no hay ningún cirujano disponible, retorna `None`.
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
    Asigna un cirujano disponible, priorizando al que domine el organo a operar y ejecuta una cirugía de trasplante sobre el receptor.

    params:
        - receptor: Instancia de Receptores que representa al paciente que recibirá el órgano.
        - tiempo: Entero que indica el tiempo estimado de la cirugía (usado para gestionar la recuperación del cirujano).

    precon:
        - `receptor` debe ser una instancia válida y contener el atributo `organo_a_recibir`.
        - Debe haber al menos un cirujano disponible en el centro de salud, preferentemente especializado.

    returns:
        - No retorna ningún valor. Realiza acciones internas:
            - Asigna al mejor cirujano disponible para el órgano requerido.
            - Llama al método `realizar_cirujia()` del cirujano asignado.
            - Agrega al paciente a la lista de `pacientes_exitosos` o `pacientes_fallidos` según el resultado.
    """

        cirujano_asignado = self.obtener_mejor_cirujano_para_organo(receptor.organo_a_recibir) #la funcion puede retornar al mejor cirujano o al disponible, por eso se la llama

        if cirujano_asignado is None:
            print(f" No hay cirujanos disponibles en {self.nombre}")
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
        print(f" Asignando cirujano {cirujano_asignado.especialidad.title()} para {receptor.organo_a_recibir}")

        resultado_cirugia = cirujano_asignado.realizar_cirujia(tiempo, receptor)

        if resultado_cirugia:
            self.pacientes_exitosos.append(receptor)
            print(f" Paciente {receptor.nombre} agregado a lista de exitosos")
        else:
            self.pacientes_fallidos.append(receptor)
            print(f" Paciente {receptor.nombre} agregado a lista de fallidos")

            
