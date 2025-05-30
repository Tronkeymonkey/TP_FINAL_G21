from incucai.INCUCAI import *
from centro_salud.Centro_Salud import *
from typing import List
import datetime
import os


# --------- Funciones para el menu ---------
def validar_fecha(fecha_str, formato="%Y-%m-%d", anios_max=100):
    try:
        fecha = datetime.datetime.strptime(fecha_str, formato)
        hoy = datetime.datetime.now()
        fecha_minima = hoy - datetime.timedelta(days=anios_max*365)
        if fecha_minima <= fecha <= hoy:
            return fecha
        else:
            print("Fecha fuera de rango lógico.")
    except ValueError:
        print("Formato de fecha inválido, Ingrese correctamente: Año, Mes, Dia.")
    return None

def obtener_centro_salud(incucai: INCUCAI, nombre_centro: str):
    for centro in incucai.centros_salud:
        if centro.nombre.strip().lower() == nombre_centro.strip().lower():
            return centro
    return None

def input_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número válido.")

def dni_donante_ya_existe(incucai: INCUCAI, dni: int) -> bool:
    return any(d.DNI == dni for d in incucai.lista_donantes)

def dni_receptor_ya_existe(incucai: INCUCAI, dni: int) -> bool:
    return any(r.DNI == dni for r in incucai.lista_receptores)

def calcular_edad(nacimiento: datetime.datetime) -> int:
    hoy = datetime.datetime.now()
    return hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))


def listas_receptores_por_centro(incucai: INCUCAI):
    print("\n---- LISTA RECEPTORES POR CENTRO DE SALUD -----")

    if not incucai.centros_salud:
        print("No hay centros de salud registrados")
        return

    listas_centros_salud(incucai)  # va a mostrar todos los centros de salud

    nombre_centro = input("\nIngrese el nombre del centro de salud para ver sus receptores: ")
    centro = obtener_centro_salud(incucai, nombre_centro)

    if not centro:
        print("Centro no encontrado. Verifique el nombre.")
        return

    receptores_filtrados = [r for r in incucai.lista_receptores if
                            r.centro_de_salud.nombre.lower() == centro.nombre.lower()]

    if not receptores_filtrados:
        print(f"No hay receptores registrados en el centro de salud: {centro.nombre}")
        return

    # Ordena por estado (inestables primero) y luego por edad (más joven primero)
    receptores_ordenados = sorted(
        receptores_filtrados,
        key=lambda r: (
            0 if getattr(r, 'estado', 'estable').lower() == 'inestable' else 1,  # Inestables primero
            calcular_edad(r.nacimiento)  # Más joven primero
        )
    )

    print(f"\nReceptores en {centro.nombre} (ordenados por estado y edad):")

    # Separar por grupos y mostrar con títulos
    inestables = [r for r in receptores_ordenados if getattr(r, 'estado', 'estable').lower() == 'inestable']
    estables = [r for r in receptores_ordenados if getattr(r, 'estado', 'estable').lower() == 'estable']

    contador = 1

    # Mostrar receptores inestables
    if inestables:
        print(f"\n RECEPTORES INESTABLES (PRIORIDAD CRÍTICA):")
        print("-" * 50)
        for i in inestables:
            print(
                f"{contador}. Nombre: {i.nombre} - Órgano: {i.organo_a_recibir} - Sangre: {i.Tsangre} - Edad: {calcular_edad(i.nacimiento)} - Partido: {i.partido} - Provincia: {i.provincia}")
            contador += 1

    # Mostrar receptores estables
    if estables:
        print(f"\n RECEPTORES ESTABLES:")
        print("-" * 30)
        for i in estables:
            print(
                f"{contador}. Nombre: {i.nombre} - Órgano: {i.organo_a_recibir} - Sangre: {i.Tsangre} - Edad: {calcular_edad(i.nacimiento)} - Partido: {i.partido} - Provincia: {i.provincia}")
            contador += 1

    if not inestables and not estables:
        print("No hay receptores para mostrar.")
        
