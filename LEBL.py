from Aircraft import *


class Barcelona_AP:
    def __init__(self, code):
        self.code = code
        self.terminals = []

class Terminal:
    def __init__(self, name):
        self.name = name
        self.ICAO = []
        self.Boarding_area = []

class Boarding_area:
    def __init__(self, name, area):
        self.name = name
        self.area = area
        self.Gate = []

class Gate:
    def __init__(self, name):  # comencem només amb això perquè la demés informació podria estar buida si no hi ha avió.
        self.name = name
        self.occupied = False
        self.aircraft_id = None

def SetGate(area, init_gate, end_gate, prefix):
    area.Gate = []
    '''
    for element in (init_gate, end_gate+1):
        if init_gate>=end_gate:
            return (-1)
        name= f"{prefix}{element}"
        new_gate = Gate(name)
        area.Gate.append(new_gate)'''
    for i in range(int(init_gate), int(end_gate) + 1):
        name = f"{prefix}{i}"
        new_gate = Gate(name)
        area.Gate.append(new_gate)


def LoadAirlines(terminal, t_name):
    nombre_archivo = f"{t_name}_Airlines.txt"
    try:
        fitxer = open(nombre_archivo, 'r')
        terminal.ICAO = []
        for linea in fitxer:
            elementos = linea.split()

            if len(elementos) > 0:
                codigo_icao = elementos[-1]  # para coger la última palabra de la linea

                terminal.ICAO.append(codigo_icao)

        fitxer.close()

    except FileNotFoundError:
        return [-1]


def SearchTerminal(bcn, name):
    ''' Given bcn of class BarcelonaAP and the name of one airline, this function
    returns the name of the terminal where the airline must board its passengers.
    Use function IsAirlineInTerminal. If the airline is not found in any of the
    terminals, the return name shall be a null string.
    '''
    i = 0
    encontrado = False
    terminales = bcn.terminals
    while not encontrado and i < len(terminales):
        if IsAirlineInTerminal(terminales[i], name):
            encontrado = True
        elif not IsAirlineInTerminal(terminales[i], name):
            i += 1
    if encontrado:
        return terminales[i].name
    else:
        return ""


def LoadAirportStructure(filename):
    ''' Crea y devuelve un objeto BarcelonaAP leyendo la estructura del archivo.
    Si el archivo no existe, devuelve None como código de error.
    '''
    try:
        f = open(filename, 'r')
        linea = f.readline()
        trozos = linea.split(' ')
        nombre_aeropuerto = trozos[0]
        aeropuerto = Barcelona_AP(nombre_aeropuerto)
        terminales = []
        for i in range(int(trozos[1])):
            provTerminal = Terminal(f'T{i + 1}')
            terminales.append(provTerminal)
        aeropuerto.terminals = terminales

        for i in range(len(aeropuerto.terminals)):
            LoadAirlines(terminales[i], terminales[i].name)

        linea = f.readline()
        i = -1
        while linea != '':
            # Usamos strip para limpiar cualquier salto de línea residual antes de separar
            linea_limpia = linea.strip()
            if linea_limpia:
                trozos = linea_limpia.split(' ')
                if trozos[0] == 'Terminal':
                    i += 1
                else:
                    # Aplicamos .strip() al tipo de área (Schengen / non-Schengen) para eliminar caracteres ocultos
                    tipo_area = trozos[2].strip()
                    provBoarding = Boarding_area(trozos[1], tipo_area)
                    SetGate(provBoarding, trozos[-3], trozos[-1], f'T{i + 1}BA{trozos[1]}')
                    aeropuerto.terminals[i].Boarding_area.append(provBoarding)
            linea = f.readline()

        f.close()
        return aeropuerto

    except FileNotFoundError:
        print(f"Error crítico: No se encontró el archivo '{filename}'.")
        return None


