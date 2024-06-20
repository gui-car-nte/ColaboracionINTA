import tkinter as tk
from tkinter import filedialog

from inta.src.back.calculations import calculate_magnetic_moment
from inta.src.back.file_handler import load_csv_files

def start_gui():
    def load_files():
        filepaths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        sensor_data = load_csv_files(filepaths)
        result = calculate_magnetic_moment(sensor_data)
        result_label.config(text=str(result))

    root = tk.Tk()
    root.title("Cálculo del Momento Magnético")
    
    load_button = tk.Button(root, text="Cargar Archivos CSV", command=load_files)
    load_button.pack()
    
    result_label = tk.Label(root, text="Resultados aparecerán aquí")
    result_label.pack()
    
    root.mainloop()
