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
        # leer la primera linea del archivo para extarer ICAO aeropuerto y nº terminales
        linea = f.readline()
        trozos = linea.split(' ')
        # obtener ICAO aeropuerto
        nombre_aeropuerto = trozos[0]
        # creacion objeto de la clase BarcelonaAP con el ICAO obtenido
        aeropuerto = Barcelona_AP(nombre_aeropuerto)
        # obtencion lista terminales
        terminales = []
        for i in range(int(trozos[1])):
            provTerminal = Terminal(f'T{i + 1}')
            terminales.append(provTerminal)
        # incluir temrinales en el objeto aeropuerto
        aeropuerto.terminals = terminales
        # cargar icaos de aerolineas para cada terminal
        for i in range(len(aeropuerto.terminals)):
            LoadAirlines(terminales[i], terminales[i].name)

        # cargar boarding areas de cada terminal + asignar gates
        linea = f.readline()
        i = -1
        while linea != '':
            trozos = linea.split(' ')
            if trozos[0] == 'Terminal':
                i += 1
            else:
                provBoarding = Boarding_area(trozos[1], trozos[2])
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
    is not occupied in the correct boarding area. To decide the correct boarding area the function must check the
    airlineterminal assignment (using the SearchTerminal function defined above) and the Schengen/non-Schengen type
    of flight-boarding area. The gate assignment consists in updating the occupancy boolean and the aircraft field
    of the chosen gate inside the bcn parameter. If there is not more free gates of the correct type, an error code
    shall be returned and no modification of the bcn parameter shall be done.'''

    aerolineaAircraft = aircraft.company
    terminal = SearchTerminal(bcn, aerolineaAircraft)

    terminales = bcn.terminals
    find = False
    indiceTerminal = 0
    try:
        if terminal == "":
            print("Aerolínea no encontrada en las terminales.")
            return None

        # buscar si la terminal está en algún archivo
        while not find and indiceTerminal < len(terminales):
            if terminal == terminales[indiceTerminal].name:
                find = True
            elif not find:
                indiceTerminal += 1

        origen = aircraft.origin_airport
        Schengen = IsSchengenAirport(origen)
        num = len(bcn.terminals[indiceTerminal].Boarding_area)
        listBoardingAreas = []
        if Schengen:
            for i in range(num):
                if bcn.terminals[indiceTerminal].Boarding_area[i].area == "Schengen":
                    listBoardingAreas.append(bcn.terminals[indiceTerminal].Boarding_area[i])
        elif not Schengen:
            for i in range(num):
                if bcn.terminals[indiceTerminal].Boarding_area[i].area == "non-Schengen":
                    listBoardingAreas.append(bcn.terminals[indiceTerminal].Boarding_area[i])

        j = 0
        gate = None
        encontrado = False
        while not encontrado and j < len(listBoardingAreas):
            k = 0
            while not encontrado and k < len(listBoardingAreas[j].Gate):
                if not listBoardingAreas[j].Gate[k].occupied:
                    encontrado = True
                    gate = listBoardingAreas[j].Gate[k]
                elif not encontrado:
                    k += 1
            if not encontrado:
                j += 1

        if encontrado:
            gate.occupied = True
            gate.aircraft_id = aircraft.id
            return True
        elif not encontrado:
            print('No hay gates libres')
            return None
    except IndexError:
        print('Error error en el array')
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
    ''' BONUS: Builds a plot showing the terminals, boarding areas,
    and the status of each gate (Free/Occupied).
    '''
    import matplotlib.pyplot as plt

    # Creamos un gráfico grande para que quepan todas las puertas
    fig, ax = plt.subplots(figsize=(14, 8))

    y_labels = []
    y_ticks = []
    current_y = 0
    area_y_map = {}

    # 1. Asignamos una altura (eje Y) a cada Área de Embarque (ej. "T1 - Area A")
    for item in occupancy_list:
        area_key = f"{item['terminal']} - Area {item['area']}"
        if area_key not in area_y_map:
            area_y_map[area_key] = current_y
            y_labels.append(area_key)
            y_ticks.append(current_y)
            current_y += 1

    # Listas para separar las puertas libres de las ocupadas
    x_free, y_free = [], []
    x_occ, y_occ = [], []

    # 2. Posicionamos cada puerta en el mapa
    for item in occupancy_list:
        # Extraemos el número de la puerta (Ej: de "T1BAAG11" sacamos el 11)
        gate_num = int(item['gate_name'].split('G')[-1])
        area_key = f"{item['terminal']} - Area {item['area']}"
        y_coord = area_y_map[area_key]

        if item['occupied']:
            x_occ.append(gate_num)
            y_occ.append(y_coord)
            # Dibujamos el ID del avión un poco por encima de la puerta roja
            ax.text(gate_num, y_coord + 0.2, item['aircraft_id'],
                    fontsize=8, ha='center', va='bottom', rotation=45, color='black')
        else:
            x_free.append(gate_num)
            y_free.append(y_coord)

    # 3. Dibujamos los "cuadraditos" de las puertas
    ax.scatter(x_free, y_free, c='#2ECC71', label='Libre', s=100, marker='s', edgecolors='black', alpha=0.7)
    ax.scatter(x_occ, y_occ, c='#E74C3C', label='Ocupada', s=100, marker='s', edgecolors='black', alpha=0.9)

    # 4. Formato visual del panel
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('Número de Puerta', fontsize=12, fontweight='bold')
    ax.set_title('Panel de Ocupación de Puertas - LEBL.txt', fontsize=16, fontweight='bold')
    ax.legend(loc='upper right')

    plt.grid(axis='x', linestyle='--', alpha=0.4)  # Cuadrícula vertical para guiarse mejor
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


def AssignNightGates(bcn, aircrafts):  # [Pau]
    ''' This function receives an object of class BarcelonaAP, bcn, and a list of
    aircraft. It assigns a gate to each of the aircraft in the list. Use the new
    version of function AssignGate. Check that the aircrafts in the list are only
    departure flights, with empty data related to arrival. In case an aircraft
    does not meet the condition then skip to the following aircraft in list. If
    the input list is empty return an error code.
    '''
    return None


def AssignGatesAtTime(bcn, aircrafts, time):
    '''This function receives an object of class BarcelonaAP, bcn, and a list of aircraft. It assigns a gate
    to each of the aircraft in the list. Use the new version of function AssignGate. Check that the aircrafts
    in the list are only departure flights, with empty data related to arrival. In case an aircraft does not
    meet the condition then skip to the following aircraft in list. If the input list is empty return an error code.'''

    unassigned_count = 0
    current_hour = time.split(':')[0]  # Extrau "14" de "14:00", per exemple

    # Primer
    for terminal in bcn.terminals:
        for area in terminal.Boarding_area:
            for gate in area.Gate:
                if gate.occupied:
                    # Trobem l'avió que ocupa la porta
                    for ac in aircrafts:
                        if ac.id == gate.aircraft_id:
                            # Si la hora de "departure" ja ha passat
                            if ac.time_of_departure != "" and ac.time_of_departure <= time:
                                gate.occupied = False
                                gate.aircraft_id = ""
                            break  # Seguim amb la següent porta

    # Asignem portes en els trams de 1h
    for ac in aircrafts:
        if ac.time_of_landing != "":
            ac_hour = ac.time_of_landing.split(':')[0]

            # Si el nou avuió d'arribada està en el tram que estem tractan...
            if ac_hour == current_hour:
                success = AssignGate(bcn, ac)

                if success is None:
                    unassigned_count += 1

    return unassigned_count
