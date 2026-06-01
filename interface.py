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
aeropuertos = []
bcn = None
canvas = None

# ------ FUNCIONES ------
#Funcions V1
def mostrar_aeropuertos():
    listado.delete(0, 'end')
    for i in range(len(aeropuertos)):
        listado.insert(tk.END, PrintAirport(aeropuertos[i]))
    return None
def anadir():
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
    if entry_icao.get() != "":
        spr_icao = entry_icao.get()
        RemoveAirport(aeropuertos,spr_icao)
        mostrar_aeropuertos()
        limpiar_formulario()
    else:
        messagebox.showerror('Error','Falta el ICAO del aeropuerto a eliminar')
def importar_archivo():
    file_path = filedialog.askopenfilename(
        title="Seleccione un archivo",
        filetypes=(("Archivos CSV", "*.txt"), ("Todos los archivos", "*.*"))
    )
    provisional = LoadAirports(file_path)
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
    mostrar_aeropuertos()
    return None
def graficoAeropuertos():
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
    SaveSchengenAirports(aeropuertos,"Schengen.txt")
    if aeropuertos:
        messagebox.showinfo('Archivo guardado','Se ha guardado un archivo Schengen.txt')
    else:
        messagebox.showwarning('Archivo no guardado', 'No hay aeropuertos para guardar')
    return None
def map_airports():
    if aeropuertos:
        try:
            MapAirports(aeropuertos)

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
    entry_icao.delete(0, 'end')
    entry_lon.delete(0, 'end')
    entry_lat.delete(0, 'end')

#Funcions V2
def mostrar_vuelos():
    listadovuelos.delete(0, 'end')
    for i in range(len(aircrafts)):
        listadovuelos.insert(tk.END, f'ID: {aircrafts[i].id}\tCompañía: {aircrafts[i].company}\tOrigen: {aircrafts[i].origin_airport}\tLlegada: {aircrafts[i].time_of_landing}')
    return None
def cargar_vuelos():
    global aircrafts
    archivo = filedialog.askopenfilename(
        title="Seleccione un archivo",
        filetypes=(("Archivos CSV", "*.txt"), ("Todos los archivos", "*.*"))
    )
    provisional = LoadArrivals(archivo)
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
    mostrar_vuelos()
def exportar_vuelos():
    archivo = filedialog.askopenfilename(
        title="Seleccione un archivo .txt",
        filetypes=(("Archivos de texto","*.txt"), ("Todos los archivos", "*.*"))
    )
    try:
        SaveFlights(aircrafts,archivo)
    except FileNotFoundError:
        messagebox.showerror('Error', 'No se ha seleccionado ningún archivo')
def grafico_vuelosSchengen():
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
    if aircrafts:
        global canvas, canvas_graficos
        fig = PlotAirlines(aircrafts)
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
def grafico_vuelosPorLlegada():
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
    if aircrafts and aeropuertos:
        try:
            MapFlights(LongDistanceArrivals(aircrafts,aeropuertos), aeropuertos)

            archivo = "Vuelos.kml"
            if sys.platform == "win32":
                os.startfile(archivo)
            elif sys.platform == "darwin":
                subprocess.call(["open", archivo])
        except:
            messagebox.showerror('Error','No tienes Google Earth instalado, prueba a abrirlo en el navegador y cargar el archivo \"Vuelos.kml\"')
    else:
        messagebox.showerror('Error', 'Faltan los datos de los vuelos, los datos de los aeropuertos o ambos')
def earth_vuelos():
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
    if not aircrafts or not bcn:
        messagebox.showerror('Error', 'Listado de aviones vacío o falta estructura del aeropuerto')
    else:
        for i in range (len(aircrafts)):
                AssignGate(bcn,aircrafts[i])
        mostrar_puertas()
        return None
def mostrar_puertas():
    listadopuertas.delete(0, 'end')
    for j in range (len(bcn.terminals)):
        for i in range(len(bcn.terminals[j].Boarding_area)):
            for k in range(len(bcn.terminals[j].Boarding_area[i].Gate)):
                if bcn.terminals[j].Boarding_area[i].Gate[k].occupied:
                    listadopuertas.insert(tk.END, f'{bcn.terminals[j].Boarding_area[i].Gate[k].name}\t\t({bcn.terminals[j].Boarding_area[i].area})\t\tOcupada por {bcn.terminals[j].Boarding_area[i].Gate[k].aircraft_id}')
                else:
                    listadopuertas.insert(tk.END,f'{bcn.terminals[j].Boarding_area[i].Gate[k].name}\t\t({bcn.terminals[j].Boarding_area[i].area})\t\tLibre')
    return None


