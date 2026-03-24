import matplotlib.pyplot as plt

class Airport:
    def __init__(self, ICAO, latitude, longitude):
        self.ICAO = ICAO
        self.latitude = latitude
        self.longitude = longitude
        self.Schengen = False

def IsSchengenAirport (code):
    '''Receives the ICAO code of an airport and checks if the airport is in an
    Schengen country. The countries which signed the Schengen agreement are
    Austria, Belgium, Czech Republic, Cyprus, Denmark, Estonia, Finland, France,
    Germany, Greece, Netherlands, Hungary, Iceland, Italy, Latvia, Lithuania,
    Luxemburg, Malta, Norway, Poland, Portugal, Slovakia, Slovenia, Spain, Sweden
    and Switzerland. To know if an airport belongs to any of these countries you
    have to check if the first 2 characters of the ICAO code are one of the
    following codes which correspond to the above list of countries:
    'LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
    'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS'
    The function returns a boolean that is True if the airport belongs to a
    Schengen country, and False otherwise. If the input parameter is empty then
    False is returned.'''
    codigos = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    encontrado = False
    i = 0

    while i < len(codigos) and not encontrado:
        if codigos[i] == code[0:2]:
            encontrado = True
        else:
            i +=1

    if encontrado:
        return True
    elif not encontrado:
        return False
    return None

def SetSchengen (airport):
    # Receives an airport and sets the Schengen attribute (True or False). Uses the IsSchengenAirport function
    airport.Schengen = IsSchengenAirport(airport.ICAO)

def PrintAirport (airport):
    # Prints in console the data of the airport
     return (f'ICAO: {airport.ICAO}\t\tLAT: {airport.latitude:05.2f}\t\tLON: {airport.longitude:05.2f}\t\tSchengen? {IsSchengenAirport(airport.ICAO)}')

def LoadAirports (filename):
    '''Opens the file with name received as input and with the format described
    below, with a header line and an airport per line, and returns a list of
    airports with the data found in the file. Convert the format of latitude and
    longitude from string to decimal degrees (float that will be negative for West
    and South coordinates). In the file you will not find any data about Schengen,
    so do not update this field of the structure. If the file does not exist the
    function returns an empty list.'''
    aeropuertos = []
    try:
        fitxer = open(filename, 'r')
        fitxer.readline()
        linia = fitxer.readline()
        while linia != "":
            elements = linia.split()
            icao = str(elements[0])
            lat = round(float(elements[1][-2:])/3600 + float(elements[1][-4:-2])/60 + float(elements[1][1:-4]),2)
            lon = round(float(elements[2][-2:])/3600 + float(elements[2][-4:-2])/60 + float(elements[2][1:-4]),2)
            #conversió lat
            if elements[1][0] == "S":
                lat = -1*lat
            # conversió lon
            if elements[2][0] == "W":
                lon = -1*lon

            provisional = Airport(icao, lat, lon)
            SetSchengen(provisional)
            aeropuertos.append(provisional)
            linia = fitxer.readline()
        fitxer.close()
    except FileNotFoundError:
        return []
    return aeropuertos

def SaveSchengenAirports (airports, filename):
    '''Given a list of airports, this function writes the information of the
    airports that are Schengen into a file whose name is in filename. The format
    of the output file must be the same as the format of the input file described
    above. If the vector is empty no file is created and an error code is
    returned.'''
    if airports == []:
        print("Lista de aeropuertos vacía")
        return None
    else:
        aeroportsSchengen = []
        for i in range (len(airports)):
            if IsSchengenAirport(airports[i].ICAO):
                aeroportsSchengen.append(airports[i])

        fitxer = open(filename, 'w')
        fitxer.write("CODE LAT LON\n")
        for j in range(len(aeroportsSchengen)):
            icao = aeroportsSchengen[j].ICAO
            lat = str(aeroportsSchengen[j].latitude)
            lon = str(aeroportsSchengen[j].longitude)
            fitxer.write(icao + " " + lat + " " + lon + "\n")
        fitxer.close()
        return fitxer

def AddAirport (airports, airport):
    '''Adds the airport to the list of airports if the airport is not in
    the list.
    '''
    encontrado = False
    i = 0
    while i < len(airports) and not encontrado:
        if airports[i].ICAO == airport.ICAO:
            encontrado = True
        else:
            i +=1
    if encontrado:
        print("El aeropuerto ya existe")
        return 5
    elif not encontrado:
        SetSchengen(airport)
        airports.append(airport)
        print("El aeropuerto añadido")
        return airports

def RemoveAirport (airports, code):
    ''' Remove from the list of airports the airport whose code is received as parameter
    If the airport is not in the list an error code is returned.'''
    encontrado = False
    i = 0
    num = len(airports)
    while i < num and not encontrado:
        if airports[i].ICAO == code:
            encontrado = True
        if not encontrado:
            i +=1
    if encontrado: # suprimir
        while i < num-1:
            airports[i] = airports[i+1]
            i = i+1
        airports.pop()
        return airports
    elif not encontrado:
        print("El aeropuerto no existe")
        return None

def PlotAirports (airports):
    '''Shows a plot of type stacked bar with
    Schen gen and non-Schengen airports (see the figure)'''

    schengen = 0
    #contar Schengen
    for i in range (len(airports)):
        if IsSchengenAirport(airports[i].ICAO):
            schengen += 1
    #definir no Schengen
    noSchengen = len(airports)-schengen

    plt.bar(["Airports"], schengen, label="Schengen", color="#458B73")
    plt.bar(["Airports"], noSchengen, bottom=schengen, label="No Schengen", color="#F26076")

    plt.title("Schengen airports")

    plt.ylabel('Count')

    plt.legend()

    plt.show()

def MapAirports (airports):
    '''Shows in Google Earth the
    airports in the list. Use different
    colors to show Schengen airports
    and no Schengen airports. See Annex
    A to learn how to show info in
    Google Earth.'''
    fitxer = open("Ubicaciones.kml", "w")
    fitxer.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n\t<Document>\n')
    fitxer.write('<Style id="color_schengen"><IconStyle><color>ff00ff00</color></IconStyle></Style>\n')
    fitxer.write('<Style id="color_noschengen"><IconStyle><color>ff0000ff</color></IconStyle></Style>\n')
    for i in range (len(airports)):
        icao = str(airports[i].ICAO)
        lat = airports[i].latitude
        lon = airports[i].longitude

        if IsSchengenAirport(icao):
            estilo = "#color_schengen"
        else:
            estilo = "#color_noschengen"

        fitxer.write(f'\t\t<Placemark>\n'
                     f'\t\t\t<name>{icao}</name>\n'
                     f'\t\t\t<styleUrl>{estilo}</styleUrl>\n'
                     f'\t\t\t<Point>\n'
                     f'\t\t\t\t<coordinates>{lon},{lat}</coordinates>\n'
                     f'\t\t\t</Point>\n'
                     f'\t\t</Placemark>\n')

    fitxer.write('\t</Document>\n</kml>')
    fitxer.close()

