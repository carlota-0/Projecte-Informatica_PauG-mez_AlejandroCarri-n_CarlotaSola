import math
from airport import *

class Aircraft:
    def __init__(self, id, company, origin_airport="", time_of_landing="", destination_airport="", time_of_departure=""):
        self.id = id
        self.company = company
        self.origin_airport = origin_airport
        self.time_of_landing = time_of_landing
        self.destination_airport = destination_airport
        self.time_of_departure = time_of_departure

def LoadArrivals (filename):
    #incializar la lista que se devuelve con todas las llegadas
    Arrivals = []
    #hacer un recorrido de todas las líneas del fichero que contiene las llegas y extraer su informacion para construir un objeto Aircraft y añadirlo a la lista de Arrivals
    try:
        fitxer = open(filename, 'r')
        fitxer.readline()
        linea=fitxer.readline()
        while linea != '':
            elements = linea.split()
            id=str(elements[0])
            origin_airport = str(elements[1])
            time_of_landing = str(elements[2])
            company = str(elements[3])
            informacion=Aircraft(id, company, origin_airport, time_of_landing)
            Arrivals.append(informacion)
            linea = fitxer.readline()
        fitxer.close()
    #en caso de no existir el archivo se devuelve una lista vacía, si existe entonces se devuelve Aircrafts
    except FileNotFoundError:
        return []
    return Arrivals

def LoadDepartures(filename):
    # incializar la lista que se devuelve con todas las salidas
    Departures = []
    #hacer un recorrido de todas las líneas del fichero que contiene las salidas y extraer su informacion para construir un objeto Aircraft y añadirlo a la lista de Departures
    try:
        fitxer = open(filename, 'r')
        fitxer.readline()  # Skip the header line
        linea = fitxer.readline()

        while linea != '':
            elements = linea.split()

            # Comprobamos que la línea tiene al menos 4 datos antes de leer
            if len(elements) >= 4:
                id = str(elements[0])
                destination_airport = str(elements[1])
                time_of_departure = str(elements[2])
                company = str(elements[3])

                # Initialize the aircraft leaving the arrival parameters empty
                informacion = Aircraft(id, company, origin_airport="", time_of_landing="", destination_airport=destination_airport, time_of_departure=time_of_departure)
                Departures.append(informacion)

            linea = fitxer.readline()

        fitxer.close()
    #en caso de no existir el archivo se devuelve una lista vacía, si existe entonces se devuelve Departures
    except FileNotFoundError:
        return []

    return Departures

def SaveFlights(aircrafts, filename):
    fitxer = open(filename, 'w')
    for aircraft in aircrafts:
        fitxer.write(f'{aircraft.id, aircraft.origin_airport, aircraft.time_of_landing, aircraft.company}\n')
    fitxer.close()
    print("S'han guardat les dades a " +filename)

def PlotFlightsType(aircrafts):
    ''' Receives a list of aircraft and shows a stacked bar plot of the number of
    flights arriving from Schengen countries and the number of non-Schengen
    '''
    schengen = 0
    #contar Schengen
    for i in range (len(aircrafts)):
        if IsSchengenAirport(aircrafts[i].origin_airport):
            schengen += 1
    #definir no Schengen
    noSchengen = len(aircrafts)-schengen
    #crear un gráfico de una sola columna apilada donde se muestran la cantidad de vuelos schengen y no schengen
    fig = Figure()
    ax = fig.add_subplot(111)

    ax.bar(["Vuelos"], schengen, label="Schengen", color="#458B73")
    ax.bar(["Vuelos"], noSchengen, bottom=schengen, label="No Schengen", color="#F26076")

    ax.set_title("Comparación vuelos Schengen y no-Schengen", family="monospace", weight="bold", size="medium")
    ax.set_ylabel('Número de vuelos')

    ax.legend()

    return fig

def PlotArrivals(aircrafts):
    #definir una lista Horas y llenarla con los números del 0 al 23 (24h ya son las Oh del día siguiente)
    horas = []
    for i in range (24):
        horas.append(i)
    #definir una lista vuelos donde se cuentan el número de vuelos que hay por franja de horas 0-1, 1-2...
    vols = [0] * len(horas)
    #contar vuelos por hora (solo aviones con hora de llegada)
    for i in range (len(aircrafts)):
        if not aircrafts[i].time_of_landing:
            continue
        horacompleta = aircrafts[i].time_of_landing
        horacompleta = horacompleta.split(":")
        hora = int(horacompleta[0])
        vols[hora] = vols[hora] + 1
    #definir el gráfico
    fig = Figure()
    ax = fig.add_subplot(111)

    marcas = []
    for i in range (len(horas)):
        if horas[i]%2 == 0 or horas[i] == 0:
            marcas.append(horas[i])
    ax.bar(horas, vols, color="#458B73")
    ax.set_xticks(marcas)
    ax.set_title("Distribución de los vuelos entrantes por hora", family="monospace", weight="bold", size="medium")
    ax.set_xlabel('Franjas horarias de vuelos')
    ax.set_ylabel('Número de vuelos')

    return fig