def listas_donantes(incucai:INCUCAI):
    print("\n----- LISTA DONANTES ----")
    for idx, i in enumerate(incucai.lista_donantes):
        centro_nombre = i.centro_de_salud.nombre if i.centro_de_salud else "Sin asignar"
        print(f"{idx}. Nombre: {i.nombre} - Tipo de sangre: {i.Tsangre} - Centro de salud: {centro_nombre}")

        # Opcional: mostrar órganos disponibles
        if hasattr(i, 'organos_a_donar') and i.organos_a_donar:
            organos = [organo.tipo_de_organo for organo in i.organos_a_donar]
            print(f"   Órganos disponibles: {', '.join(organos)}")
        print()  # Línea en blanco para mejor legibilidad
        
def listas_centros_salud(incucai: INCUCAI):
    print("\n ---- CENTROS DE SALUD ----")
    for i in incucai.centros_salud:
        print(f" Nombre: {i.nombre} - Partido: {i.partido} - Provincia: {i.provincia} - Tel: {i.telefono} ") 

      
def agregar_receptor(incucai: INCUCAI):
    print("\n CARGAR NUEVO RECEPTOR")
    
    # Solicitar DNI primero
    while True:
        dni_input = input("DNI (8 dígitos): ").strip()
        if not dni_input.isdigit():
            print("El DNI debe contener solo números.")
        elif len(dni_input) != 8:
            print("El DNI debe tener exactamente 8 dígitos.")
        else:
            dni = int(dni_input)
            if dni_donante_ya_existe(incucai, dni):
                print( "Ya existe un donante con ese DNI. Cancelando ingreso.")
                return  # corta la función
            if dni_receptor_ya_existe(incucai, dni):
                print("Ya existe un receptor con ese DNI. Cancelando ingreso.")
                return
            break  # DNI válido y no repetido
        
    #bucle nombre
    while True:
        nombre = input("Nombre: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío. Ingrese nuevamente un nombre:")
        elif any(char.isdigit() for char in nombre):
            print("El nombre no puede contener números. Ingrese nuevamente un nombre:")
        else:
            break
        
    #bucle sexo
    sexo = input("Sexo: M para masculino, F para femenino: ")
    while sexo.upper() not in ("M", "F"):
        print("Sexo inválido. Ingrese M o F.")
        sexo = input("Sexo (M/F): ")
    sexo = sexo.upper()
    
    #bucle nacimiento
    #Inicializo nacimiento en none, no hay una fecha valida todavia
    #que la edad sea mayor o igual a tal edad para perfeccionarlo
    nacimiento = None
    while not nacimiento: #se ejecuta el bucle mientras la variable nacimiento siga siendo none, mientras que no tengamos una fecha valida
        nacimiento_input = input("Fecha de nacimiento (YYYY-MM-DD): ") #Ingresa el usuario una fecha en el formato adecuado
        nacimiento = validar_fecha(nacimiento_input, "%Y-%m-%d") #Se llama a la funcion validar fecha para hacer la validacion real. Se escribe en el formato correcto y la fecha es logica, la funcion devuelve un objeto datetime, sino muestra error y el while sigue.
    
    #bucle grupos sanguineos
    grupos_validos = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    while True:     
        grupo_sanguineo = input("Grupo sanguíneo (A+, A-, B+, B-, AB+, AB-, O+, O-): ").strip().upper()
        if grupo_sanguineo in grupos_validos:
            break
        else:
            print("Grupo sanguíneo inválido. Ingrese uno de estos grupos: (A+, A-, B+, B-, AB+, AB-, O+, O-).")
    
    telefono = input_entero("Telefono:") #ver cuantos digitos tiene que poner
    
    #bucle centro de salud
    centro_de_salud = None
    while not centro_de_salud:
        nombre_centro = input("Nombre del centro de salud: ")
        centro_de_salud = obtener_centro_salud(incucai, nombre_centro) #llama a mi funcion obtener centro para que coincidan lo que tengo en las listas con lo que ingreso
        if not centro_de_salud:
            print("Centro no encontrado. Verifique el nombre.")
    
    #bucle organos        
    organos_validos = ["corazon", "pulmon", "piel", "corneas", "huesos", "higado", "riñon", "intestinos"]
    while True:
        organo_a_recibir = input("Órgano que necesita: ").strip().lower()
        if organo_a_recibir in organos_validos:
            break
        else:
            print(f"Órgano inválido. Debe ser uno de: {', '.join(organos_validos)}")
            
                       
    #bucle fecha en esperadel receptor
    fecha_en_espera = None
    while not fecha_en_espera:
        espera_input = input("Fecha de espera (YYYY-MM-DD HH:MM): ")
        fecha_en_espera = validar_fecha(espera_input, "%Y-%m-%d %H:%M")
    
    patologia = input("Patología: ").strip()

    nuevo = Receptores(nombre, dni, sexo, nacimiento, grupo_sanguineo, telefono, organo_a_recibir, fecha_en_espera, patologia)

    # Asignar el centro al receptor
    nuevo.centro_de_salud = centro_de_salud
    nuevo.partido = centro_de_salud.partido
    nuevo.provincia = centro_de_salud.provincia

    incucai.lista_receptores.append(nuevo)
    centro_de_salud.lista_pacientes.append(nuevo)
    print("Receptor agregado correctamente.")


