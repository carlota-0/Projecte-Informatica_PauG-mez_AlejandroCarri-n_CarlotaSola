from airport import *
from Aircraft import *
from LEBL import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import sys
import subprocess

aircrafts = []
departures_list = []
aeropuertos = []
bcn = None
canvas = None

# ------ FUNCIONES ------
#Funcions V1
def mostrar_aeropuertos():
    #mostrar todos los aeropuertos en el listado
    listado.delete(0, 'end')
    for i in range(len(aeropuertos)):
        listado.insert(tk.END, PrintAirport(aeropuertos[i]))
    return None
def anadir():
    #añadir un aeropuerto a la lista
    if entry_icao.get() != "" and entry_lat.get() != "" and entry_lon.get() != "":
        try:
            icao = entry_icao.get()
            lat = float(entry_lat.get())
            lon = float(entry_lon.get())
            temporal = Airport(icao, lat, lon)
            if AddAirport(aeropuertos, temporal) == 5:
                messagebox.showinfo('Aeropuerto ya en el listado', 'El aeropuerto ya estaba añadido')
            else:
                AddAirport(aeropuertos, temporal)
                messagebox.showinfo('Aeropuerto añadido', 'El aeropuerto ha sido añadido')
            mostrar_aeropuertos()
            limpiar_formulario()
        except ValueError:
            messagebox.showerror('Error', 'Error en los datos introducidos')
    else:
        messagebox.showerror('Error','Faltan datos del aeropuerto')
def suprimir():
    #eliminar un aeropuerto de la lista
    if entry_icao.get() != "":
        spr_icao = entry_icao.get()
        if RemoveAirport(aeropuertos, spr_icao) is None:
            messagebox.showerror('Error', 'Aeropuerto no encontrado')
        else:
            mostrar_aeropuertos()
            limpiar_formulario()
    else:
        messagebox.showerror('Error','Falta el ICAO del aeropuerto a eliminar')
def importar_archivo():
    #cargar aeropuertos desde un archivo
    file_path = filedialog.askopenfilename(
        title="Seleccione un archivo",
        filetypes=(("Archivos CSV", "*.txt"), ("Todos los archivos", "*.*"))
    )
    if not file_path:
        return None
    provisional = LoadAirports(file_path)
    nuevos = 0
    for i in range(len(provisional)):
        encontrado = False
        j = 0
        while j < (len(aeropuertos)) and not encontrado:
            if aeropuertos[j].ICAO == provisional[i].ICAO:
                encontrado = True
            else:
                j += 1
        if not(encontrado):
            aeropuertos.append(provisional[i])
            nuevos += 1
    mostrar_aeropuertos()
    messagebox.showinfo('Aeropuertos cargados', f'Se cargaron {nuevos} aeropuertos')
    return None
def graficoAeropuertos():
    #mostrar gráfico de aeropuertos Schengen/No-Schengen
    if aeropuertos:
        global canvas, canvas_graficos
        fig = PlotAirports(aeropuertos)
        fig.set_size_inches(1, 1)
        fig.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.10)
        #fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame_graficos)

        if 'canvas_graficos' in globals():
            canvas_graficos.grid_forget()
        canvas_graficos = canvas.get_tk_widget()
        canvas_graficos.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.E+tk.W, padx = 15, pady = 15)
        #canvas_graficos.grid(row = 0, column = 0, padx = 15, pady = 15)

        canvas.draw()
    else:
        messagebox.showerror('Error','La lista de aeropuertos está vacía')
def archivo_Schengen():
    #guardar aeropuertos Schengen en un archivo .txt
    SaveSchengenAirports(aeropuertos,"Schengen.txt")
    if aeropuertos:
        messagebox.showinfo('Archivo guardado','Se ha guardado un archivo Schengen.txt')
    else:
        messagebox.showwarning('Archivo no guardado', 'No hay aeropuertos para guardar')
    return None
def map_airports():
    #mostrar aeropuertos en Google Earth
    if aeropuertos:
        try:
            if not MapAirports(aeropuertos):
                messagebox.showerror('Error', 'No se pudo crear el archivo KML')
                return

            archivo = "Ubicaciones.kml"
            if sys.platform == "win32":
                os.startfile(archivo)
            elif sys.platform == "darwin":
                subprocess.call(["open", archivo])
        except (OSError, subprocess.SubprocessError):
            messagebox.showerror('Error','No tienes Google Earth instalado, prueba a abrirlo en el navegador y cargar el archivo \"Ubicaciones.kml\"')
    else:
        messagebox.showerror('Error','Lista de aeropuertos vacía')
def limpiar_formulario():
    #limpiar los campos de entrada
    entry_icao.delete(0, 'end')
    entry_lon.delete(0, 'end')
    entry_lat.delete(0, 'end')

#Funcions V2
def mostrar_vuelos():
    #mostrar todos los vuelos en el listado
    listadovuelos.delete(0, 'end')
    for i in range(len(aircrafts)):
        org = aircrafts[i].origin_airport if aircrafts[i].origin_airport else "---"
        lleg = aircrafts[i].time_of_landing if aircrafts[i].time_of_landing else "---"
        dst = aircrafts[i].destination_airport if aircrafts[i].destination_airport else "---"
        sal = aircrafts[i].time_of_departure if aircrafts[i].time_of_departure else "---"
        listadovuelos.insert(tk.END, f'ID: {aircrafts[i].id}\t\tCompañía: {aircrafts[i].company}\t\tOrigen: {org}\t\tLlegada: {lleg}\t\tDestino: {dst}\t\tSalida: {sal}')
    return None
def cargar_vuelos():
    #cargar vuelos de llegada desde un archivo
    global aircrafts
    archivo = filedialog.askopenfilename(
        title="Seleccione un archivo",
        filetypes=(("Archivos CSV", "*.txt"), ("Todos los archivos", "*.*"))
    )
    if not archivo:
        return None
    provisional = LoadArrivals(archivo)
    nuevos = 0
    for i in range(len(provisional)):
        encontrado = False
        j = 0
        while j < (len(aircrafts)) and not encontrado:
            if aircrafts[j].id == provisional[i].id:
                encontrado = True
            else:
                j += 1
        if not(encontrado):
            aircrafts.append(provisional[i])
            nuevos += 1
    mostrar_vuelos()
    messagebox.showinfo('Llegadas cargadas', f'Se cargaron {nuevos} vuelos de llegada')
    if len(departures_list) > 0 and messagebox.askyesno('Combinar movimientos', 'Hay salidas cargadas. ¿Quiere combinar llegadas y salidas automáticamente?'):
        resultado = MergeMovements(aircrafts, departures_list)
        if resultado != -1:
            aircrafts = resultado
            mostrar_vuelos()
            messagebox.showinfo('Combinación completada', f'Movimientos combinados. Total: {len(aircrafts)} aeronaves')
