class Organos:

    def __init__(self, tipo_de_organo):
        """
    Representa un órgano que puede ser donado.

    params:
        - tipo_de_organo: Una cadena de texto que indica el tipo o nombre del órgano.
        """
        self.tipo_de_organo = tipo_de_organo
        self.fecha_ablacion = None # fecha en la que se realiza la ablacion del organo, no pongo nada, ya que no se sabe cuando se va a donar el organo
