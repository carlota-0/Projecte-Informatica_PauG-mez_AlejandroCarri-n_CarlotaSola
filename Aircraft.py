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
