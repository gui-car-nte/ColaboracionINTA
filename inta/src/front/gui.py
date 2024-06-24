import tkinter as tk
from tkinter import filedialog

from src.back.calculations import Calculations
from src.back.file_handler import FileHandler

def start_gui():

    color_primary = "#E7EFE7" # Blanco
    color_secundary = "#1F62B1" # Azul

    def load_files():

            c = Calculations()
            f = FileHandler()

            filepaths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
            sensor_data = f.load_csv_files(filepaths)
            result = c.calculate_magnetic_moment(sensor_data)
            result_label.config(text=str(result))

    root = tk.Tk()
    root.title("Cálculo del Momento Magnético")
    root.configure(background=color_primary)

    top_frame = tk.Frame(root)
    top_frame.configure(background=color_primary)
    top_frame.pack(side=tk.TOP, pady=10)

    button1 = tk.Button(top_frame, text="Cargar Archivos CSV", command=load_files, background=color_secundary)
    button1.pack(side=tk.LEFT, padx=10)

    button2 = tk.Button(top_frame, text="Introducir distancias", background=color_secundary)
    button2.pack(side=tk.LEFT, padx=10)

    button3 = tk.Button(top_frame, text="Exportar a PDF", background=color_secundary)
    button3.pack(side=tk.LEFT, padx=10)

    center_frame = tk.Frame(root)
    # center_frame.configure(background=color_primary)
    center_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

    result_label = tk.Label(center_frame, text="", wraplength=300, justify=tk.LEFT)
    result_label.pack(pady=20)

    bottom_frame = tk.Frame(root)
    bottom_frame.configure(background=color_primary)
    bottom_frame.pack(side=tk.BOTTOM, pady=10)

    x_label = tk.Label(bottom_frame, text="X:")
    x_label.configure(background=color_primary)
    x_label.pack(side=tk.LEFT, padx=10)

    y_label = tk.Label(bottom_frame, text="Y:")
    y_label.configure(background=color_primary)
    y_label.pack(side=tk.LEFT, padx=10)

    z_label = tk.Label(bottom_frame, text="Z:")
    z_label.configure(background=color_primary)
    z_label.pack(side=tk.LEFT, padx=10)

    root.mainloop()