def agregar_donante(incucai: INCUCAI):
    print("\nCARGAR NUEVO DONANTE:")

    # Bucle nombre
    while True:
        nombre = input("Nombre: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
        elif any(char.isdigit() for char in nombre):
            print("El nombre no puede contener números.")
        else:
            break

    # Bucle DNI
    while True:
        dni_input = input("DNI (8 dígitos): ").strip()
        if not dni_input.isdigit():
            print("El DNI debe contener solo números.")
        elif len(dni_input) != 8:
            print("El DNI debe tener exactamente 8 dígitos.")
        else:
            dni = int(dni_input)
            # Verificar que no exista ya
            if dni_donante_ya_existe(incucai, dni):
                print("Ya existe un donante con ese DNI. Cancelando ingreso.")
                return
            if dni_receptor_ya_existe(incucai, dni):
                print("Ya existe un receptor con ese DNI. Cancelando ingreso.")
                return
            break

    # Bucle sexo
    while True:
        sexo = input("Sexo (M/F): ").strip().upper()
        if sexo in ("M", "F"):
            break
        else:
            print("Sexo inválido. Ingrese M o F.")

    # Bucle nacimiento
    fecha_nacimiento = None
    while not fecha_nacimiento:
        nacimiento_input = input("Fecha de nacimiento (YYYY-MM-DD): ")
        fecha_nacimiento = validar_fecha(nacimiento_input, "%Y-%m-%d")

    # Bucle grupo sanguíneo
    grupos_validos = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    while True:
        grupo_sanguineo = input("Grupo sanguíneo (A+, A-, B+, B-, AB+, AB-, O+, O-): ").strip().upper()
        if grupo_sanguineo in grupos_validos:
            break
        else:
            print("Grupo sanguíneo inválido. Intente nuevamente.")

    # Teléfono
    telefono = input_entero("Teléfono: ")

    # Bucle centro de salud
    centro_salud = None
    while not centro_salud:
        nombre_centro = input("Nombre del centro de salud: ")
        centro_salud = obtener_centro_salud(incucai, nombre_centro)
        if not centro_salud:
            print("Centro no encontrado. Verifique el nombre.")

    # Bucle fecha hora fallecimiento (no ablación)
    fecha_hora_fallecimiento = None
    while not fecha_hora_fallecimiento:
        fallecimiento_input = input("Fecha y hora de fallecimiento (YYYY-MM-DD HH:MM): ")
        fecha_hora_fallecimiento = validar_fecha(fallecimiento_input, "%Y-%m-%d %H:%M")

    # Agregar selección de órganos a donar
    organos_validos = ["corazon", "pulmon", "piel", "corneas", "huesos", "higado", "riñon", "intestinos"]
    organos_donante = []

    print("\nSeleccione los órganos a donar (escriba 'fin' para terminar):")
    print(f"Órganos disponibles: {', '.join(organos_validos)}")

    while True:
        organo = input("Órgano: ").strip().lower()
        if organo == 'fin':
            if not organos_donante:
                print("Debe seleccionar al menos un órgano.")
                continue
            break
        elif organo in organos_validos:
            from organos.Organos import Organos
            organos_donante.append(Organos(organo))
            print(f"Órgano '{organo}' agregado.")
        else:
            print(f"Órgano inválido. Debe ser uno de: {', '.join(organos_validos)}")

    # Crear el donante con los parámetros correctos según el constructor
    # Constructor: (nombre, DNI, sexo, nacimiento, Tsangre, telefono, fhfallecimiento, organos_a_donar)
    nuevo_donante = Donantes(
        nombre,
        dni,
        sexo,
        fecha_nacimiento,
        grupo_sanguineo,
        telefono,
        fecha_hora_fallecimiento,
        organos_donante  # Asignar la lista de órganos
    )

    # Asignar el centro al donante
    nuevo_donante.centro_de_salud = centro_salud
    nuevo_donante.partido = centro_salud.partido
    nuevo_donante.provincia = centro_salud.provincia

    # Agregar a las listas
    incucai.lista_donantes.append(nuevo_donante)
    centro_salud.lista_pacientes.append(nuevo_donante)

    print(f"\nDonante agregado correctamente.")
    print(f"Órganos a donar: {', '.join([org.tipo_de_organo for org in organos_donante])}")


def consultar_resultado_trasplante(incucai: INCUCAI):
    """
    Busca el resultado de trasplante para un paciente (receptor o donante) por DNI.
    Muestra información detallada sobre el estado del trasplante.
    """
    try:
        dni_buscado = int(input("Ingrese el DNI del paciente: "))
    except ValueError:
        print("DNI inválido. Debe ser un número.")
        return

    # Buscar en todos los centros de salud
    for centro in incucai.centros_salud:
        # Buscar en pacientes exitosos
        for paciente in centro.pacientes_exitosos:
            if paciente.DNI == dni_buscado:
                print(f" TRASPLANTE EXITOSO")
                print(f"Paciente: {paciente.nombre}")
                print(f"DNI: {paciente.DNI}")
                print(f"Órgano trasplantado: {paciente.organo_a_recibir}")
                print(f"Centro de salud: {centro.nombre}")
                return

        # Buscar en pacientes fallidos
        for paciente in centro.pacientes_fallidos:
            if paciente.DNI == dni_buscado:
                print(f" TRASPLANTE FALLIDO")
                print(f"Paciente: {paciente.nombre}")
                print(f"DNI: {paciente.DNI}")
                print(f"Órgano que necesitaba: {paciente.organo_a_recibir}")
                print(f"Centro de salud: {centro.nombre}")
                return

    # Si no se encontró en exitosos/fallidos, buscar si existe como receptor
    receptor_encontrado = None
    for receptor in incucai.lista_receptores:
        if receptor.DNI == dni_buscado:
            receptor_encontrado = receptor
            break

    if receptor_encontrado:
        # Verificar si tiene órganos a disposición
        if hasattr(receptor_encontrado, 'organos_a_disposicion') and receptor_encontrado.organos_a_disposicion:
            print(f" RECEPTOR EN PROCESO")
            print(f"Paciente: {receptor_encontrado.nombre}")
            print(f"DNI: {receptor_encontrado.DNI}")
            print(f"Órgano necesario: {receptor_encontrado.organo_a_recibir}")
            print(f"Estado: Órgano compatible encontrado, pendiente de cirugía")
            print(
                f"Centro de salud: {receptor_encontrado.centro_de_salud.nombre if receptor_encontrado.centro_de_salud else 'No asignado'}")
        else:
            print(f" RECEPTOR EN ESPERA")
            print(f"Paciente: {receptor_encontrado.nombre}")
            print(f"DNI: {receptor_encontrado.DNI}")
            print(f"Órgano necesario: {receptor_encontrado.organo_a_recibir}")
            print(f"Estado: En lista de espera, sin órgano compatible disponible")
            print(
                f"Centro de salud: {receptor_encontrado.centro_de_salud.nombre if receptor_encontrado.centro_de_salud else 'No asignado'}")
        return

    # Buscar si existe como donante
    donante_encontrado = None
    for donante in incucai.lista_donantes:
        if donante.DNI == dni_buscado:
            donante_encontrado = donante
            break

    if donante_encontrado:
        print(f" DONANTE REGISTRADO")
        print(f"Paciente: {donante_encontrado.nombre}")
        print(f"DNI: {donante_encontrado.DNI}")
        if hasattr(donante_encontrado, 'organos_a_donar') and donante_encontrado.organos_a_donar:
            organos = [organo.tipo_de_organo for organo in donante_encontrado.organos_a_donar]
            print(f"Órganos disponibles para donación: {', '.join(organos)}")
        else:
            print("Órganos ya donados o no disponibles")
        print(
            f"Centro de salud: {donante_encontrado.centro_de_salud.nombre if donante_encontrado.centro_de_salud else 'No asignado'}")
        return

    print(" No se encontró ningún paciente (receptor o donante) con ese DNI.")


def procesar_nuevos_trasplantes(incucai: INCUCAI):
    """
    Procesa los nuevos pacientes agregados para buscar compatibilidades
    y ejecutar trasplantes pendientes.
    """
    print(" Procesando nuevos trasplantes...")

    # Procesar todos los pacientes en los centros de salud
    pacientes_procesados = 0

    for centro in incucai.centros_salud:
        for paciente in centro.lista_pacientes[:]:  # Crear copia para iterar seguro
            if isinstance(paciente, Receptores):
                # Verificar si ya está en la lista de receptores de INCUCAI
                if paciente not in incucai.lista_receptores:
                    incucai.lista_receptores.append(paciente)

                # Buscar compatibilidad si no tiene órganos asignados
                if not hasattr(paciente, 'organos_a_disposicion') or not paciente.organos_a_disposicion:
                    if incucai.buscar_compatibilidad_receptor_a_donante(paciente):
                        tiempo = centro.asignar_y_mandar_vehiculo(paciente)
                        if tiempo is not None:
                            centro.asignar_cirujano_y_operar(paciente, tiempo)
                            pacientes_procesados += 1

            elif isinstance(paciente, Donantes):
                # Verificar si ya está en la lista de donantes de INCUCAI
                if paciente not in incucai.lista_donantes:
                    incucai.lista_donantes.append(paciente)

                # Buscar receptor compatible
                receptor_encontrado = incucai.buscar_compatibilidad_donante_a_receptor(paciente)
                if receptor_encontrado is not None:
                    tiempo = centro.asignar_y_mandar_vehiculo(receptor_encontrado)
                    if tiempo is not None:
                        centro.asignar_cirujano_y_operar(receptor_encontrado, tiempo)
                        pacientes_procesados += 1

    if pacientes_procesados > 0:
        print(f" Se procesaron {pacientes_procesados} nuevos trasplantes.")
    else:
        print(" No se encontraron nuevas compatibilidades para procesar.")

def limpiar_terminal():
    """
    Limpia la terminal dependiendo del sistema operativo
    """
    # Para Windows
    if os.name == 'nt':
        os.system('cls')
    # Para Mac y Linux
    else:
        os.system('clear')


def pausa():
    """
    Pausa la ejecución hasta que el usuario presione Enter
    """
    input("\nPresione Enter para continuar...")


def mostrar_menu():
    """
    Muestra el menú principal
    """
    print(f'''
-----INCUCAI SISTEMA DE TRANSPLANTES-----

        \n1. Ver lista de receptores
        \n2. Ver lista de donantes
        \n3. Ver centros de salud
        \n4. Agregar nuevo receptor
        \n5. Agregar nuevo donante
        \n6. Resultado transplante
        \n7. Salir del programa''')


def menu(incu: INCUCAI):
    while True:
        limpiar_terminal()  # Limpiar al inicio
        mostrar_menu()  # Mostrar menú

        opcion = input("\nElija una opcion: ")

        if opcion == "1":
            limpiar_terminal()
            listas_receptores_por_centro(incu)
            pausa()

        elif opcion == "2":
            limpiar_terminal()
            listas_donantes(incu)
            pausa()

        elif opcion == "3":
            limpiar_terminal()
            listas_centros_salud(incu)
            pausa()

        elif opcion == "4":
            limpiar_terminal()
            agregar_receptor(incu)
            # Procesar automáticamente después de agregar
            procesar_nuevos_trasplantes(incu)
            pausa()

        elif opcion == "5":
            limpiar_terminal()
            agregar_donante(incu)
            # Procesar automáticamente después de agregar
            procesar_nuevos_trasplantes(incu)
            pausa()

        elif opcion == "6":
            limpiar_terminal()
            consultar_resultado_trasplante(incu)
            pausa()

        elif opcion == "7":
            limpiar_terminal()
            print("Saliendo del sistema...")
            break

        else:
            limpiar_terminal()
            print("Opción no válida. Elegí nuevamente.")
            pausa()
                
                