#Funcion V4


def PlotDayOccupancy(bcn, aircrafts):
    """
    Construye el gráfico de ocupación horaria adaptado a tu estructura de datos exacta.
    """
    import matplotlib.pyplot as plt

    # Comprobación de seguridad por si el usuario no ha cargado los datos todavía
    if not bcn or not aircrafts:
        from tkinter import messagebox
        messagebox.showerror('Error', 'Faltan los datos del aeropuerto, los vuelos o ambos.')
        return

    horas = [f"{str(h).zfill(2)}:00" for h in range(24)]
    terminal_names = [t.name for t in bcn.terminals]
    ocupacion_por_terminal = {name: [0] * 24 for name in terminal_names}
    no_asignados = [0] * 24

    for h_idx, hora_actual in enumerate(horas):
        # 1. Liberar puertas de aviones que salen a esta hora
        for ac in aircrafts:
            ac_id = getattr(ac, 'id', getattr(ac, 'ID', None))
            ac_dep = getattr(ac, 'time_of_departure', None)
            if ac_dep:
                hora_dep = ac_dep.split(":")[0] + ":00"
                if hora_dep == hora_actual:
                    FreeGate(bcn, ac_id)

        # 2. Contar ocupación usando Boarding_area y Gate con mayúsculas reales
        for terminal in bcn.terminals:
            count = 0
            # Usamos getattr por seguridad, pero apunta directamente a Boarding_area
            lista_areas = getattr(terminal, 'Boarding_area', [])
            for area in lista_areas:
                lista_puertas = getattr(area, 'Gate', [])
                for gate in lista_puertas:
                    if getattr(gate, 'occupied', False) or getattr(gate, 'Occupied', False):
                        count += 1
            ocupacion_por_terminal[terminal.name][h_idx] = count

    # --- Renderizado del gráfico ---
    fig, ax = plt.subplots(figsize=(10, 5))
    for name, datos_hora in ocupacion_por_terminal.items():
        ax.plot(horas, datos_hora, marker='o', label=f"Ocupación {name}")

    ax.set_xticklabels(horas, rotation=45)
    ax.set_xlabel("Hora del día")
    ax.set_ylabel("Puertas Ocupadas")
    ax.set_title("Ocupación Dinámica del Aeropuerto (V4)")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    plt.tight_layout()
    plt.show()


