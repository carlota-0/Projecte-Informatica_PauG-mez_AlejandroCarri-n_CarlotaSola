from airport import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import sys
import subprocess

aeropuertos = []

# ------ FUNCIONES ------

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
def grafico():
    PlotAirports(aeropuertos)
    return None
def archivo_Schengen():
    SaveSchengenAirports(aeropuertos,"Schengen.txt")
    if aeropuertos:
        messagebox.showinfo('Archivo guardado','Se ha guardado un archivo Schengen.txt')
    else:
        messagebox.showwarning('Archivo no guardado', 'No hay aeropuertos para guardar')
    return None
def map_airports():
    MapAirports(aeropuertos)
    messagebox.showinfo("Archivo KML creado", "Se ha creado un archivo \"Ubicaciones.kml\"")

    archivo = "Ubicaciones.kml"
    if sys.platform == "win32":
        os.startfile(archivo)
    elif sys.platform == "darwin":
        subprocess.call(["open", archivo])
    print(ruta_archivo)

    return None
def limpiar_formulario():
    entry_icao.delete(0, 'end')
    entry_lon.delete(0, 'end')
    entry_lat.delete(0, 'end')

# ------ CONFIGURACION VENTANA ------

window = Tk()
# window.geometry("1500x650")
window.title("Projecte I1")
# window.resizable(True, False)

window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=1, minsize=500)
window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=0)
window.rowconfigure(2, weight=0)

# ------ FRAME MOSTRAR GRÁFICOS ------

frame_graficos = tk.LabelFrame(window, text="Visualización graficos")
frame_graficos.grid(row = 0, column = 1, padx = (0,10), pady=5, rowspan = 3, sticky = tk.N + tk.S + tk.E + tk.W)
frame_graficos.grid_columnconfigure(0, weight=1)
frame_graficos.grid_rowconfigure(0, weight=1)
boton_vuelosschengen = tk.Label(frame_graficos, text="Placeholder")
boton_vuelosschengen.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

# ------ FRAME VERSIO1 ------

frame_v1 = tk.LabelFrame(window, text="Aeropuertos")
frame_v1.grid(row = 0, column = 0, padx = 10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)
frame_v1.grid_columnconfigure(0, weight=0)
frame_v1.grid_columnconfigure(1, weight=2)
frame_v1.grid_rowconfigure(0, weight=0)
frame_v1.grid_rowconfigure(1, weight=1)
frame_v1.grid_rowconfigure(2, weight=0)

# ------ FRAME DATOS AEROPUERTO ------