def cargar_salidas():
    #cargar vuelos de salida desde un archivo
    global departures_list
    global aircrafts
    archivo = filedialog.askopenfilename(
        title="Seleccione un archivo de salidas",
        filetypes=(("Archivos CSV", "*.txt"), ("Todos los archivos", "*.*"))
    )
    if not archivo:
        return None
    departures_list = LoadDepartures(archivo)
    if len(departures_list) > 0:
        # Si aun no hay llegadas cargadas, mostrar las salidas en el listado
        if len(aircrafts) == 0:
            listadovuelos.delete(0, 'end')
            for i in range(len(departures_list)):
                dst = departures_list[i].destination_airport if departures_list[i].destination_airport else "---"
                sal = departures_list[i].time_of_departure if departures_list[i].time_of_departure else "---"
                listadovuelos.insert(tk.END, f'ID: {departures_list[i].id}\t\tCompañía: {departures_list[i].company}\t\tDestino: {dst}\t\tSalida: {sal}')
        messagebox.showinfo('Salidas cargadas', f'Se han cargado {len(departures_list)} salidas')
    else:
        messagebox.showwarning('Sin datos', 'El archivo no contenía datos de salidas')
    if len(aircrafts) > 0 and messagebox.askyesno('Combinar movimientos', 'Hay llegadas cargadas. ¿Quiere combinar salidas y llegadas automáticamente?'):
        resultado = MergeMovements(aircrafts, departures_list)
        if resultado != -1:
            aircrafts = resultado
            mostrar_vuelos()
            messagebox.showinfo('Combinación completada', f'Movimientos combinados. Total: {len(aircrafts)} aeronaves')
    return None
def fusionar_movimientos():
    #fusionar llegadas y salidas del mismo avión
    global aircrafts, departures_list
    if len(aircrafts) == 0:
        messagebox.showerror('Error', 'No hay vuelos de llegada cargados')
        return None
    if len(departures_list) == 0:
        messagebox.showerror('Error', 'No hay vuelos de salida cargados')
        return None
    resultado = MergeMovements(aircrafts, departures_list)
    if resultado == -1:
        messagebox.showerror('Error', 'Error al fusionar: listas vacías')
        return None
    aircrafts = resultado
    mostrar_vuelos()
    messagebox.showinfo('Fusión completada', f'Se han fusionado los movimientos. Total: {len(aircrafts)} aeronaves')
    return None
def exportar_vuelos():
    #exportar vuelos a un archivo
    archivo = filedialog.asksaveasfilename(
        title="Seleccione un archivo .txt",
        defaultextension=".txt",
        filetypes=(("Archivos de texto","*.txt"), ("Todos los archivos", "*.*"))
    )
    if not archivo:
        return
    if SaveFlights(aircrafts, archivo):
        messagebox.showinfo('Exportar', f'Vuelos guardados en {archivo}')
    else:
        messagebox.showerror('Error', 'No se pudo guardar el archivo')
def grafico_vuelosSchengen():
    #mostrar gráfico de vuelos Schengen/No-Schengen
    if aircrafts:
        global canvas, canvas_graficos
        fig = PlotFlightsType(aircrafts)
        fig.set_size_inches(1, 1)
        fig.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.10)
        #fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame_graficos)

        if 'canvas_graficos' in globals():
            canvas_graficos.grid_forget()
        canvas_graficos = canvas.get_tk_widget()
        canvas_graficos.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.E+tk.W, padx = 15, pady = 15)
        #canvas_graficos.grid(row = 0, column = 0, padx = 15, pady = 15)

        canvas.draw()
    else:
        messagebox.showerror('Error','La lista de vuelos está vacía')
def grafico_vuelosPorCompania():
    #mostrar gráfico de vuelos por compañía con opciones
    if not aircrafts:
        messagebox.showerror('Error','La lista de vuelos está vacía')
        return

    # --- pop-up para elegir modo ---
    top = tk.Toplevel(window)
    top.title("Tipo de gráfico")
    top.geometry("300x150")
    top.transient(window)
    top.grab_set()

    tk.Label(top, text="¿Qué gráfico desea?", font=("Arial", 11, "bold")).pack(pady=10)

    def elegir_top5():
        top.destroy()
        fig = PlotAirlinesSignificatives(aircrafts)
        mostrar_figura(fig)

    def elegir_seleccion():
        top.destroy()
        # --- pop-up de selección múltiple de aerolíneas ---
        aerolineas = sorted(set(ac.company for ac in aircrafts))

        sel = tk.Toplevel(window)
        sel.title("Seleccionar aerolíneas")
        sel.geometry("300x450")
        sel.transient(window)
        sel.grab_set()

        tk.Label(sel, text="Seleccione aerolíneas:", font=("Arial", 10, "bold")).pack(pady=(5, 0))

        busqueda_var = tk.StringVar()
        entry_busqueda = tk.Entry(sel, textvariable=busqueda_var, font=("Arial", 10))
        entry_busqueda.pack(fill=tk.X, padx=10, pady=5)
        entry_busqueda.focus_set()

        frame = tk.Frame(sel)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set, font=("Courier", 10))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        def actualizar_lista(*args):
            filtro = busqueda_var.get().lower()
            listbox.delete(0, tk.END)
            for a in aerolineas:
                if filtro in a.lower():
                    listbox.insert(tk.END, a)

        busqueda_var.trace_add("write", actualizar_lista)
        actualizar_lista()

        def confirmar():
            seleccionadas = [listbox.get(i) for i in listbox.curselection()]
            if not seleccionadas:
                messagebox.showerror("Error", "Debe seleccionar al menos una aerolínea")
                return
            sel.destroy()
            # preguntar si mostrar columna "Otras"
            if messagebox.askyesno("Resto de vuelos", "¿Mostrar columna con el resto de vuelos?"):
                fig = PlotAirlinesFiltered(aircrafts, seleccionadas, True)
            else:
                fig = PlotAirlinesFiltered(aircrafts, seleccionadas, False)
            mostrar_figura(fig)

        ttk.Button(sel, text="Aceptar", command=confirmar, width=15).pack(pady=10)

    ttk.Button(top, text="Top 5 aerolíneas + Otras", command=elegir_top5, width=25).pack(pady=5)
    ttk.Button(top, text="Seleccionar aerolíneas", command=elegir_seleccion, width=25).pack(pady=5)