def MostrarMapaInteractivo(bcn, aircrafts):
    """
    Muestra un mapa interactivo con un Slider para las horas y un selector
    de Terminal (T1 / T2) que utiliza la función lógica del grupo (AssignGatesAtTime)
    de forma secuencial y limpia para actualizar el estado de ocupación.
    """
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider, RadioButtons
    import matplotlib.patches as patches

    if not bcn or not aircrafts:
        from tkinter import messagebox
        messagebox.showerror('Error', 'Primero debes cargar el aeropuerto y los vuelos.')
        return

    # Creamos la figura y ajustamos márgenes para los controles interactivos
    fig, ax = plt.subplots(figsize=(11, 6))
    plt.subplots_adjust(bottom=0.2, left=0.2)

    # Variables de estado que rastrean lo que el usuario ve en pantalla
    terminal_actual = bcn.terminals[0].name  # Por defecto la T1
    hora_actual_int = 12  # Por defecto las 12:00

    def simular_y_dibujar():
        ax.clear()
        ax.set_title(f"Estado de Puertas - {terminal_actual} - Hora {str(hora_actual_int).zfill(2)}:00", fontsize=14,
                     fontweight='bold')
        ax.set_xlim(-1, 10)
        ax.set_ylim(-1, 8)
        ax.axis('off')

        # 1. RESETEAR TODAS LAS PUERTAS A SU ESTADO VACÍO ANTES DE COMENZAR EL DÍA
        for t in bcn.terminals:
            for area in getattr(t, 'Boarding_area', []):
                for g in getattr(area, 'Gate', []):
                    g.occupied = False
                    g.aircraft_id = ""

        # 2. SIMULAR EL PASO DEL TIEMPO HORA A HORA SECUENCIALMENTE
        # Pasamos por cada hora de forma independiente para que no se dupliquen asignaciones
        for h in range(hora_actual_int + 1):
            hora_str = f"{str(h).zfill(2)}:00"

            # Ejecutamos la lógica de asignación y liberación de esa hora concreta
            try:
                AssignGatesAtTime(bcn, aircrafts, hora_str)
            except Exception as e:
                # Evita que un error bloquee el renderizado del gráfico
                pass

        # 3. OBTENER LA TERMINAL QUE EL USUARIO HA SELECCIONADO PARA DIBUJARLA
        t_obj = next((t for t in bcn.terminals if t.name == terminal_actual), bcn.terminals[0])
        lista_areas = getattr(t_obj, 'Boarding_area', [])

        # Dibujar pasillo principal superior
        ax.plot([0, 9], [7, 7], color='#1a5f7a', linewidth=8)

        # Posiciones en el eje X para representar las áreas de embarque
        columnas_x = [1.5, 4.5, 7.5]

        for i, area in enumerate(lista_areas):
            if i >= 3: break  # Límite visual de la ventana de dibujo

            x = columnas_x[i]
            nombre_area = getattr(area, 'name', f"Area {i + 1}")

            # Dibujar el pasillo vertical del muelle de embarque
            ax.plot([x, x], [1, 7], color='#1a5f7a', linewidth=10)
            ax.text(x, 0.5, nombre_area, ha='center', fontsize=12, fontweight='bold')

            lista_puertas = getattr(area, 'Gate', [])

            # Dibujar hasta 6 puertas por cada área
            for p_idx, gate in enumerate(lista_puertas):
                if p_idx >= 6: break

                es_izquierda = (p_idx % 2 == 0)
                fila_y = [5.5, 3.5, 1.5][p_idx // 2]

                if es_izquierda:
                    ax.plot([x - 0.6, x], [fila_y, fila_y], color='#1a5f7a', linewidth=4)
                    x_rect = x - 1.2
                    ha_text = 'right'
                    x_text = x - 1.4
                else:
                    ax.plot([x, x + 0.6], [fila_y, fila_y], color='#1a5f7a', linewidth=4)
                    x_rect = x + 0.7
                    ha_text = 'left'
                    x_text = x + 1.3

                # Capturar el estado de ocupación calculado
                is_occupied = getattr(gate, 'occupied', False) or getattr(gate, 'Occupied', False)
                ac_label = getattr(gate, 'aircraft_id', '') if is_occupied else ""

                # Color del avión según el estado: Rojo (ocupado) o Verde (libre)
                color = 'red' if is_occupied else '#10b981'

                # Pintar el rectángulo de la puerta
                rect = patches.Rectangle((x_rect, fila_y - 0.2), 0.5, 0.4, linewidth=1, facecolor=color)
                ax.add_patch(rect)

                # Si hay una aeronave asignada, pintar su matrícula
                if ac_label:
                    ax.text(x_text, fila_y, ac_label, ha=ha_text, va='center', fontsize=8, color='black',
                            fontweight='bold')

        fig.canvas.draw_idle()

    # --- CONTROLES INTERACTIVOS DE MATPLOTLIB ---
    ax_slider = plt.axes([0.25, 0.05, 0.55, 0.03], facecolor='lightgray')
    slider_hora = Slider(ax_slider, 'Hora', 0, 23, valinit=12, valfmt='%02d:00')

    ax_radio = plt.axes([0.02, 0.4, 0.12, 0.2], facecolor='lightgray')
    nombres_terminales = [t.name for t in bcn.terminals]
    radio_terminal = RadioButtons(ax_radio, nombres_terminales)

    def update_slider(val):
        nonlocal hora_actual_int
        hora_actual_int = int(slider_hora.val)
        simular_y_dibujar()

    def update_radio(label):
        nonlocal terminal_actual
        terminal_actual = label
        simular_y_dibujar()

    slider_hora.on_changed(update_slider)
    radio_terminal.on_clicked(update_radio)

    # Dibujamos el estado inicial
    simular_y_dibujar()
    plt.show()


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

btn_anadir = tk.Button(frame_aeropuerto, text="Añadir", command=anadir)
btn_anadir.grid(row=1, column=3, padx=(5,0), pady=(0,5), sticky=tk.N + tk.S + tk.E + tk.W)

btn_suprimir = tk.Button(frame_aeropuerto, text="Eliminar", command=suprimir)
btn_suprimir.grid(row=1, column=4, padx=(0,5), pady=(0,5), sticky=tk.N + tk.S + tk.E + tk.W)

boton_cargar = tk.Button(frame_aeropuerto, text="Cargar archivo de aeropuertos", command=importar_archivo)
boton_cargar.grid(row=2, column=0, columnspan=5, padx=5, pady=(0,5), sticky=tk.N + tk.S + tk.E + tk.W)

# ------ FRAME VISUALIZACION DATOS ------

frame_visualizacion = tk.LabelFrame(frame_v1, text="Opciones respecto al listado de aeropuertos")
frame_visualizacion.grid(row=1, column=0, padx=10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)
frame_visualizacion.grid_columnconfigure(0, weight=1)
frame_visualizacion.grid_columnconfigure(1, weight=1)
frame_visualizacion.grid_rowconfigure(0, weight=1)
frame_visualizacion.grid_rowconfigure(1, weight=1)

boton_grafico = tk.Button(frame_visualizacion, text="Gráfico Schengen/No-Schengen", command=graficoAeropuertos)
boton_grafico.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_kml = tk.Button(frame_visualizacion, text="Visualizar en Google Earth", command=map_airports)
boton_kml.grid(row = 0, column = 1, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_schengen = tk.Button(frame_visualizacion, text="Guardar aeropuertos Schengen en .txt", command=archivo_Schengen)
boton_schengen.grid(row = 1, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W, columnspan=2)

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

frame_gestionvuelos = tk.LabelFrame(frame_v2, text="Cargar/Exportar vuelos")
frame_gestionvuelos.grid(row = 0, column = 0, padx=10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)
frame_gestionvuelos.grid_rowconfigure(0, weight=1)
frame_gestionvuelos.grid_columnconfigure(0, weight=1)
frame_gestionvuelos.grid_columnconfigure(1, weight=1)

boton_cargarvuelos = tk.Button(frame_gestionvuelos, text="Cargar vuelos", command=cargar_vuelos)
boton_cargarvuelos.grid(row=0, column=0, padx=(5,0), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

boton_exportarvuelos = tk.Button(frame_gestionvuelos, text="Exportar vuelos", command=exportar_vuelos)
boton_exportarvuelos.grid(row=0, column=1, padx=(0,5), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

# ------ FRAME GRAFICOS VUELOS ------

frame_graficosvuelos = tk.LabelFrame(frame_v2, text="Gráficos de llegadas")
frame_graficosvuelos.grid(row=1, column=0, padx=10, pady=(5,10),sticky = tk.N + tk.S + tk.E + tk.W)
frame_graficosvuelos.grid_columnconfigure(0, weight=1)
frame_graficosvuelos.grid_columnconfigure(1, weight=1)
frame_graficosvuelos.grid_rowconfigure(0, weight=1)
frame_graficosvuelos.grid_rowconfigure(1, weight=1)

boton_vuelosschengen = tk.Button(frame_graficosvuelos, text="Schengen/No-Schengen", command=grafico_vuelosSchengen)
boton_vuelosschengen.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_vueloscompania = tk.Button(frame_graficosvuelos, text="Por compañia", command=grafico_vuelosPorCompania)
boton_vueloscompania.grid(row = 0, column = 1, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_vueloshora = tk.Button(frame_graficosvuelos, text="Por horas", command=grafico_vuelosPorLlegada)
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

boton_earthvuelos = tk.Button(frame_earth, text="Mostrar todos los vuelos", command=earth_vuelos)
boton_earthvuelos.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_vueloslargos = tk.Button(frame_earth, text="Mostrar vuelos de larga distancia", command=earth_largaDistancia)
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
frame_puertas.grid_columnconfigure(0, weight=1)
frame_puertas.grid_columnconfigure(1, weight=1)

# ------ BOTONS ------

boton_estructura = tk.Button(frame_puertas, text="Cargar estructura del apuerto", command=cargar_estructura)
boton_estructura.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_asignarpuerta = tk.Button(frame_puertas, text="Asignar puerta a cada vuelo", command=asignar_puertas)
boton_asignarpuerta.grid(row = 1, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)
'''
boton_mostrarocupacion = tk.Button(frame_puertas, text="Mostrar ocupación puertas", command=mostrar_ocupacion)
boton_mostrarocupacion.grid(row = 0, column = 1, padx=5, pady=5, rowspan=2, sticky = tk.N + tk.S + tk.E + tk.W)
'''
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


# ------ v4 --------
boton_grafico_v4 = tk.Button(frame_puertas, text="Gráfico Ocupación 24h (V4)", command=lambda: PlotDayOccupancy(bcn, aircrafts))
boton_grafico_v4.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

boton_mapa_interactivo = tk.Button(frame_puertas, text="Ver Mapa Puertas Ocupadas (Slider)", command=lambda: MostrarMapaInteractivo(bcn, aircrafts))
boton_mapa_interactivo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

window.mainloop()