frame_aeropuerto = tk.LabelFrame(frame_v1, text="Datos aeropuerto")
frame_aeropuerto.grid(row=0, column=0, padx=10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

# ------ FORMULARIOS DATOS AEROPUERTOS ------

lbl_icao = tk.Label(frame_aeropuerto, text="ICAO")
lbl_icao.grid(row=0, column=0, padx = 10, sticky = tk.W)

entry_icao = tk.Entry(frame_aeropuerto)
entry_icao.grid(row=1, column=0, padx = 10, pady = (0,5), sticky = tk.N + tk.S + tk.E + tk.W)

lbl_lat = tk.Label(frame_aeropuerto, text="Latitud")
lbl_lat.grid(row=0, column=1, padx = 10, sticky = tk.W)

entry_lat = tk.Entry(frame_aeropuerto)
entry_lat.grid(row=1, column=1, padx = 10, pady = (0,5), sticky = tk.N + tk.S + tk.E + tk.W)

lbl_lon = tk.Label(frame_aeropuerto, text="Longitud")
lbl_lon.grid(row=0, column=2, padx = 10, sticky = tk.W)

entry_lon = tk.Entry(frame_aeropuerto)
entry_lon.grid(row=1, column=2, padx = 10, pady = (0,5), sticky = tk.N + tk.S + tk.E + tk.W)

# ------ FRAME MODIFICACIONES ------

frame_mod = tk.LabelFrame(frame_v1, text="Modificacion listado aeropuertos")
frame_mod.grid(row = 1, column = 0, padx=10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)
frame_mod.grid_rowconfigure(0, weight=1)
frame_mod.grid_rowconfigure(1, weight=0)
frame_mod.grid_rowconfigure(1, weight=0)
frame_mod.grid_columnconfigure(0, weight=1)
frame_mod.grid_columnconfigure(1, weight=0)

boton_anadir = tk.Button(frame_mod, text="Añadir aeropuerto", command=anadir)
boton_anadir.grid(row=0, column=0, padx=(5,0), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

boton_suprimir = tk.Button(frame_mod, text="Suprimir aeropuerto", command=suprimir)
boton_suprimir.grid(row=0, column=1, padx=(0,5), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

separador_mod = ttk.Separator(frame_mod, orient="horizontal")
separador_mod.grid(row=1, column=0, columnspan=2, sticky= tk.W + tk.E , padx=5, pady=5)

#entry_archivo = ttk.Entry(frame_mod)
#entry_archivo.grid(row=2, column=0, padx = 10, pady = (0,5), sticky = tk.N + tk.S + tk.E + tk.W)

boton_archivo = tk.Button(frame_mod, text="Cargar archivo .txt", command=importar_archivo)
boton_archivo.grid(row=2, column=0, columnspan=2, padx=(0,5), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

# ------ FRAME VISUALIZACION DATOS ------

frame_visualizacion = tk.LabelFrame(frame_v1, text="Opciones respecto al listado de aeropuertos")
frame_visualizacion.grid(row=2, column=0, padx=10, pady=(5,10),sticky = tk.N + tk.S + tk.E + tk.W)
frame_visualizacion.grid_columnconfigure(0, weight=1)
frame_visualizacion.grid_columnconfigure(1, weight=1)
frame_visualizacion.grid_rowconfigure(0, weight=1)
frame_visualizacion.grid_rowconfigure(1, weight=1)

boton_grafico = tk.Button(frame_visualizacion, text="Gráfico Schengen/No-Schengen", command=grafico)
boton_grafico.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_kml = tk.Button(frame_visualizacion, text="Generar archivo .kml", command=map_airports)
boton_kml.grid(row = 0, column = 1, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_schengen = tk.Button(frame_visualizacion, text="Guardar aeropuertos Schengen en .txt", command=archivo_Schengen)
boton_schengen.grid(row = 1, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W, columnspan=2)

# ------ FRAME LISTADO AEROPUERTO ------

frame_listado = tk.LabelFrame(frame_v1, text="Listado aeropuertos")
frame_listado.grid(row=0, column=1, padx=(0,10), pady=10, rowspan=3, sticky = tk.N + tk.S + tk.E + tk.W)
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
frame_v2.grid(row = 1, column = 0, padx = 10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)
frame_v2.grid_columnconfigure(0, weight=0)
frame_v2.grid_columnconfigure(1, weight=1)
frame_v2.grid_rowconfigure(0, weight=0)
frame_v2.grid_rowconfigure(1, weight=1)
frame_v2.grid_rowconfigure(2, weight=0)

# ------ CARGAR/EXPORTAR VUELOS VUELOS ------

frame_gestionvuelos = tk.LabelFrame(frame_v2, text="Cargar/Exportar vuelos")
frame_gestionvuelos.grid(row = 0, column = 0, padx=10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)
frame_gestionvuelos.grid_rowconfigure(0, weight=1)
frame_gestionvuelos.grid_columnconfigure(0, weight=1)
frame_gestionvuelos.grid_columnconfigure(1, weight=1)

boton_cargarvuelos = tk.Button(frame_gestionvuelos, text="Cargar vuelos", command=None)
boton_cargarvuelos.grid(row=0, column=0, padx=(5,0), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

boton_exportarvuelos = tk.Button(frame_gestionvuelos, text="Exportar vuelos", command=None)
boton_exportarvuelos.grid(row=0, column=1, padx=(0,5), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

# ------ FRAME VISUALIZACION DATOS ------

frame_graficosvuelos = tk.LabelFrame(frame_v2, text="Gráficos")
frame_graficosvuelos.grid(row=1, column=0, padx=10, pady=(5,10),sticky = tk.N + tk.S + tk.E + tk.W)
frame_graficosvuelos.grid_columnconfigure(0, weight=1)
frame_graficosvuelos.grid_columnconfigure(1, weight=1)
frame_graficosvuelos.grid_rowconfigure(0, weight=1)
frame_graficosvuelos.grid_rowconfigure(1, weight=1)

boton_vuelosschengen = tk.Button(frame_graficosvuelos, text="Gráfico Schengen/No-Schengen", command=None)
boton_vuelosschengen.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_vueloscompania = tk.Button(frame_graficosvuelos, text="Gráfico por compañia", command=None)
boton_vueloscompania.grid(row = 0, column = 1, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_vueloshora = tk.Button(frame_graficosvuelos, text="Gráfico por horas", command=None)
boton_vueloshora.grid(row = 1, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W, columnspan=2)

# ------ FRAME LISTADO AEROPUERTO ------

frame_listadovuelos = tk.LabelFrame(frame_v2, text="Listado vuelos")
frame_listadovuelos.grid(row=0, column=1, padx=(0,10), pady=10, rowspan=3, sticky = tk.N + tk.S + tk.E + tk.W)
frame_listadovuelos.grid_rowconfigure(0, weight=1)
frame_listadovuelos.grid_columnconfigure(0, weight=1)

# ------ FRAME GOOGLE EARTH ------

frame_earth = tk.LabelFrame(frame_v2, text="Mostrar vuelos en Google Earth")
frame_earth.grid(row=2, column=0, padx=10, pady=(5,10),sticky = tk.N + tk.S + tk.E + tk.W)
frame_earth.grid_columnconfigure(0, weight=1)
frame_earth.grid_columnconfigure(1, weight=1)
frame_earth.grid_rowconfigure(0, weight=1)

boton_earthvuelos = tk.Button(frame_earth, text="Mostrar todos los vuelos", command=None)
boton_earthvuelos.grid(row = 0, column = 0, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

boton_vueloslargos = tk.Button(frame_earth, text="Mostrar vuelos de larga distancia", command=None)
boton_vueloslargos.grid(row = 0, column = 1, padx=5, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

# ------ LISTBOX LISTA VUELOS + SCROLLBAR------

listadovuelos = tk.Listbox(frame_listadovuelos, font=("Courier", 14), )
listadovuelos.grid(row = 0, column = 0, padx=10, pady=5, sticky = tk.N + tk.S + tk.E + tk.W)

vscrollbar = tk.Scrollbar(frame_listadovuelos, orient="vertical")
vscrollbar.grid(row=0, column=1, sticky= tk.N + tk.S)

listadovuelos.config(yscrollcommand=vscrollbar.set)
vscrollbar.config(command=listado.yview)

hscrollbar = tk.Scrollbar(frame_listadovuelos, orient="horizontal")
hscrollbar.grid(row=1, column=0, sticky= tk.E +tk.W)

listadovuelos.config(xscrollcommand=hscrollbar.set)
hscrollbar.config(command=listado.xview)

window.mainloop()