def AssignGate(bcn, aircraft):
    '''Given bcn of class BarcelonaAP and an aircraft of class Aircraft this function looks for the first gate that
    is not occupied in the correct boarding area...'''

    aerolineaAircraft = aircraft.company
    terminal = SearchTerminal(bcn, aerolineaAircraft)

    terminales = bcn.terminals
    find = False
    indiceTerminal = 0
    try:
        if terminal == "":
            return None

        # Buscar el índice de la terminal correspondiente
        while not find and indiceTerminal < len(terminales):
            if terminal == terminales[indiceTerminal].name:
                find = True
            elif not find:
                indiceTerminal += 1

        # --- CORRECCIÓN INTELIGENTE DE FRONTERA SCHENGEN ---
        # Si el avión tiene origen, evaluamos el origen.
        # Si el origen está vacío (avión pernoctador que solo sale), evaluamos su destino.
        if hasattr(aircraft, 'origin_airport') and aircraft.origin_airport != "":
            origen_evaluar = aircraft.origin_airport
        else:
            origen_evaluar = getattr(aircraft, 'destination_airport', "")

        # Si ambos campos están vacíos por algún error de datos, por defecto es Schengen
        if origen_evaluar == "":
            Schengen = True
        else:
            Schengen = IsSchengenAirport(origen_evaluar)
        # ----------------------------------------------------

        num = len(bcn.terminals[indiceTerminal].Boarding_area)
        listBoardingAreas = []

        # Filtramos las áreas limpiando saltos de línea con .strip()
        if Schengen:
            for i in range(num):
                if bcn.terminals[indiceTerminal].Boarding_area[i].area.strip() == "Schengen":
                    listBoardingAreas.append(bcn.terminals[indiceTerminal].Boarding_area[i])
        else:
            for i in range(num):
                if bcn.terminals[indiceTerminal].Boarding_area[i].area.strip() == "non-Schengen":
                    listBoardingAreas.append(bcn.terminals[indiceTerminal].Boarding_area[i])

        # --- ASIGNACIÓN DE PUERTAS EQUILIBRADA ---
        # Para evitar que la zona M se coma todo el tráfico y la R se quede vacía,
        # si hay más de un área disponible (como M y R), podemos distribuir los aviones
        # de forma alternativa usando el ID del avión (o su matrícula).
        j = 0
        if len(listBoardingAreas) > 1:
            # Si el último carácter de la matrícula del avión es un número par o letra par,
            # intentamos empezar a buscar por la segunda zona (Área R) para balancear la carga.
            try:
                if ord(aircraft.id[-1]) % 2 == 0:
                    j = 1
            except:
                j = 0

        gate = None
        encontrado = False
        intentos_areas = 0

        # Recorremos las áreas de embarque de forma circular para asegurar el reparto real
        while not encontrado and intentos_areas < len(listBoardingAreas):
            area_actual = listBoardingAreas[j % len(listBoardingAreas)]
            k = 0
            while not encontrado and k < len(area_actual.Gate):
                if not area_actual.Gate[k].occupied:
                    encontrado = True
                    gate = area_actual.Gate[k]
                else:
                    k += 1
            j += 1
            intentos_areas += 1

        if encontrado:
            gate.occupied = True
            gate.aircraft_id = aircraft.id
            return True
        else:
            return None

    except IndexError:
        return None

def GateOccupancy(bcn):
    ''' Given a BarcelonaAP object, returns a list of dictionaries with
    gate names, status, and aircraft id.
    '''
    occupancy_list = []

    # Recorremos la jerarquía completa: Aeropuerto -> Terminales -> Áreas -> Puertas
    for terminal in bcn.terminals:
        for area in terminal.Boarding_area:
            for gate in area.Gate:
                # Guardamos la info de forma estructurada
                puerta_info = {
                    'terminal': terminal.name,
                    'area': area.name,
                    'gate_name': gate.name,
                    'occupied': gate.occupied,
                    'aircraft_id': gate.aircraft_id
                }
                occupancy_list.append(puerta_info)

    return occupancy_list


