import tkinter as tk
from tkinter import filedialog

from src.back.calculations import Calculations
from src.back.file_handler import FileHandler

def start_gui():
    def load_files():
        
        c = Calculations()
        f = FileHandler()
        
        
        filepaths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        sensor_data = f.load_csv_files(filepaths)
        result = c.calculate_magnetic_moment(sensor_data)
        result_label.config(text=str(result))

    root = tk.Tk()
    root.title("Cálculo del Momento Magnético")
    
    load_button = tk.Button(root, text="Cargar Archivos CSV", command=load_files)
    load_button.pack()
    
    result_label = tk.Label(root, text="Resultados aparecerán aquí")
    result_label.pack()
    
    root.mainloop()
