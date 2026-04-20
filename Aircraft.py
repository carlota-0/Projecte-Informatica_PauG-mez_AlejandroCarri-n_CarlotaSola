import math
from airport import *

class Aircraft:
    def __init__(self, id, company, origin_airport, time_of_landing):
        self.id=id
        self.company=company
        self.origin_airport=origin_airport
        self.time_of_landing=time_of_landing

def __repr__(self):
    return f"[{self.id} - {self.company} - {self.origin_airport} - {self.time_of_landing}]"

def LoadArrivals (filename):
    Arrivals = []
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

    except FileNotFoundError:
        return []
    return Arrivals

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

    fig = Figure()
    ax = fig.add_subplot(111)

    ax.bar(["Vuelos"], schengen, label="Schengen", color="#458B73")
    ax.bar(["Vuelos"], noSchengen, bottom=schengen, label="No Schengen", color="#F26076")

    ax.set_title("Comparación vuelos Schengen y no-Schengen", family="monospace", weight="bold", size="medium")
    ax.set_ylabel('Número de vuelos')

    ax.legend()

    return fig

def PlotArrivals(aircrafts):
    try:
        horas = []
        for i in range (24):
            horas.append(i)

        vols = [0] * len(horas)

        for i in range (len(aircrafts)):
            horacompleta = aircrafts[i].time_of_landing
            horacompleta = horacompleta.split(":")
            hora = int(horacompleta[0])
            vols[hora] = vols[hora] + 1

        fig = Figure()
        ax = fig.add_subplot(111)

        marcas = []
        for i in range (len(horas)):
            if horas[i]%2 == 0 or horas[i] == 0:
                marcas.append(horas[i])
        ax.bar(horas, vols, color="#458B73")
        ax.set_xticks(marcas)
        ax.set_title("Comparación vuelos Schengen y no-Schengen", family="monospace", weight="bold", size="medium")
        ax.set_xlabel('Franjas horarias de vuelos')
        ax.set_ylabel('Número de vuelos')

        return fig
    except ValueError:
        print("Error en los datos")

def MapFlights(aircrafts, airports):
    '''Shows in Google Earth the trajectories of all flights in the list, from
    origin airport to LEBL. Show in different colors the trajectories with origin
    in a Schengen country. Remember that Annex A explains how to draw lines in
    Google Earth.
    '''

    lonLEBL = 2.08
    latLEBL = 41.30

    fitxer = open("Vuelos.kml", "w")
    fitxer.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n\t<Document>\n')
    fitxer.write('<Style id="color_schengen"><LineStyle><color>ff00ff00</color><width>2</width></LineStyle></Style>\n')
    fitxer.write('<Style id="color_noschengen"><LineStyle><color>ff0000ff</color><width>2</width></LineStyle></Style>\n')
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
                         f'\t\t\t<name>Vuelo {origen} - LEBL</name>\n'
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

    fitxer.write('\t</Document>\n</kml>')
    fitxer.close()

def LongDistanceArrivals(aircrafts):
    '''Returns a list with the aircrafts from the input list of aircrafts that
    arrive to LEBL from an airport that is more that 2000 Km away (this aircraft
    would need special inspection after landing).
    You will need a function to compute the Haversine3 distance between two
    coordinates.
    '''

    lonLEBL = math.radians(2.08)
    latLEBL = math.radians(41.30)
    r = 6371

    largaDistancia = []

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

    return largaDistancia