def PlotGateOccupancy(occupancy_list):
    ''' BONUS OPTIMIZADO: Construye un gráfico separando el Área B
    en dos filas para que no se corten las puertas en la pantalla.
    '''
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(15, 9))  # Aumentamos un pelín el tamaño del lienzo

    y_labels = []
    y_ticks = []
    current_y = 0
    area_y_map = {}

    # 1. PASO PREVIO: Registrar las filas en el eje Y (incluyendo la fila extra para el Área B)
    for item in occupancy_list:
        terminal = item['terminal']
        area = item['area']

        # Si es el Área B, vamos a mirar el número de la puerta para decidir su fila
        if terminal == "T1" and area == "B":
            try:
                gate_num = int(item['gate_name'].split('G')[-1])
            except:
                gate_num = 0

            # Dividimos el Área B: Puertas hasta la 35 en la fila principal, el resto a la de continuación
            if gate_num <= 35:
                area_key = f"{terminal} - Area {area}"
            else:
                area_key = f"{terminal} - Area {area} (Cont.)"
        else:
            # Para el resto de áreas (A, C, M, R, S), mantenemos su comportamiento normal
            area_key = f"{terminal} - Area {area}"

        if area_key not in area_y_map:
            area_y_map[area_key] = current_y
            y_labels.append(area_key)
            y_ticks.append(current_y)
            current_y += 1

    # Listas para guardar las posiciones de los cuadraditos
    x_free, y_free = [], []
    x_occ, y_occ = [], []

    # 2. Posicionar cada puerta en su coordenada correspondiente
    for item in occupancy_list:
        try:
            gate_num = int(item['gate_name'].split('G')[-1])
        except:
            continue

        terminal = item['terminal']
        area = item['area']

        # Aplicamos la misma regla de división para pintar los puntos en el lugar correcto
        if terminal == "T1" and area == "B" and gate_num > 35:
            area_key = f"{terminal} - Area {area} (Cont.)"
        else:
            area_key = f"{terminal} - Area {area}"

        y_coord = area_y_map[area_key]

        if item['occupied']:
            x_occ.append(gate_num)
            y_occ.append(y_coord)
            # Dibujamos el ID del avión con una rotación bonita para que no se solapen
            ax.text(gate_num, y_coord + 0.15, item['aircraft_id'],
                    fontsize=7, ha='center', va='bottom', rotation=45, color='black', fontweight='bold')
        else:
            x_free.append(gate_num)
            y_free.append(y_coord)

    # 3. Dibujamos los "cuadraditos" de las puertas (reducimos el tamaño 's' de 100 a 70 para que quepan mejor)
    ax.scatter(x_free, y_free, c='#2ECC71', label='Libre', s=70, marker='s', edgecolors='black', alpha=0.8)
    ax.scatter(x_occ, y_occ, c='#E74C3C', label='Ocupada', s=70, marker='s', edgecolors='black', alpha=0.9)

    # 4. Formato visual de la interfaz del gráfico
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=10, fontweight='bold')
    ax.set_xlabel('Número de Puerta', fontsize=12, fontweight='bold')
    ax.set_title('Panel de Ocupación de Puertas de Embarque (LEBL)', fontsize=15, fontweight='bold', pad=15)
    ax.legend(loc='upper right', frameon=True, shadow=True)

    # Añadimos líneas de rejilla tanto verticales como horizontales muy suaves para guiar la vista
    plt.grid(axis='both', linestyle='--', alpha=0.3)

    # Ajustamos los límites de la pantalla para dar espacio a los textos de los aviones arriba
    ax.set_ylim(-0.5, current_y - 0.5)

    plt.tight_layout()
    plt.show()

def IsAirlineInTerminal(terminal, name):
    ''' Given terminal of class Terminal and the name of one airline, this
    function returns True if the airline is in the list of airlines boarding in
    this terminal and False otherwise.
    '''
    # 1. Comprobar si el nombre de la aerolínea es un string nulo/vacío
    if name == "" or name is None:
        print("Error: El nombre de la aerolínea no puede estar vacío.")
        return False

    # 2. Comprobar si la terminal tiene una lista de aerolíneas vacía
    if not terminal.ICAO:
        return False

    # 3. Comprobar si la aerolínea está en la lista
    if name in terminal.ICAO:
        return True
    else:
        return False


# ==========================================
#         FUNCIONES DE LA VERSIÓN 4
# ==========================================

def NightAircraft(aircrafts):
    """
    Recibe una lista de aviones y devuelve una nueva lista con los aviones "pernoctadores"
    (aquellos que NO tienen datos de llegada, pero SÍ tienen datos de salida).
    Si la lista de entrada está vacía, devuelve un código de error (por ejemplo, -1).
    """
    if not aircrafts:
        print("Error: La lista de aeronaves está vacía.")
        return -1

    night_list = []
    for ac in aircrafts:
        # Un avión pernoctó si no tiene origen/hora de llegada, pero sí tiene destino/salida
        # Ajusta 'origin_airport' y 'destination_airport' según los nombres exactos de tu clase Aircraft
        tiene_llegada = hasattr(ac, 'origin_airport') and ac.origin_airport != ""
        tiene_salida = hasattr(ac, 'destination_airport') and ac.destination_airport != ""

        if tiene_salida and not tiene_llegada:
            night_list.append(ac)

    return night_list


def FreeGate(bcn, aircraft_id):
    """
    Busca un avión por su ID en todas las puertas del aeropuerto bcn.
    Si lo encuentra, libera la puerta (occupied = False, aircraft_id = "") y termina.
    """
    found = False

    # Recorremos usando TUS nombres exactos de variables: terminals -> Boarding_area -> Gate
    for terminal in bcn.terminals:
        for area in terminal.Boarding_area:  # <--- Cambiado a tu formato
            for gate in area.Gate:  # <--- Cambiado a tu formato
                # Nota: Si en tu clase Gate, 'occupied' o 'aircraft_id' van en mayúsculas,
                # cámbialos aquí abajo también (ej: gate.Occupied o gate.Aircraft_id)
                if hasattr(gate, 'occupied') and gate.occupied and getattr(gate, 'aircraft_id', '') == aircraft_id:
                    gate.occupied = False
                    gate.aircraft_id = ""
                    found = True
                    break
                elif hasattr(gate, 'Occupied') and gate.Occupied and getattr(gate, 'Aircraft_id', '') == aircraft_id:
                    gate.Occupied = False
                    gate.Aircraft_id = ""
                    found = True
                    break
            if found: break
        if found: break

    if not found:
        print(f"Error: El avión {aircraft_id} no se encontró en ninguna puerta.")
        return -1

    return 0  # Éxito


