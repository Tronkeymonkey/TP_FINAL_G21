
class Pacientes:
    def __init__(self, nombre, DNI, sexo, nacimiento, Tsangre, telefono):
        """
        Inicializa un objeto Pacientes con los datos básicos de un paciente.

        params:
            - nombre: Nombre completo del paciente.
            - DNI: Documento Nacional de Identidad del paciente (puede generarse aleatoriamente).
            - sexo: Sexo biológico del paciente.
            - nacimiento: Fecha de nacimiento del paciente (puede generarse aleatoriamente o con datetime).
            - Tsangre: Tipo de sangre del paciente.
            - telefono: Número de contacto del paciente.

        precon (opcional):
            - DNI puede ser generado aleatoriamente si no se provee.
            - nacimiento puede ser una fecha real o generada.
        
        returns:
            None. Inicializa una instancia de Pacientes con los atributos proporcionados.
        """
        self.nombre = nombre
        self.DNI = DNI #este se obtiene con un random 
        self.sexo = sexo
        self.nacimiento = nacimiento #este se obtiene con un random o daytime o ambas (o quizas ninguna ja)
        self.Tsangre = Tsangre
        self.telefono = telefono


