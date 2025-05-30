from pacientes.Pacientes import Pacientes
from organos.Organos import Organos

class Receptores(Pacientes):

    def __init__(self, nombre, DNI, sexo, nacimiento, Tsangre, telefono, organo_a_recibir, fecha_en_espera, patologia, estado = None):
        super().__init__(nombre, DNI, sexo, nacimiento, Tsangre, telefono)
        """
        Inicializa un objeto Receptores, que hereda de Pacientes, con atributos específicos para receptores de órganos.

        params:
            - nombre: Nombre completo del receptor.
            - DNI: Documento Nacional de Identidad del receptor.
            - sexo: Sexo biológico del receptor.
            - nacimiento: Fecha de nacimiento del receptor.
            - Tsangre: Tipo de sangre del receptor.
            - telefono: Número de contacto del receptor.
            - organo_a_recibir: Órgano que el receptor necesita recibir (se almacena en minúsculas).
            - fecha_en_espera: Fecha desde la cual el receptor está en lista de espera para trasplante.
            - patologia: Patología o enfermedad del receptor que justifica el trasplante.
            - estado: Estado actual del receptor, por defecto "Estable".

        precon (opcional):
            - organo_a_recibir debe ser una cadena que se pueda convertir a minúsculas.
            - estado suele ser "Estable" salvo que falle el trasplante.

        returns:
            None. Inicializa una instancia de Receptores con los atributos proporcionados.
        """
        organo_a_recibir = organo_a_recibir.lower()
        self.organo_a_recibir = organo_a_recibir
        self.fecha_en_espera = fecha_en_espera
        self.estado = "Estable" #siempre va a estar estable, a menos que falle el trasplante 
        self.organos_a_disposicion: list [Organos] =[] # lista de organos que el receptor puede recibir, en caso de que haya compatibilidad con el donante
        self.patologia = patologia
        self.partido = None
        self.provincia = None
        self.centro_de_salud = None

    #No hay prioridad como atributo a declarar, ya que este se ve influenciado por su estado y edad