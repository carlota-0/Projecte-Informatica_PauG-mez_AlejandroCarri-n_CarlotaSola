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
