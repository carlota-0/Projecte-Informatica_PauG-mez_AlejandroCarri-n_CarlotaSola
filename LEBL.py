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
    def __init__(self,name, area):
        self.name = name
        self.area = area
        self.Gate = []

class Gate:
    def __init__(self,name):    #comencem només amb això perquè la demés informació podria estar buida si no hi ha avió.
        self.name = name
        self.occupied = False
        self.aircraft_id = None

def SetGate (area, init_gate, end_gate, prefix):
    area.gates=[]
    for element in (init_gate, end_gate+1):
        if init_gate>=end_gate:
            return (-1)
        name= f"{prefix}{element}"
        new_gate = Gate(name)
        area.gates.append(new_gate)

def LoadAirlines (terminal, t_name):
    nombre_archivo = f"{t_name}_Airlines.txt"
    try:
        fitxer = open(nombre_archivo, 'r')
        terminal.icao_codes = []
        for linea in fitxer:
            elementos = linea.split()

            if len(elementos) > 0:
                codigo_icao = elementos[-1] #para coger la última palabra de la linea

                terminal.icao_codes.append(codigo_icao)

        fitxer.close()

    except FileNotFoundError:
        return [-1]

def SearchTerminal (bcn, name):
    ''' Given bcn of class BarcelonaAP and the name of one airline, this function
    returns the name of the terminal where the airline must board its passengers.
    Use function IsAirlineInTerminal. If the airline is not found in any of the
    terminals, the return name shall be a null string.
    '''
    i = 0
    encontrado = False
    terminales = bcn.terminals
    while not encontrado:
        if IsAirlineInTerminal(terminals[i], name):
            encontrado = True
        elif not IsAirlineInTerminal(terminals[i], name):
            i += 1
    if encontrado:
        return terminales[i]
    else:
        return ""

def AssignGate (bcn, aircraft):
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
        while not find and indiceTerminal < len(terminales):
            if terminal == terminales[indiceTerminal]:
                find = True
            elif not find:
                indiceTerminal += 1


        origen = aircraft.origin_airport
        Schengen = IsSchengenAirport(origen)
        num = len(bcn.terminals[indiceTerminal].Boarding_area)
        listBoardingAreas = []
        if Schengen:
            for i in range (num):
                if bcn.terminals[indiceTerminal].Boarding_area[i].area == "Schengen" :
                    listBoardingAreas.append(bcn.terminals[indiceTerminal].Boarding_area[i])
        elif not Schengen:
            for i in range (num):
                if bcn.terminals[indiceTerminal].Boarding_area[i].area == "NoSchengen" :
                    listBoardingAreas.append(bcn.terminals[indiceTerminal].Boarding_area[i])

        j = 0
        gate = ""
        encontrado = False
        while not encontrado and j < len(listBoardingAreas):
            k = 0
            while not encontrado and k < len(listBoardingAreas[j].Gate):
                if listBoardingAreas[j].Gate[k].occupied == False:
                    encontrado = True
                    gate = listBoardingAreas[j].Gate[k]
                elif not encontrado:
                    k += 1
            if not encontrado:
                j += 1

        if encontrado:
            gate.occupied = True
            gate.aircraft_id = aircraft.id
        elif not encontrado:
            print('No hay gates libres')
            return None
    except IndexError:
        print('Error error en el array')
        return None