def PlotAirlines(aircrafts):
    #definir una lista con todas las aerolíneas distintas
    aerolineas = []

    for i in range (len(aircrafts)):
        k = 0
        encontrado = False
        while k < len(aerolineas) and not encontrado:
            if aircrafts[i].company == aerolineas[k]:
                encontrado = True
            if not encontrado:
                k += 1
        if not encontrado:
            aerolineas.append(aircrafts[i].company)
    #contar vuelos de cada aerolínea
    vols = [0] * len(aerolineas)

    for i in range (len(aerolineas)):
        for k in range (len(aircrafts)):
            if aircrafts[k].company == aerolineas[i]:
                vols[i] += 1

    #definir gráfico
    fig = Figure()
    ax = fig.add_subplot(111)

    ax.bar(aerolineas, vols, color="#458B73")
    ax.set_title("Número de vuelos por compañía", family="monospace", weight="bold", size="medium")
    ax.set_xlabel('Aerolíneas')
    ax.set_ylabel('Número de vuelos')
    ax.tick_params(axis='x', labelsize=6, labelrotation=90)

    print(len(aerolineas))

    return fig

def MapFlights(aircrafts, airports):
    '''Shows in Google Earth the trajectories of all flights in the list, from
    origin airport to LEBL.txt. Show in different colors the trajectories with origin
    in a Schengen country. Remember that Annex A explains how to draw lines in
    Google Earth.
    '''
    #coordenades LEBL
    lonLEBL = 2.08
    latLEBL = 41.30
    #inicializar fichero kml + defnir estilos
    fitxer = open("Vuelos.kml", "w")
    fitxer.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n\t<Document>\n')
    fitxer.write('<Style id="color_schengen"><LineStyle><color>ff00ff00</color><width>2</width></LineStyle></Style>\n')
    fitxer.write('<Style id="color_noschengen"><LineStyle><color>ff0000ff</color><width>2</width></LineStyle></Style>\n')
    #recorrido de la lista de aviones donde se mira si el aeropuerto de origen es schengen o no para dibujar una línea de un color u otro (se verifica que el aeropuerto esté en el listado)
    for i in range (len(aircrafts)):
        origen = str(aircrafts[i].origin_airport)

        encontrado = False
        k = 0
        while k < len(airports) and not encontrado:
            if origen == airports[k].ICAO:
                encontrado = True
            elif not encontrado:
                k += 1
        if encontrado:
            lonOrigen = airports[k].longitude
            latOrigen = airports[k].latitude
            if IsSchengenAirport(origen):
                estilo = "#color_schengen"
            else:
                estilo = "#color_noschengen"

            fitxer.write(f'\t\t<Placemark>\n'
                         f'\t\t\t<name>Vuelo {origen} - LEBL.txt</name>\n'
                         f'\t\t\t<styleUrl>{estilo}</styleUrl>\n'
                         f'\t\t\t<LineString>\n'
                         f'\t\t\t\t<altitudeMode>clampToGround</altitudeMode>\n'
                         f'\t\t\t\t<extrude>1</extrude>\n'
                         f'\t\t\t\t<tessellate>1</tessellate>\n'
                         f'\t\t\t\t<coordinates>\n'
                         f'\t\t\t\t\t{lonOrigen},{latOrigen}\n'
                         f'\t\t\t\t\t{lonLEBL},{latLEBL}\n'
                         f'\t\t\t\t</coordinates>\n'
                         f'\t\t\t</LineString>\n'
                         f'\t\t</Placemark>\n')
        elif not encontrado:
            print(f'{aircrafts[i].origin_airport}, de l avió {aircrafts[i]} no està a la llista d aeroports')
    #cieere documento
    fitxer.write('\t</Document>\n</kml>')
    fitxer.close()

def LongDistanceArrivals(aircrafts,airports):
    '''Returns a list with the aircrafts from the input list of aircrafts that
    arrive to LEBL.txt from an airport that is more that 2000 Km away (this aircraft
    would need special inspection after landing).
    You will need a function to compute the Haversine3 distance between two
    coordinates.
    '''
    #coordenadas LEBL convertidas a radianes + radio de la tierra en metros
    lonLEBL = math.radians(2.08)
    latLEBL = math.radians(41.30)
    r = 6371
    #inicializar lista que será el resultado de la función donde estarán todos los vuelos de larga distancia
    largaDistancia = []
    #recorrer toda las lista de vuelos y buscar primero si el aeropuerto está dentro del listaod de aeropuertos o no y después calcular su distancia a LEBL; si es mayor a 2000km se añade a la lista
    for i in range(len(aircrafts)):
        origen = str(aircrafts[i].origin_airport)

        encontrado = False
        k = 0
        while k < len(airports) and not encontrado:
            if origen == airports[k].ICAO:
                encontrado = True
            else:
                k += 1
        if encontrado:
            lonOrigen = airports[k].longitude
            latOrigen = airports[k].latitude

            lonOrigen = math.radians(lonOrigen)
            latOrigen = math.radians(latOrigen)

            deltaLon = abs(lonOrigen - lonLEBL) / 2
            deltaLat = abs(latOrigen - latLEBL) / 2

            a = (math.sin(deltaLat)) ** 2 + math.cos(latLEBL) * math.cos(latOrigen) * (math.sin(deltaLon) ** 2)

            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

            d = r * c
            if d > 2000:
                largaDistancia.append(aircrafts[i])
        elif not encontrado:
            print(f'{aircrafts[i].origin_airport}, de l avió {aircrafts[i]} no està a la llista d aeroports')
    #la función devuelve una nueva lista con los vuelos de larga distáncia
    return largaDistancia