def AssignNightGates(bcn, aircrafts):
    # 1. Agrupamos todos los vuelos por matrícula (ID) para analizar su comportamiento real
    historial_aviones = {}
    for ac in aircrafts:
        if ac.id not in historial_aviones:
            historial_aviones[ac.id] = {"llegadas": [], "salidas": [], "objeto": ac}

        if getattr(ac, "time_of_landing", None):
            historial_aviones[ac.id]["llegadas"].append(ac.time_of_landing)
        if getattr(ac, "time_of_departure", None):
            historial_aviones[ac.id]["salidas"].append(ac.time_of_departure)

    contador_nocturnos = 0
    aviones_procesados = set()  # Para evitar procesar la misma matrícula dos veces

    # 2. Recorremos los aviones para ver quiénes califican como "Pernoctadores"
    for ac in aircrafts:
        id_avion = ac.id
        if id_avion in aviones_procesados:
            continue

        datos = historial_aviones.get(id_avion, {"llegadas": [], "salidas": [], "objeto": ac})

        es_pernoctador = False

        # REGLA 1: Tiene una salida programada, pero NUNCA llegó hoy (estaba desde ayer)
        if len(datos["salidas"]) > 0 and len(datos["llegadas"]) == 0:
            es_pernoctador = True

        # REGLA 2: Tiene llegada y salida, pero su primera salida ocurre ANTES de su primera llegada
        elif len(datos["salidas"]) > 0 and len(datos["llegadas"]) > 0:
            primera_salida = sorted(datos["salidas"])[0]
            primera_llegada = sorted(datos["llegadas"])[0]
            if primera_salida < primera_llegada:
                es_pernoctador = True

        # 3. SOLO si es pernoctador, le buscamos la puerta reglamentaria
        if es_pernoctador:
            aviones_procesados.add(id_avion)
            # 🔥 CORRECCIÓN CRÍTICA: Usamos vuestra función de asignación reglamentaria
            # para respetar aerolíneas y fronteras Schengen, en lugar de llenar todo al azar
            success = AssignGate(bcn, datos["objeto"])
            if success is not None:
                contador_nocturnos += 1

    # Imprimimos el recuento real en consola
    print(f"Asignación nocturna completada: {contador_nocturnos} aviones asignados de forma reglamentaria.")

    #  CORRECCIÓN CRÍTICA 2: Devolvemos el número para que Tkinter no muestre 'None'
    return contador_nocturnos


def AssignGatesAtTime(bcn, aircrafts, time):
    '''
    Versión Avanzada de Simulación Continua SIN DUPLICADOS.
    Mantiene los aviones en las puertas de embarque desde que aterrizan
    hasta el minuto exacto de su despegue.
    '''
    unassigned_count = 0

    # 1. LIBERACIÓN DE PUERTAS (Aviones que despegan en este minuto exacto)
    for terminal in bcn.terminals:
        for area in terminal.Boarding_area:
            for gate in area.Gate:
                if gate.occupied and gate.aircraft_id:
                    # Buscamos el vuelo en la lista para comprobar su hora de salida
                    for ac in aircrafts:
                        if ac.id == gate.aircraft_id:
                            if ac.time_of_departure != "" and ac.time_of_departure == time:
                                gate.occupied = False
                                gate.aircraft_id = None
                            break

    # 2. ASIGNACIÓN CONTINUA (Aviones que aterrizan en este minuto exacto)
    for ac in aircrafts:
        if ac.time_of_landing != "" and ac.time_of_landing == time:

            # CONTROL DE DUPLICADOS: Comprobamos si este avión ya tiene una puerta asignada
            ya_esta_en_puerta = False
            for terminal in bcn.terminals:
                for area in terminal.Boarding_area:
                    for gate in area.Gate:
                        if gate.aircraft_id == ac.id:
                            ya_esta_en_puerta = True
                            break

            # Solo si el avión no está duplicado en el aeropuerto, le asignamos puerta
            if not ya_esta_en_puerta:
                success = AssignGate(bcn, ac)
                if success is None:
                    unassigned_count += 1

    return unassigned_count