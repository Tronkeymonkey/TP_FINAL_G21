from pacientes.Pacientes import Pacientes
from organos.Organos import Organos

class Donantes(Pacientes):

    def __init__(self, nombre, DNI, sexo, nacimiento, Tsangre, telefono, fhfallecimiento, organos_a_donar=[]):
        super().__init__(nombre, DNI, sexo, nacimiento, Tsangre, telefono)
        """
        Inicializa un objeto Donantes, que hereda de Pacientes, con datos personales y atributos específicos para donantes.

        params:
            - nombre: Nombre completo del donante.
            - DNI: Documento Nacional de Identidad del donante.
            - sexo: Sexo biológico del donante.
            - nacimiento: Fecha de nacimiento del donante.
            - Tsangre: Tipo de sangre del donante.
            - telefono: Número de contacto del donante.
            - fhfallecimiento: Fecha de fallecimiento del donante.
            - organos_a_donar: Lista de órganos que el donante está dispuesto a donar.

        precon (opcional):
            - organos_a_donar debe ser una lista o un único objeto órgano que será convertido en lista.

        returns:
            None. Inicializa una instancia de Donantes con los atributos proporcionados.
        """
        self.fhfallecimiento = fhfallecimiento
        self.organos_a_donar: list[Organos] = organos_a_donar if isinstance(organos_a_donar, list) else [organos_a_donar]
        self.partido = None
        self.provincia = None
        self.centro_de_salud = None
        