def MergeMovements (arrivals, departures): #[Pau]
    ''' This function receives two lists of aircraft (arrivals and departures) and
    returns a new list of aircrafts in which the data of the aircraft with the
    same id and with compatible times are merged into the same Aircraft structure.
    Times are compatible when the arrival time is previous to the departure time.
    Remember that some aircrafts may not have a departure and others may not have
    an arrival in the day (night aircraft). If some of the input lists is empty an
    error code shall be returned. IMPORTANT: an aircraft can land and take-off
    more than once at LEBL during the same day.
    '''
    #comprobar que no hay listas vacías y devolver un código de error si lo están
    if arrivals == [] or departures == []:
        return -1

    # lista para marcar qué despegues ya han sido emparejados
    matched = []
    i = 0
    while i < len(departures):
        matched.append(False)
        i += 1

    resultado = []

    # recorrer  llegadas
    i = 0
    while i < len(arrivals):
        id_buscar = arrivals[i].id
        t_llegada = arrivals[i].time_of_landing
        encontrado = False
        j = 0

        #buscar unsa salida
        while j < len(departures) and not encontrado:
            if not matched[j] and departures[j].id == id_buscar and t_llegada < departures[j].time_of_departure:
                #crear un nuevo objeto de la clase Aircraft con los datos combinados
                nuevo = Aircraft(id=id_buscar, company=arrivals[i].company, origin_airport=arrivals[i].origin_airport, time_of_landing=arrivals[i].time_of_landing, destination_airport=departures[j].destination_airport, time_of_departure=departures[j].time_of_departure)
                resultado.append(nuevo)
                matched[j] = True
                encontrado = True
            j += 1

        # Si no se encontró despegue compatible, añadir solo la llegada
        if not encontrado:
            resultado.append(arrivals[i])

        i += 1

    # Añadir los despegues que no fueron emparejados (night aircraft que solo salen)
    j = 0
    while j < len(departures):
        if not matched[j]:
            resultado.append(departures[j])
        j += 1

    return resultado

# Gràfic TOP 5 aerolinies més significatives
''' 
def PlotAirlinesSignificatives(aircrafts):

    aerolineasTotals = []

    for i in range (len(aircrafts)):
        k = 0
        encontrado = False
        while k < len(aerolineasTotals) and not encontrado:
            if aircrafts[i].company == aerolineasTotals[k]:
                encontrado = True
            if not encontrado:
                k += 1
        if not encontrado:
            aerolineasTotals.append(aircrafts[i].company)

    volsTotals = [0] * len(aerolineasTotals)

    for i in range (len(aerolineasTotals)):
        for k in range (len(aircrafts)):
            if aircrafts[k].company == aerolineasTotals[i]:
                volsTotals[i] += 1

    aerolineas = [""] * 5
    vols = [0] * len(aerolineas)

    for i in range(len(volsTotals)):
        for k in range(5):
            if volsTotals[i] > vols[k]:
                j = 4
                while j > k:
                    vols[j] = vols[j - 1]
                    aerolineas[j] = aerolineas[j - 1]
                    j -= 1
                vols[k] = volsTotals[i]
                aerolineas[k] = aerolineasTotals[i]
                break

# --- añadir una barra de la suma de las demás aerolíneas --- 
    aerolineas.append("Otras")
    otros = 0
    for i in range (len(aerolineasTotals)):
        encontrado = False
        for k in range (5):
            if aerolineasTotals[i] == aerolineas[k]:
                encontrado = True
        if not encontrado:
            otros = volsTotals[i]+otros
    vols.append(otros)
# -------------------------------------------------------------

# gráfico 
    fig = Figure()
    ax = fig.add_subplot(111)

    ax.bar(aerolineas, vols, color="#458B73")
    ax.set_title("Número de vuelos por compañía (TOP5)", family="monospace", weight="bold", size="medium")
    ax.set_xlabel('Aerolíneas')
    ax.set_ylabel('Número de vuelos')
    ax.tick_params(axis='x', labelsize=10, labelrotation=0)

    print(len(aerolineas))

    return fig
'''

# test section