def mostrar_figura(fig):
    #mostrar figura en el frame de gráficos
    global canvas, canvas_graficos
    fig.set_size_inches(1, 1)
    fig.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.10)

    canvas = FigureCanvasTkAgg(fig, master=frame_graficos)

    if 'canvas_graficos' in globals():
        canvas_graficos.grid_forget()
    canvas_graficos = canvas.get_tk_widget()
    canvas_graficos.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, padx=15, pady=15)

    canvas.draw()
def grafico_vuelosPorLlegada():
    #mostrar gráfico de vuelos por hora de llegada
    if aircrafts:
        global canvas, canvas_graficos
        fig = PlotArrivals(aircrafts)
        fig.set_size_inches(1, 1)
        fig.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.10)
        # fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame_graficos)

        if 'canvas_graficos' in globals():
            canvas_graficos.grid_forget()
        canvas_graficos = canvas.get_tk_widget()
        canvas_graficos.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, padx=15, pady=15)
        # canvas_graficos.grid(row = 0, column = 0, padx = 15, pady = 15)

        canvas.draw()
    else:
        messagebox.showerror('Error','La lista de vuelos está vacía')
def earth_largaDistancia():
    #mostrar vuelos de larga distancia en Google Earth
    if aircrafts and aeropuertos:
        try:
            MapFlights(LongDistanceArrivals(aircrafts,aeropuertos), aeropuertos)

            archivo = "Vuelos.kml"
            if sys.platform == "win32":
                os.startfile(archivo)
            elif sys.platform == "darwin":
                subprocess.call(["open", archivo])
        except (OSError, subprocess.SubprocessError):
            messagebox.showerror('Error','No tienes Google Earth instalado, prueba a abrirlo en el navegador y cargar el archivo \"Vuelos.kml\"')
    else:
        messagebox.showerror('Error', 'Faltan los datos de los vuelos, los datos de los aeropuertos o ambos')
def earth_vuelos():
    #mostrar todos los vuelos en Google Earth
    if aircrafts and aeropuertos:
        try:
            MapFlights(aircrafts, aeropuertos)

            archivo = "Vuelos.kml"
            if sys.platform == "win32":
                os.startfile(archivo)
            elif sys.platform == "darwin":
                subprocess.call(["open", archivo])
        except (OSError, subprocess.SubprocessError):
            messagebox.showerror('Error','No tienes Google Earth instalado, prueba a abrirlo en el navegador y cargar el archivo \"Vuelos.kml\"')
    else:
        messagebox.showerror('Error','Faltan los datos de los vuelos, los datos de los aeropuertos o ambos')

#Funcions V3
def cargar_estructura():
    #cargar estructura del aeropuerto desde un archivo
    archivo = filedialog.askopenfilename(
        title="Seleccione un archivo",
        filetypes=(("Archivos CSV", "*.txt"), ("Todos los archivos", "*.*"))
    )
    if not archivo:
        return None
    global bcn
    bcn = LoadAirportStructure(archivo)
    if bcn:
        mostrar_puertas()
    else:
        messagebox.showerror("Error", "No se pudo cargar la estructura del aeropuerto.")

    return None
def asignar_puertas():
    #asignar una puerta a cada vuelo
    if not aircrafts or not bcn:
        messagebox.showerror('Error', 'Listado de aviones vacío o falta estructura del aeropuerto')
    else:
        asignadas = 0
        for i in range (len(aircrafts)):
            if AssignGate(bcn, aircrafts[i]) is not None:
                asignadas += 1
        mostrar_puertas()
        messagebox.showinfo('Puertas asignadas', f'{asignadas} de {len(aircrafts)} vuelos tienen puerta asignada')
        return None
def mostrar_puertas():
    #mostrar estado de las puertas en el listado
    if bcn is None:
        return
    listadopuertas.delete(0, 'end')
    for j in range (len(bcn.terminals)):
        for i in range(len(bcn.terminals[j].Boarding_area)):
            for k in range(len(bcn.terminals[j].Boarding_area[i].Gate)):
                if bcn.terminals[j].Boarding_area[i].Gate[k].occupied:
                    listadopuertas.insert(tk.END, f'{bcn.terminals[j].Boarding_area[i].Gate[k].name}\t\t({bcn.terminals[j].Boarding_area[i].area})\t\tOcupada por {bcn.terminals[j].Boarding_area[i].Gate[k].aircraft_id}')
                else:
                    listadopuertas.insert(tk.END,f'{bcn.terminals[j].Boarding_area[i].Gate[k].name}\t\t({bcn.terminals[j].Boarding_area[i].area})\t\tLibre')
    return None
def asignar_puertas_nocturnas():
    #asignar puertas a aviones que pasan la noche
    if not aircrafts or not bcn:
        messagebox.showerror('Error', 'Listado de aviones vacío o falta estructura del aeropuerto')
    else:
        resultado = AssignNightGates(bcn, aircrafts)
        if resultado == -1:
            messagebox.showerror('Error', 'Error al asignar puertas nocturnas')
        else:
            messagebox.showinfo('Puertas nocturnas', f'Se asignaron {resultado} puertas a aviones nocturnos')
        mostrar_puertas()
        mostrar_vuelos()
    return None

