from pacientes.Receptores import Receptores
from organos.Organos import Organos
from incucai.INCUCAI import INCUCAI
from vehiculos.Auto import Auto
from vehiculos.Avion import Avion
from vehiculos.Helicoptero import Helicoptero
from centro_salud.Centro_Salud import CentroSalud
from cirujanos.Cirujanos import Cirujanos
from pacientes.Donantes import Donantes
import datetime
from src.menu import *

cirujanos = [Cirujanos("Cardiovascular"),
             Cirujanos("Gastroenterologo"),
             Cirujanos("General")]

# Crear vehículos
vehiculos = [
    Auto(velocidad_viajes=80, identificador="AD 342 SD"),
    Auto(velocidad_viajes=100, identificador="AB 134 DF"),
    Helicoptero(velocidad_viajes=250, identificador="HEL01"),
    Helicoptero(velocidad_viajes=300, identificador="HEL02"),
    Avion(velocidad_viajes=600, identificador="AE01"),
    Avion(velocidad_viajes=700, identificador="AE02")]

centros_salud = [
    CentroSalud("Hospital Italiano", "Calle Falsa 123", "1122334455", "3 de Febrero", "Buenos Aires", [cirujanos[1]], [vehiculos[0], vehiculos[2]]),
    CentroSalud("Hospital Privado Rosario", " Pres. Roca 2440", "0341 489-3500", "Rosario", "Santa Fe", [cirujanos[1], cirujanos[2]], [vehiculos[1], vehiculos[3]]),
    CentroSalud("Hospital Zonal Dr. Ramón Carrillo", "20 de Febrero 598 ", "0294 452-5000", "Bariloche", "Rio Negro", [cirujanos[2]], [vehiculos[4]]),
    CentroSalud("Sanatorio Parque", "Blvd. Oroño 860", " 0341 420-0222", "Rosario", "Santa Fe", [cirujanos[1]], [vehiculos[5]])]

organos = [
    Organos("riñon"),
    Organos("corazon"),
    Organos("pulmon"),
    Organos("higado"),
    Organos("corneas"),
    Organos("intestinos"),
    Organos("piel"),
    Organos("huesos")]

pacientes = [
    Receptores("Ignacio Amarillo", 23456987, "M", datetime.datetime.strptime("1973-02-09", "%Y-%m-%d"), "O+", 113334567, "riñon", datetime.datetime.strptime("2024-10-23", "%Y-%m-%d"), 1, "Insuficiencia renal"),
    Receptores("Maria Escalante", 34654321, "F", datetime.datetime.strptime("1995-05-15", "%Y-%m-%d"), "A+", 11234567, "corazon", datetime.datetime.strptime("2025-10-02", "%Y-%m-%d"), 2, "Cardiopatía"),
    Receptores("Luis Beinlich", 45608230, "M", datetime.datetime.strptime("2005-09-01", "%Y-%m-%d"), "O+", 270345678, "pulmon", datetime.datetime.strptime("2022-11-21", "%Y-%m-%d"), 1, "Neumonía"),
    Receptores("Ana Lavalle", 25445566, "F", datetime.datetime.strptime("1975-03-22", "%Y-%m-%d"), "B-", 341354769, "higado", datetime.datetime.strptime("2024-01-15", "%Y-%m-%d"), 3, "Hepatitis"),

    Donantes("Carlos Ponce", 34222333, "M", datetime.datetime.strptime("1985-06-30", "%Y-%m-%d"), "O+", 23459385, datetime.datetime.strptime("2025-03-21", "%Y-%m-%d"), [organos[0]]),
    Donantes("Elena Mariscotti", 22113344, "F", datetime.datetime.strptime("1970-04-10", "%Y-%m-%d"), "A+", 112305739, datetime.datetime.strptime("2025-04-07", "%Y-%m-%d"), [organos[0], organos[3], organos[4]]),
    Donantes("Tomas Hourquescos", 35112244, "M", datetime.datetime.strptime("1995-12-01", "%Y-%m-%d"), "O+", 341823045, datetime.datetime.strptime("2025-04-25", "%Y-%m-%d"), [organos[5], organos[6], organos[7]]),
    Donantes("Lucía Drappo", 44112233, "F", datetime.datetime.strptime("1982-08-08", "%Y-%m-%d"), "B-", 1134728305, datetime.datetime.strptime("2025-05-03", "%Y-%m-%d"), [organos[2], organos[5], organos[4]]),
    Donantes("Franca Nanni", 47034652, "F", datetime.datetime.strptime("2006-03-24", "%Y-%m-%d"), "O+", 3412348764, datetime.datetime.strptime("2025-05-15", "%Y-%m-%d"), [organos[1]]),

    Receptores("Ricardo Sánchez", 28901234, "M", datetime.datetime.strptime("1980-11-10", "%Y-%m-%d"), "A-", 115678901, "higado", datetime.datetime.strptime("2023-09-05", "%Y-%m-%d"), 2, "Insuficiencia hepática"),
    Receptores("Pedro Giménez", 31098765, "M", datetime.datetime.strptime("1990-03-01", "%Y-%m-%d"), "O-", 341987654, "corazon", datetime.datetime.strptime("2024-02-18", "%Y-%m-%d"), 1, "Miocardiopatía dilatada"),
    Receptores("Valeria Rossi", 29876543, "F", datetime.datetime.strptime("1983-09-25", "%Y-%m-%d"), "B+", 261876543, "pulmon", datetime.datetime.strptime("2023-11-30", "%Y-%m-%d"), 3, "Enfisema pulmonar"),
    Receptores("Florencia Blanco", 38012345, "F", datetime.datetime.strptime("1996-12-12", "%Y-%m-%d"), "O+", 387123456, "riñon", datetime.datetime.strptime("2024-05-20", "%Y-%m-%d"), 2, "Poliquistosis renal"),
    Receptores("Emilia Gómez", 30123456, "F", datetime.datetime.strptime("1988-06-03", "%Y-%m-%d"), "AB+", 341456789, "higado", datetime.datetime.strptime("2023-07-10", "%Y-%m-%d"), 1, "Diabetes tipo 1"),
]

centros_salud[0].asignar_pacientes([pacientes[0], pacientes[4], pacientes[13]])
centros_salud[1].asignar_pacientes([pacientes[1], pacientes[2], pacientes[3]])
centros_salud[2].asignar_pacientes([pacientes[5], pacientes[6], pacientes[7], pacientes[8], pacientes[9]])
centros_salud[3].asignar_pacientes([pacientes[10], pacientes[11], pacientes[12]])


incucai = INCUCAI(centros_salud)

incucai.clasificar_centros_salud()

menu(incucai)
