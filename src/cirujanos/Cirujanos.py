import random as rnd
from datetime import datetime, timedelta
from pacientes.Receptores import \
    Receptores  # Importar la clase Receptores desde el archivo Receptores.py de la carpeta pacientes


class Cirujanos:

    def __init__(self, especialidad):
        """
    Constructor de la clase Cirujanos.
    
    params:
        - especialidad: La especialidad médica del cirujano (por ejemplo, 'cardiovascular', 'plastico', etc.).
    
    precon:
        La especialidad debe estar en minúsculas o será convertida automáticamente. Se espera que coincida con alguna clave de la tabla de sinergias.
    
    returns:
        No retorna nada directamente. Inicializa los atributos del objeto:
            - self.especialidad: almacena la especialidad en minúsculas.
            - self.disponibilidad: se setea como 'Disponible' por defecto.
            - self.ultima_cirugia: inicia como None y almacenará la última fecha de cirugía.
            - self.tiempo_recuperacion: valor fijo en horas (24) para volver a estar disponible.
            - self.tabla_sinergias: diccionario que indica qué especialidades pueden operar qué órganos.
    """
        self.especialidad = especialidad.lower()
        self.disponibilidad = "Disponible"
        self.ultima_cirugia = None  #Almacena la fecha/hora de la última cirugía
        self.tiempo_recuperacion = 24  #Horas que debe esperar antes de estar disponible otra vez

        #Tabla de sinergias
        self.tabla_sinergias = {
            "cardiovascular": ["corazon"],
            "pulmonar": ["pulmon"],
            "plastico": ["piel", "corneas"],
            "traumatologo": ["huesos"],
            "gastroenterologo": ["higado", "riñon", "intestinos"],  
            "general": ["corazon", "pulmon", "piel", "corneas", "huesos", "higado", "riñon", "intestinos"]
        }

    def verificar_disponibilidad(self):
        """
        Verifica si el cirujano está disponible para operar, basándose en el tiempo transcurrido
    desde su última cirugía.

    params:
        - self: instancia actual del objeto Cirujano.

    precon:
        self.ultima_cirugia debe ser None o un objeto datetime válido.
        self.tiempo_recuperacion debe estar definido (en horas).

    returns:
        True si el cirujano está disponible (han pasado 24 horas o más desde la última cirugía,
        o aún no ha realizado ninguna); False en caso contrario. También actualiza el estado
        de disponibilidad internamente a "Disponible" u "Ocupado" según corresponda.
        """
        if self.ultima_cirugia is None:
            self.disponibilidad = "Disponible"
            return True

        tiempo_actual = datetime.now()
        tiempo_transcurrido = tiempo_actual - self.ultima_cirugia
        horas_transcurridas = tiempo_transcurrido.total_seconds() / 3600

        if horas_transcurridas >= self.tiempo_recuperacion:
            self.disponibilidad = "Disponible"
            return True
        else:
            self.disponibilidad = "Ocupado"
            horas_restantes = self.tiempo_recuperacion - horas_transcurridas
            return False

    def tiempo_restante_recuperacion(self):
        """
    Calcula y devuelve la cantidad de horas restantes para que el cirujano
    vuelva a estar disponible.

    params:
        - self: instancia actual del objeto Cirujano.

    precon:
        self.ultima_cirugia debe ser None o un objeto datetime válido.
        self.tiempo_recuperacion debe estar definido (en horas).

    returns:
        Un número flotante representando las horas restantes hasta que el cirujano
        esté disponible. Si ya está disponible (o no ha operado nunca), retorna 0.
        El valor retornado se redondea a un decimal.
        """
        if self.ultima_cirugia is None:
            return 0

        tiempo_actual = datetime.now()
        tiempo_transcurrido = tiempo_actual - self.ultima_cirugia
        horas_transcurridas = tiempo_transcurrido.total_seconds() / 3600

        if horas_transcurridas >= self.tiempo_recuperacion:
            return 0
        else:
            return round(self.tiempo_recuperacion - horas_transcurridas, 1)

    def realizar_cirujia(self, tiempo, receptor: Receptores):
        """
        Simula el proceso de una cirugía y determina su éxito.

    params:
        - tiempo: Diferencia en horas entre la hora actual y la hora de ablación del órgano.
        - receptor: Objeto Receptores que representa al paciente que necesita el trasplante.

    precon:
        - El cirujano debe estar disponible para realizar la cirugía.
        - El tiempo debe ser un valor numérico positivo.
        - El receptor no debe ser None.
        - Si el tiempo de ablación supera las 20 horas, la cirugía se cancela automáticamente.

    returns:
        - True si la cirugía fue exitosa.
        - False si la cirugía falló o fue cancelada (por disponibilidad, receptor None o tiempo excedido).
        """
        #Verificar disponibilidad basada en tiempo
        if not self.verificar_disponibilidad():
            tiempo_restante = self.tiempo_restante_recuperacion()
            print(f" Cirujano no disponible. Tiempo restante de recuperación: {tiempo_restante} horas")
            return False

        #Verificar que los parámetros no sean None
        if receptor is None:
            print("Error: No se puede realizar cirugía, receptor es None")
            return False

        if tiempo is None:
            print("Error: No se puede realizar cirugía, tiempo es None")
            return False

        tiempo_tardado = tiempo

        if tiempo_tardado > 20:
            print("Cirugía interrumpida: TIEMPO DE ABLACIÓN MAYOR A 20 HS")
            return False  #Retornar False cuando se cancela por tiempo

        if tiempo_tardado <= 20:
            #Obtener la especialidad correctamente y verificar compatibilidad
            organo_necesario = receptor.organo_a_recibir.lower()
            especialidad_cirujano = self.especialidad.lower()

            #Marcar el tiempo de la cirugía y cambiar disponibilidad
            self.ultima_cirugia = datetime.now()
            self.disponibilidad = "Ocupado"

            #El cirujano general siempre tiene 50% de éxito independientemente del órgano
            if especialidad_cirujano == "general":
                exito = rnd.randint(1, 10)
                if exito >= 5: 
                    print(f" Cirugía EXITOSA (cirujano general): {receptor.nombre} - {organo_necesario}")
                    return True
                else:
                    print(f" Cirugía FALLIDA (cirujano general): {receptor.nombre} - {organo_necesario}")
                    return False

            # Para cirujanos especialistas
            elif organo_necesario in self.tabla_sinergias.get(especialidad_cirujano, []):
                
                exito = rnd.randint(1, 10)  
                if exito >= 3:
                    print(
                        f" Cirugía EXITOSA: {receptor.nombre} - {organo_necesario} por especialista en {especialidad_cirujano}")
                    return True
                else:
                    print(
                        f" Cirugía FALLIDA: {receptor.nombre} - {organo_necesario} por especialista en {especialidad_cirujano}")
                    return False

            else:
                # Cirugía no compatible
                exito = rnd.randint(1, 10)
                if exito >= 5:  
                    print(
                        f" Cirugía EXITOSA (no especialista): {receptor.nombre} - {organo_necesario} por {especialidad_cirujano}")
                    return True
                else:
                    print(
                        f" Cirugía FALLIDA (no especialista): {receptor.nombre} - {organo_necesario} por {especialidad_cirujano}")
                    return False

        #Caso por defecto (no debería llegar aca, pero por seguridad)
        return False

    def __str__(self):
        """
        Método mágico para representación legible del cirujano
        Incluye información sobre disponibilidad y tiempo de recuperación
        """
        if self.disponibilidad == "Disponible":
            return f"Dr./Dra. - Especialidad: {self.especialidad.title()} - Estado: {self.disponibilidad}"
        else:
            tiempo_restante = self.tiempo_restante_recuperacion()
            return f"Dr./Dra. - Especialidad: {self.especialidad.title()} - Estado: {self.disponibilidad} (Disponible en {tiempo_restante} horas)"

    def get_organos_compatibles(self):
        """
        Método auxiliar que devuelve los órganos que puede operar este cirujano
        """
        return self.tabla_sinergias.get(self.especialidad, [])