#Funcion V4
def PlotDayOccupancy(bcn, aircrafts):
    #calcular ocupación de puertas en 24h y devolver figura
    import copy

    if not bcn or not aircrafts:
        return None

    bcn_copia = copy.deepcopy(bcn)
    terminal_names = [t.name for t in bcn_copia.terminals]
    ocupacion_por_terminal = {name: [0] * 24 for name in terminal_names}

    AssignNightGates(bcn_copia, aircrafts)

    for h_idx in range(24):
        for m in range(60):
            tiempo_sim_str = f"{str(h_idx).zfill(2)}:{str(m).zfill(2)}"
            AssignGatesAtTime(bcn_copia, aircrafts, tiempo_sim_str)

        for terminal in bcn_copia.terminals:
            count = 0
            for area in getattr(terminal, 'Boarding_area', []):
                for gate in getattr(area, 'Gate', []):
                    if getattr(gate, 'occupied', False):
                        count += 1
            ocupacion_por_terminal[terminal.name][h_idx] = count

    fig = Figure()
    ax = fig.add_subplot(111)
    for name, datos_hora in ocupacion_por_terminal.items():
        ax.plot(range(24), datos_hora, marker='o', linewidth=2, label=f"Terminal {name}")

    marcas = [h for h in range(24) if h % 3 == 0]
    ax.set_xticks(marcas)
    ax.set_xlabel("Hora (h)", fontweight='bold')
    ax.set_ylabel("Número de Puertas Ocupadas", fontweight='bold')
    ax.set_title("Evolución de la Ocupación\nen las 24 horas (LEBL)", fontsize=13, fontweight='bold', pad=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper left')
    fig.tight_layout()

    return fig
def MostrarMapaInteractivo(bcn, aircrafts):
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider, RadioButtons
    import matplotlib.patches as patches
    import sys
    import os
    import copy

    if not bcn or not aircrafts:
        from tkinter import messagebox
        messagebox.showerror('Error', 'Primero debes cargar el aeropuerto y los vuelos.')
        return
    if not bcn.terminals:
        messagebox.showerror('Error', 'El aeropuerto no tiene terminales cargadas.')
        return

    # =========================================================================
    # ⏱️ PRECALCULAR TODO EL DÍA MINUTO A MINUTO (Simulación limpia)
    # =========================================================================
    bcn_simulado = copy.deepcopy(bcn)

    # Vaciamos por completo el aeropuerto para empezar desde cero absoluto
    for t in bcn_simulado.terminals:
        for area in getattr(t, 'Boarding_area', []):
            for g in getattr(area, 'Gate', []):
                g.occupied = False
                g.aircraft_id = None

    # Cargamos los pernoctadores de la noche usando vuestra función corregida
    from LEBL import AssignNightGates, AssignGatesAtTime
    AssignNightGates(bcn_simulado, aircrafts)

    # Creamos la línea de tiempo de 24 horas (1440 minutos)
    historial_minutos = []

    for m in range(1440):
        horas = str(m // 60).zfill(2)
        mins = str(m % 60).zfill(2)
        tiempo_str = f"{horas}:{mins}"

        # Ejecutamos vuestra lógica minuto a minuto
        AssignGatesAtTime(bcn_simulado, aircrafts, tiempo_str)

        # Guardamos la foto exacta de este minuto
        historial_minutos.append(copy.deepcopy(bcn_simulado))

    # =========================================================================
    # 🎨 CONFIGURACIÓN DE LA VENTANA GRÁFICA
    # =========================================================================
    fig, ax = plt.subplots(figsize=(14, 7.5))
    plt.subplots_adjust(bottom=0.2, left=0.25)

    terminal_actual = bcn.terminals[0].name
    minutos_actuales = 0

    # =========================================================================
    # 🔄 RENDERIZADO DINÁMICO
    # =========================================================================
    def simular_y_draw():
        ax.clear()

        # Extraemos el estado del aeropuerto exacto de la línea de tiempo
        bcn_instante = historial_minutos[minutos_actuales]

        horas_str = str(minutos_actuales // 60).zfill(2)
        mins_str = str(minutos_actuales % 60).zfill(2)
        tiempo_actual_str = f"{horas_str}:{mins_str}"

        ax.set_title(f"Plano de Puertas Dinámico - {terminal_actual} - Hora {tiempo_actual_str}", fontsize=13,
                     fontweight='bold')
        slider_tiempo.valtext.set_text("")

        # Filtramos por la terminal que el usuario tenga seleccionada
        t_obj = next((t for t in bcn_instante.terminals if t.name == terminal_actual), bcn_instante.terminals[0])
        lista_areas = getattr(t_obj, 'Boarding_area', [])

        # Organizamos las filas visuales de 18 en 18 para que quepa en pantalla
        total_filas_necesarias = 0
        filas_por_area = []
        for area in lista_areas:
            num_puertas = len(getattr(area, 'Gate', []))
            filas_este_area = ((num_puertas - 1) // 18) + 1 if num_puertas > 0 else 1
            filas_por_area.append(filas_este_area)
            total_filas_necesarias += filas_este_area

        ax.set_xlim(-1.8, 21)
        ax.set_ylim(-1, total_filas_necesarias * 1.4)
        ax.axis('off')

        fila_actual_global = total_filas_necesarias - 1

        # Dibujamos los bloques correspondientes
        for i, area in enumerate(lista_areas):
            nombre_area = str(getattr(area, 'name', f'Area {i+1}')).strip()
            num_filas_area = filas_por_area[i]

            y_centro_etiqueta = (fila_actual_global - (num_filas_area - 1) / 2) * 1.4
            ax.text(-0.6, y_centro_etiqueta + 0.2, f"Área {nombre_area}", ha='right', va='center', fontsize=10,
                    fontweight='bold', color='#1a5f7a')

            for j, gate in enumerate(getattr(area, 'Gate', [])):
                subfila_dentro_area = j // 18
                columna = j % 18

                fila_render = fila_actual_global - subfila_dentro_area
                x_pos = columna * 1.15
                y_pos = fila_render * 1.4

                ocupado = getattr(gate, 'occupied', False) or getattr(gate, 'Occupied', False)
                ac_id = getattr(gate, 'aircraft_id', None) or getattr(gate, 'Aircraft_id', None)
                gate_name = str(getattr(gate, 'name', f'G{j+1}'))

                color = '#dc2626' if ocupado else '#10b981'
                rect = patches.Rectangle((x_pos, y_pos), 0.95, 0.6, linewidth=1, facecolor=color, edgecolor='white')
                ax.add_patch(rect)

                if ocupado and ac_id:
                    ax.text(x_pos + 0.47, y_pos + 0.3, str(ac_id)[:5], ha='center', va='center', fontsize=6,
                            color='white', fontweight='bold', rotation=30)
                else:
                    num_limpio = gate_name.split('G')[-1] if 'G' in gate_name else str(j + 1)
                    ax.text(x_pos + 0.47, y_pos + 0.3, num_limpio, ha='center', va='center', fontsize=7, color='white',
                            alpha=0.8)

            fila_actual_global -= num_filas_area
        fig.canvas.draw_idle()

    # =========================================================================
    # 🎛️ CONTROLES MATPLOTLIB
    # =========================================================================
    ax_slider = plt.axes([0.3, 0.05, 0.55, 0.03], facecolor='lightgray')
    slider_tiempo = Slider(ax_slider, 'Tiempo del día', 0, 1439, valinit=0, valstep=1)

    ax_radio = plt.axes([0.02, 0.4, 0.16, 0.2], facecolor='lightgray')
    nombres_terminales = [t.name for t in bcn.terminals]
    radio_terminal = RadioButtons(ax_radio, nombres_terminales)

    def update_slider(val):
        nonlocal minutos_actuales
        minutos_actuales = int(slider_tiempo.val)
        simular_y_draw()

    def update_radio(label):
        nonlocal terminal_actual
        terminal_actual = label
        simular_y_draw()

    slider_tiempo.on_changed(update_slider)
    radio_terminal.on_clicked(update_radio)

    # Lanzamiento inicial
    simular_y_draw()
    plt.show()
def earth_aeropuertos_misma_letra():
    if aeropuertos:  # Comprobamos que la lista general no esté vacía
        aeropuertos_filtrados = [] #Con este bucle nos quedaremos solamente con los aeropuertos que nos interesan
        for element in range(len(aeropuertos)):
            icao=aeropuertos[element].ICAO
            if icao[0] == icao[-1]: #comprobamos si la primera y la última letra son iguales
                aeropuertos_filtrados.append(aeropuertos[element]) #añadimos el aeropuerto encontrado a la lista vacía
        if len(aeropuertos_filtrados) > 0: #se hace solamente si hemos logrado encontrar un aeropuerto
            try:
                MapAirports(aeropuertos_filtrados)
                archivo = "Ubicaciones.kml"
                if sys.platform == "win32":
                    os.startfile(archivo)
                elif sys.platform == "darwin":
                    subprocess.call(["open", archivo])
            except (OSError, subprocess.SubprocessError):
                messagebox.showerror(title='Error',
                                     message='No tienes Google Earth instalado, prueba a abrirlo en el navegador y cargar el archivo \"Ubicaciones.kml\"')
        else:
            messagebox.showinfo(title='Información',
                                message='No hay aeropuertos cuyo ICAO empiece y acabe por la misma letra')

    else:
        messagebox.showerror(title='Error', message='Lista de aeropuertos vacía')
def cambiar_tema(color_fondo, color_boton):
    # 1. Pintar el fondo de la ventana principal
    window.config(bg=color_fondo)

    # 2. Configurar el estilo de los botones (La clave para que funcione en macOS)
    estilo = ttk.Style()
    estilo.theme_use('default')  # Fuerza al sistema a dejarnos cambiar los colores
    estilo.configure('TButton', background=color_boton)

    # 3. Función recursiva para pintar todos los marcos y textos por dentro
    def pintar_widgets(widget):
        # Filtramos para no pintar donde el usuario escribe, listas o canvas
        if not isinstance(widget, (tk.Entry, tk.Listbox, tk.Canvas, tk.Scrollbar, ttk.Separator, ttk.Combobox)):
            try:
                widget.config(bg=color_fondo)
            except tk.TclError:
                pass  # Si el elemento no tiene propiedad de fondo, lo ignoramos

        # Repetimos para todos los elementos dentro de este widget
        for hijo in widget.winfo_children():
            pintar_widgets(hijo)

    pintar_widgets(window)
def generar_reporte_diario():
    # 1. Comprobar que hay datos mínimos para hacer un reporte
    if len(aircrafts) == 0:
        messagebox.showerror('Error', 'No hay vuelos cargados o fusionados para generar el reporte.')
        return

    # 2. Abrir explorador para elegir dónde guardar el archivo
    archivo = filedialog.asksaveasfilename(
        title="Guardar Reporte Diario",
        defaultextension=".txt",
        initialfile="Reporte_LEBL_Cierre.txt",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )
    if not archivo:
        return

    try:
        # 3. Recopilar datos directamente de la lista global combinada
        total_aeronaves = len(aircrafts)

        # Contadores de tipos de vuelo
        llegadas = sum(1 for ac in aircrafts if getattr(ac, 'time_of_landing', '') != "")
        salidas = sum(1 for ac in aircrafts if getattr(ac, 'time_of_departure', '') != "")
        pernoctaciones = sum(1 for ac in aircrafts if
                             getattr(ac, 'time_of_departure', '') != "" and getattr(ac, 'time_of_landing', '') == "")

        # Calcular Top 3 Aerolíneas
        conteo_cias = {}
        for ac in aircrafts:
            conteo_cias[ac.company] = conteo_cias.get(ac.company, 0) + 1
        # Ordenamos el diccionario de mayor a menor y nos quedamos con los 3 primeros
        top_3 = sorted(conteo_cias.items(), key=lambda x: x[1], reverse=True)[:3]

        # Calcular Larga Distancia usando tu función oficial
        num_largos = 0
        if aeropuertos:
            try:
                largos = LongDistanceArrivals(aircrafts, aeropuertos)
                if largos:
                    num_largos = len(largos)
            except Exception:
                pass

        # Calcular ocupación actual de puertas en el aeropuerto (estado bcn)
        puertas_ocupadas = 0
        total_puertas = 0
        if bcn:
            for terminal in bcn.terminals:
                for area in getattr(terminal, 'Boarding_area', []):
                    for gate in getattr(area, 'Gate', []):
                        total_puertas += 1
                        if getattr(gate, 'occupied', False) or getattr(gate, 'Occupied', False):
                            puertas_ocupadas += 1

        # 4. Escribir el archivo con formato visual de "Ticket de Operaciones"
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("=========================================================\n")
            f.write("          REPORTE DIARIO DE OPERACIONES - LEBL           \n")
            f.write("=========================================================\n\n")

            f.write(">>> RESUMEN GLOBAL DE TRÁFICO <<<\n")
            f.write("---------------------------------------------------------\n")
            f.write(f"Total de aeronaves gestionadas : {total_aeronaves}\n")
            f.write(f"Vuelos de llegada procesados   : {llegadas}\n")
            f.write(f"Vuelos de salida procesados    : {salidas}\n")
            f.write(f"Pernoctaciones (solo salida)   : {pernoctaciones}\n\n")

            f.write(">>> MÉTRICAS DE EFICIENCIA Y SEGURIDAD <<<\n")
            f.write("---------------------------------------------------------\n")
            f.write(f"Llegadas larga distancia (>2000km): {num_largos} \n")

            if total_puertas > 0:
                porcentaje = (puertas_ocupadas / total_puertas) * 100
                f.write(
                    f"Estado de puertas al cierre       : {puertas_ocupadas}/{total_puertas} ({porcentaje:.1f}% de ocupación)\n")
            else:
                f.write("Estado de puertas al cierre       : Aeropuerto no cargado\n")
            f.write("\n")

            f.write(">>> TOP 3 AEROLÍNEAS DEL DÍA <<<\n")
            f.write("---------------------------------------------------------\n")
            for i, (cia, cantidad) in enumerate(top_3):
                f.write(f"{i + 1}. {cia} - {cantidad} vuelos operativos\n")


        messagebox.showinfo('Reporte Generado',
                            f'El reporte de cierre diario se ha guardado correctamente en:\n{archivo}')

    except Exception as e:
        messagebox.showerror('Error', f'Ocurrió un error al generar el reporte:\n{e}')

# ------ CONFIGURACION VENTANA ------

window = Tk()
# window.geometry("1500x650")
window.title("Projecte I1")
window.minsize(1400, 1)
# window.resizable(True, False)

window.columnconfigure(0, weight=1, minsize=900)
window.columnconfigure(1, weight=1, minsize=500)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)


# ------ FUNCIONES DE TEMA (COLORES) ------
def cambiar_tema(color_fondo, color_boton):
    # 1. Pintar el fondo de la ventana principal
    window.config(bg=color_fondo)

    # 2. Configurar el estilo de los botones (La clave para que funcione en macOS)
    estilo = ttk.Style()
    estilo.theme_use('default')  # Fuerza al sistema a dejarnos cambiar los colores
    estilo.configure('TButton', background=color_boton)

    # 3. Función recursiva para pintar todos los marcos y textos por dentro
    def pintar_widgets(widget):
        # Filtramos para no pintar donde el usuario escribe, listas o canvas
        if not isinstance(widget, (tk.Entry, tk.Listbox, tk.Canvas, tk.Scrollbar, ttk.Separator)):
            try:
                widget.config(bg=color_fondo)
            except tk.TclError:
                pass  # Si el elemento no tiene propiedad de fondo, lo ignoramos

        # Repetimos para todos los elementos dentro de este widget
        for hijo in widget.winfo_children():
            pintar_widgets(hijo)

    pintar_widgets(window)


def tema_rosa():
    cambiar_tema('#ffa6d9', '#ff788c')


def tema_amarillo():
    cambiar_tema('#ffbf6e', '#ffb852')


def tema_verde():
    cambiar_tema('#94ff94', '#2dbc94')


def tema_defecto():
    # Colores grises por defecto de la interfaz clásica
    cambiar_tema('#ececec', '#e0e0e0')


# ------ MENÚ SUPERIOR (SELECTOR DE TEMAS) ------
barra_menu = tk.Menu(window)
window.config(menu=barra_menu)

menu_temas = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Temas", menu=menu_temas)

menu_temas.add_command(label="Por defecto", command=tema_defecto)
menu_temas.add_command(label="Rosa", command=tema_rosa)
menu_temas.add_command(label="Amarillo", command=tema_amarillo)
menu_temas.add_command(label="Verde", command=tema_verde)

# ------ FRAME MOSTRAR GRÁFICOS ------

frame_graficos = tk.LabelFrame(window, text="Visualización gráficos")
frame_graficos.grid(row = 0, column = 1, padx = (0,10), pady=5, rowspan = 3, sticky = tk.N + tk.S + tk.E + tk.W)
frame_graficos.grid_columnconfigure(0, weight=1)
frame_graficos.grid_rowconfigure(0, weight=1)
canvas_graficos = tk.Canvas(frame_graficos)
canvas_graficos.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

# ------ FRAME VERSIO1 ------

frame_v1 = tk.LabelFrame(window, text="Aeropuertos")
frame_v1.grid(row = 0, column = 0, padx = 10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)
frame_v1.grid_columnconfigure(0, weight=0)
frame_v1.grid_columnconfigure(1, weight=1, minsize=460)
frame_v1.grid_rowconfigure(0, weight=0)
frame_v1.grid_rowconfigure(1, weight=1)

# ------ FRAME DATOS AEROPUERTO ------

frame_aeropuerto = tk.LabelFrame(frame_v1, text="Datos aeropuerto")
frame_aeropuerto.grid(row=0, column=0, padx=10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

# ------ FORMULARIOS DATOS AEROPUERTOS ------

lbl_icao = tk.Label(frame_aeropuerto, text="ICAO")
lbl_icao.grid(row=0, column=0, padx = 5, sticky = tk.W)

entry_icao = tk.Entry(frame_aeropuerto, width=10)
entry_icao.grid(row=1, column=0, padx = 5, pady = (0,5), sticky = tk.N + tk.S + tk.E + tk.W)

lbl_lat = tk.Label(frame_aeropuerto, text="Latitud")
lbl_lat.grid(row=0, column=1, padx = 5, sticky = tk.W)

entry_lat = tk.Entry(frame_aeropuerto, width=10)
entry_lat.grid(row=1, column=1, padx = 5, pady = (0,5), sticky = tk.N + tk.S + tk.E + tk.W)

lbl_lon = tk.Label(frame_aeropuerto, text="Longitud")
lbl_lon.grid(row=0, column=2, padx = 5, sticky = tk.W)

entry_lon = tk.Entry(frame_aeropuerto, width=10)
entry_lon.grid(row=1, column=2, padx = 5, pady = (0,5), sticky = tk.N + tk.S + tk.E + tk.W)

btn_anadir = ttk.Button(frame_aeropuerto, text="Añadir", command=anadir)
btn_anadir.grid(row=1, column=3, padx=(5,0), pady=(0,5), sticky=tk.N + tk.S + tk.E + tk.W)

btn_suprimir = ttk.Button(frame_aeropuerto, text="Eliminar", command=suprimir)
btn_suprimir.grid(row=1, column=4, padx=(0,5), pady=(0,5), sticky=tk.N + tk.S + tk.E + tk.W)

boton_cargar = ttk.Button(frame_aeropuerto, text="Cargar archivo de aeropuertos", command=importar_archivo)
boton_cargar.grid(row=2, column=0, columnspan=5, padx=5, pady=(0,5), sticky=tk.N + tk.S + tk.E + tk.W)

# ------ FRAME VISUALIZACION DATOS ------

frame_visualizacion = tk.LabelFrame(frame_v1, text="Opciones respecto al listado de aeropuertos")
frame_visualizacion.grid(row=1, column=0, padx=10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)
frame_visualizacion.grid_columnconfigure(0, weight=1)
frame_visualizacion.grid_columnconfigure(1, weight=1)
frame_visualizacion.grid_rowconfigure(0, weight=1)
frame_visualizacion.grid_rowconfigure(1, weight=1)

boton_grafico = ttk.Button(frame_visualizacion, text="Gráfico Schengen/No-Schengen", command=graficoAeropuertos)
boton_grafico.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_kml = ttk.Button(frame_visualizacion, text="Visualizar en Google Earth", command=map_airports)
boton_kml.grid(row = 0, column = 1, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_schengen = ttk.Button(frame_visualizacion, text="Guardar aeropuertos Schengen en .txt", command=archivo_Schengen)
boton_schengen.grid(row = 1, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W, columnspan=2)

boton_misma_letra = ttk.Button(frame_visualizacion, text="Google Earth: ICAO misma letra", command=earth_aeropuertos_misma_letra)
boton_misma_letra.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W, columnspan=2)
# ------ FRAME LISTADO AEROPUERTOS ------

frame_listado = tk.LabelFrame(frame_v1, text="Listado aeropuertos")
frame_listado.grid(row=0, column=1, padx=(0,10), pady=(0,5), rowspan=2, sticky = tk.N + tk.S + tk.E + tk.W)
frame_listado.grid_rowconfigure(0, weight=1)
frame_listado.grid_columnconfigure(0, weight=1)

# ------ LISTBOX LISTA AEROPUERTOS + SCROLLBAR------

listado = tk.Listbox(frame_listado, font=("Courier", 14), )
listado.grid(row = 0, column = 0, padx=10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

vscrollbar = tk.Scrollbar(frame_listado, orient="vertical")
vscrollbar.grid(row=0, column=1, sticky= tk.N + tk.S)

listado.config(yscrollcommand=vscrollbar.set)
vscrollbar.config(command=listado.yview)

hscrollbar = tk.Scrollbar(frame_listado, orient="horizontal")
hscrollbar.grid(row=1, column=0, sticky= tk.E +tk.W)

listado.config(xscrollcommand=hscrollbar.set)
hscrollbar.config(command=listado.xview)

# ------ FRAME VERSIO2 ------

frame_v2 = tk.LabelFrame(window, text="Vuelos")
frame_v2.grid(row = 1, column = 0, padx = 10, pady=(0,5), sticky = tk.N + tk.S + tk.E + tk.W)
frame_v2.grid_columnconfigure(0, weight=0)
frame_v2.grid_columnconfigure(1, weight=1, minsize=480)
frame_v2.grid_rowconfigure(0, weight=1)
frame_v2.grid_rowconfigure(1, weight=1)
frame_v2.grid_rowconfigure(2, weight=1)

# ------ CARGAR/EXPORTAR VUELOS VUELOS ------

frame_gestionvuelos = tk.LabelFrame(frame_v2, text="Cargar/Exportar llegadas")
frame_gestionvuelos.grid(row = 0, column = 0, padx=10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)
frame_gestionvuelos.grid_rowconfigure(0, weight=1)
frame_gestionvuelos.grid_rowconfigure(2, weight=1)
frame_gestionvuelos.grid_columnconfigure(0, weight=1)
frame_gestionvuelos.grid_columnconfigure(1, weight=1)

boton_cargarvuelos = ttk.Button(frame_gestionvuelos, text="Cargar vuelos", command=cargar_vuelos)
boton_cargarvuelos.grid(row=0, column=0, padx=(5,0), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

boton_exportarvuelos = ttk.Button(frame_gestionvuelos, text="Exportar vuelos", command=exportar_vuelos)
boton_exportarvuelos.grid(row=0, column=1, padx=(0,5), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

separador_fusion = ttk.Separator(frame_gestionvuelos, orient="horizontal")
separador_fusion.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=2)

boton_cargarsalidas = ttk.Button(frame_gestionvuelos, text="Cargar salidas", command=cargar_salidas)
boton_cargarsalidas.grid(row=2, column=0, padx=(5,0), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

boton_fusionar = ttk.Button(frame_gestionvuelos, text="Combinar Salidas y Llegadas", command=fusionar_movimientos)
boton_fusionar.grid(row=2, column=1, padx=(0,5), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

# ------ FRAME GRAFICOS VUELOS ------

frame_graficosvuelos = tk.LabelFrame(frame_v2, text="Gráficos de llegadas")
frame_graficosvuelos.grid(row=1, column=0, padx=10, pady=(5,10),sticky = tk.N + tk.S + tk.E + tk.W)
frame_graficosvuelos.grid_columnconfigure(0, weight=1)
frame_graficosvuelos.grid_columnconfigure(1, weight=1)
frame_graficosvuelos.grid_rowconfigure(0, weight=1)
frame_graficosvuelos.grid_rowconfigure(1, weight=1)

boton_vuelosschengen = ttk.Button(frame_graficosvuelos, text="Schengen/No-Schengen", command=grafico_vuelosSchengen)
boton_vuelosschengen.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_vueloscompania = ttk.Button(frame_graficosvuelos, text="Por compañia", command=grafico_vuelosPorCompania)
boton_vueloscompania.grid(row = 0, column = 1, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_vueloshora = ttk.Button(frame_graficosvuelos, text="Por horas", command=grafico_vuelosPorLlegada)
boton_vueloshora.grid(row = 1, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W, columnspan=2)

# ------ FRAME LISTADO AEROPUERTO ------

frame_listadovuelos = tk.LabelFrame(frame_v2, text="Listado aviones")
frame_listadovuelos.grid(row=0, column=1, padx=(0,10), pady=10, rowspan=3, sticky = tk.N + tk.S + tk.E + tk.W)
frame_listadovuelos.grid_rowconfigure(0, weight=1)
frame_listadovuelos.grid_columnconfigure(0, weight=1)

# ------ FRAME GOOGLE EARTH ------

frame_earth = tk.LabelFrame(frame_v2, text="Mostrar vuelos en Google Earth")
frame_earth.grid(row=2, column=0, padx=10, pady=(5,10),sticky = tk.N + tk.S + tk.E + tk.W)
frame_earth.grid_columnconfigure(0, weight=1)
frame_earth.grid_columnconfigure(1, weight=1)
frame_earth.grid_rowconfigure(0, weight=1)

boton_earthvuelos = ttk.Button(frame_earth, text="Mostrar todos los vuelos", command=earth_vuelos)
boton_earthvuelos.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_vueloslargos = ttk.Button(frame_earth, text="Mostrar vuelos de larga distancia", command=earth_largaDistancia)
boton_vueloslargos.grid(row = 0, column = 1, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

# ------ LISTBOX LISTA VUELOS + SCROLLBAR------

listadovuelos = tk.Listbox(frame_listadovuelos, font=("Courier", 14),)
listadovuelos.grid(row = 0, column = 0, padx=10, pady=(0,5), sticky = tk.N + tk.S + tk.E + tk.W)

vscrollbar = tk.Scrollbar(frame_listadovuelos, orient="vertical")
vscrollbar.grid(row=0, column=1, sticky= tk.N + tk.S)

listadovuelos.config(yscrollcommand=vscrollbar.set)
vscrollbar.config(command=listadovuelos.yview)

hscrollbar = tk.Scrollbar(frame_listadovuelos, orient="horizontal")
hscrollbar.grid(row=1, column=0, sticky= tk.E +tk.W)

listadovuelos.config(xscrollcommand=hscrollbar.set)
hscrollbar.config(command=listadovuelos.xview)

# ------ FRAME V3 ------

frame_v3 = tk.LabelFrame(window, text="Puertas de embarque")
frame_v3.grid(row = 2, column = 0, padx = 10, pady=(0,5), sticky = tk.N + tk.S + tk.E + tk.W)
frame_v3.grid_columnconfigure(0, weight=0)
frame_v3.grid_columnconfigure(1, weight=1, minsize=480)
frame_v3.grid_rowconfigure(0, weight=1)
frame_v3.grid_rowconfigure(1, weight=1)
frame_v3.grid_rowconfigure(2, weight=1)

# ------ GESTIÓ PORTES ------

frame_puertas = tk.LabelFrame(frame_v3, text="Gestión")
frame_puertas.grid(row = 0, column = 0, padx = 10, pady=(0,5), sticky = tk.N + tk.S + tk.E + tk.W)
frame_puertas.grid_rowconfigure(0, weight=1)
frame_puertas.grid_rowconfigure(1, weight=1)
frame_puertas.grid_rowconfigure(2, weight=1)
frame_puertas.grid_columnconfigure(0, weight=1)
frame_puertas.grid_columnconfigure(1, weight=1)

# ------ BOTONS ------

boton_estructura = ttk.Button(frame_puertas, text="Cargar estructura del apuerto", command=cargar_estructura)
boton_estructura.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_asignarpuerta = ttk.Button(frame_puertas, text="Asignar puerta a cada vuelo", command=asignar_puertas)
boton_asignarpuerta.grid(row = 1, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_puertasnocturnas = ttk.Button(frame_puertas, text="Asignar puertas nocturnas", command=asignar_puertas_nocturnas)
boton_puertasnocturnas.grid(row = 2, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)
# ------ FRAME LISTADO PUERTAS ------

frame_listadopuertas = tk.LabelFrame(frame_v3, text="Listado puertas")
frame_listadopuertas.grid(row=0, column=1, padx=(0,10), pady=(0,5), rowspan=1, sticky = tk.N + tk.S + tk.E + tk.W)
frame_listadopuertas.grid_rowconfigure(0, weight=1)
frame_listadopuertas.grid_columnconfigure(0, weight=1)

# ------ LISTBOX LISTA PUERTAS + SCROLLBAR------

listadopuertas = tk.Listbox(frame_listadopuertas, font=("Courier", 14),)
listadopuertas.grid(row = 0, column = 0, padx=10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

vscrollbar = tk.Scrollbar(frame_listadopuertas, orient="vertical")
vscrollbar.grid(row=0, column=1, sticky= tk.N + tk.S)

listadopuertas.config(yscrollcommand=vscrollbar.set)
vscrollbar.config(command=listadopuertas.yview)

hscrollbar = tk.Scrollbar(frame_listadopuertas, orient="horizontal")
hscrollbar.grid(row=1, column=0, sticky= tk.E +tk.W)

listadopuertas.config(xscrollcommand=hscrollbar.set)
hscrollbar.config(command=listadopuertas.xview)


# ------ SECCIÓN V4 CONTROL DE INTERFAZ (LIMPIO) ------
def grafico_ocupacion():
    #mostrar gráfico de ocupación de puertas en 24h
    fig = PlotDayOccupancy(bcn, aircrafts)
    if fig is None:
        messagebox.showerror('Error', 'Faltan los datos del aeropuerto, los vuelos o ambos.')
        return
    global canvas, canvas_graficos
    fig.set_size_inches(1, 1)
    fig.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.10)

    canvas = FigureCanvasTkAgg(fig, master=frame_graficos)

    if 'canvas_graficos' in globals():
        canvas_graficos.grid_forget()
    canvas_graficos = canvas.get_tk_widget()
    canvas_graficos.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, padx=15, pady=15)

    canvas.draw()

boton_grafico_v4 = ttk.Button(
    frame_puertas,
    text="Gráfico Ocupación 24h",
    command=grafico_ocupacion
)
boton_grafico_v4.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

boton_mapa_interactivo = ttk.Button(
    frame_puertas,
    text="Plano Dinámico Real",
    command=lambda: MostrarMapaInteractivo(bcn, aircrafts)
)
boton_mapa_interactivo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

# ------ SELECTOR DE TEMA VISUAL ------
frame_tema = tk.LabelFrame(frame_puertas, text="Tema Visual")
frame_tema.grid(row=2, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

opciones_tema = ["Por defecto", "Rosa", "Amarillo", "Verde", "Azul"]
tema_seleccionado = tk.StringVar(value="Por defecto")

combo_tema = ttk.Combobox(frame_tema, textvariable=tema_seleccionado, values=opciones_tema, state="readonly")
combo_tema.pack(padx=10, pady=5, expand=True)

def aplicar_tema(event):
    seleccion = tema_seleccionado.get()
    if seleccion == "Rosa":
        # Fondo: Rosa nube | Botón: Rosa chicle suave
        cambiar_tema('#FCE4EC', '#F48FB1')

    elif seleccion == "Amarillo":
        # Fondo: Vainilla claro | Botón: Amarillo melocotón
        cambiar_tema('#FFF9C4', '#FFE082')

    elif seleccion == "Verde":
        # Fondo: Menta muy claro | Botón: Verde pistacho suave
        cambiar_tema('#E8F5E9', '#A5D6A7')

    elif seleccion == "Azul":
        # Fondo: Azul hielo | Botón: Azul cielo
        cambiar_tema('#E3F2FD', '#90CAF9')

    else:
        # Colores grises por defecto de la interfaz clásica
        cambiar_tema('#ececec', '#e0e0e0')

# Activar la función cuando el usuario elija algo en el desplegable
combo_tema.bind("<<ComboboxSelected>>", aplicar_tema)



# ------ BOTÓN GENERAR REPORTE DIARIO ------
boton_reporte = ttk.Button(
    frame_puertas,
    text="Generar Reporte Diario de Cierre",
    command=generar_reporte_diario
)
boton_reporte.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)



window.mainloop()