import tkinter as tk
from tkinter import filedialog

from src.front.gui import start_gui

COLOR_PRIMARY = "#E7EFE7" # Blanco
COLOR_SECONDARY = "#1F62B1" # Azul


root = tk.Tk()
root.title("Cálculo del Momento Magnético")
root.configure(background=COLOR_PRIMARY)

top_frame = tk.Frame(root)
top_frame.configure(background=COLOR_PRIMARY)
top_frame.pack(side=tk.TOP, pady=10)

button1 = tk.Button(top_frame, text="Cargar Archivos CSV", command=start_gui, background=COLOR_SECONDARY)
button1.pack(side=tk.LEFT, padx=10)

button2 = tk.Button(top_frame, text="Introducir distancias", background=COLOR_SECONDARY)
button2.pack(side=tk.LEFT, padx=10)

button3 = tk.Button(top_frame, text="Exportar a PDF", background=COLOR_SECONDARY)
button3.pack(side=tk.LEFT, padx=10)

center_frame = tk.Frame(root)
# center_frame.configure(background=COLOR_PRIMARY)
center_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

result_label = tk.Label(center_frame, text="", wraplength=300, justify=tk.LEFT)
result_label.pack(pady=20)

bottom_frame = tk.Frame(root)
bottom_frame.configure(background=COLOR_PRIMARY)
bottom_frame.pack(side=tk.BOTTOM, pady=10)

x_label = tk.Label(bottom_frame, text="X:")
x_label.configure(background=COLOR_PRIMARY)
x_label.pack(side=tk.LEFT, padx=10)

y_label = tk.Label(bottom_frame, text="Y:")
y_label.configure(background=COLOR_PRIMARY)
y_label.pack(side=tk.LEFT, padx=10)

z_label = tk.Label(bottom_frame, text="Z:")
z_label.configure(background=COLOR_PRIMARY)
z_label.pack(side=tk.LEFT, padx=10)