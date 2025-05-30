import random as rnd
from datetime import datetime, timedelta
from pacientes.Receptores import \
    Receptores  # Importar la clase Receptores desde el archivo Receptores.py de la carpeta pacientes


class Cirujanos:

    def __init__(self, especialidad):
        """
        Constructor de la clase Cirujanos.
        Recibe como argumento la especialidad del cirujano
        La disponibilidad se setea por defecto como 'Disponible'. También se inicializa una tabla de sinergias,
        que define qué especialidades están capacitadas para operar qué órganos.
        Se agrega control de tiempo para disponibilidad post-cirugía.
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
        Verifica si el cirujano está disponible basándose en el tiempo transcurrido
        desde su última cirugía. Si han pasado 24 horas o más, actualiza su estado a "Disponible".
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
        Devuelve las horas restantes hasta que el cirujano esté disponible.
        Retorna 0 si ya está disponible.
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
        Simula el proceso de una cirujia y determina el exito de esta. El parametro tiempo es la diferencia entre
        la hora actual y la hora de ablacion del organo. El parametro receptor, es el receptor que necesita el transplante.
        Si el organo ha pasado mas de 20hs desde la ablación, la cirujia se cancela automaticamente. Si el organo es compatible con la especialidad
        del cirujano, la probabilidad de exito es mayor, pero si no es compatible, la cirujia puede seguir adelante pero con menor probabilidad de exito.
        El cirujano estará ocupado por 24 horas después de la operación.
        Devuelve True si la cirujia fue exitosa. False si la cirujia falló. Y muestra un mensaje si el tiempo de ablacion supera las 20hs.
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
                if exito >= 5:  # 50% de probabilidad para cirujano general
                    print(f" Cirugía EXITOSA (cirujano general): {receptor.nombre} - {organo_necesario}")
                    return True
                else:
                    print(f" Cirugía FALLIDA (cirujano general): {receptor.nombre} - {organo_necesario}")
                    return False

            # Para cirujanos especialistas
            elif organo_necesario in self.tabla_sinergias.get(especialidad_cirujano, []):
                # Cirugía compatible: mayor probabilidad de éxito (70%)
                exito = rnd.randint(1, 10)  #Cambiar rango de 1-10 para que 3+ sea 70%
                if exito >= 3:
                    print(
                        f" Cirugía EXITOSA: {receptor.nombre} - {organo_necesario} por especialista en {especialidad_cirujano}")
                    return True
                else:
                    print(
                        f" Cirugía FALLIDA: {receptor.nombre} - {organo_necesario} por especialista en {especialidad_cirujano}")
                    return False

            else:
                # Cirugía no compatible: menor probabilidad de éxito (50%)
                exito = rnd.randint(1, 10)
                if exito >= 5:  #50% de probabilidad
                    print(
                        f" Cirugía EXITOSA (no especialista): {receptor.nombre} - {organo_necesario} por {especialidad_cirujano}")
                    return True
                else:
                    print(
                        f" Cirugía FALLIDA (no especialista): {receptor.nombre} - {organo_necesario} por {especialidad_cirujano}")
                    return False

        #Caso por defecto (no debería llegar aquí, pero por seguridad)
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