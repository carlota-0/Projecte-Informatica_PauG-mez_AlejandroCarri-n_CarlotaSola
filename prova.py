import tkinter as tk
from tkintermapview import TkinterMapView

# 1. Configuración de la ventana principal
root = tk.Tk()
root.title("Mapa dentro de un Canvas")
root.geometry("800x600")

# 2. Crear el Canvas
# El canvas actuará como el contenedor principal
canvas = tk.Canvas(root, width=800, height=600, bg="gray")
canvas.pack(fill="both", expand=True)

# 3. Crear el widget de mapa (TkinterMapView)
# NOTA: El 'master' del mapa debe ser el canvas
map_widget = TkinterMapView(canvas, width=600, height=400, corner_radius=10)

# Configuración inicial del mapa (coordenadas opcionales)
map_widget.set_position(40.4167, -3.7037)  # Madrid, España
map_widget.set_zoom(12)

# 4. Incrustar el mapa dentro del Canvas usando 'create_window'
# El anchor="nw" hace que las coordenadas (x, y) correspondan a la esquina superior izquierda del mapa
canvas.create_window(50, 50, window=map_widget, anchor="nw")

# 5. Dibujar elementos extra en el Canvas (Opcional)
# Solo para demostrar que puedes dibujar por encima o alrededor del mapa
canvas.create_rectangle(40, 40, 660, 460, outline="red", width=2)
canvas.create_text(400, 30, text="Mapa interactivo incrustado en Canvas", fill="black", font=("Arial", 14, "bold"))

# Iniciar la aplicación
root.mainloop()