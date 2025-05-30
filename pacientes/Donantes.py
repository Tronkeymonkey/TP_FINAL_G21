from pacientes.Pacientes import Pacientes
from organos.Organos import Organos

class Donantes(Pacientes):

    def __init__(self, nombre, DNI, sexo, nacimiento, Tsangre, telefono, fhfallecimiento, organos_a_donar=[]):
        super().__init__(nombre, DNI, sexo, nacimiento, Tsangre, telefono)
        self.fhfallecimiento = fhfallecimiento
        self.organos_a_donar: list[Organos] = organos_a_donar if isinstance(organos_a_donar, list) else [organos_a_donar]
        self.partido = None
        self.provincia = None
        self.centro_de_salud = None
        