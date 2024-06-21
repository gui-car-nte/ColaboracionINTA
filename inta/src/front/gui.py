import tkinter as tk
from tkinter import filedialog

from src.back.calculations import Calculations
from src.back.file_handler import FileHandler

def start_gui():

    color_primary = "#E7EFE7"
    color_secundary = "#1F62B1"

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
    photo = tk.PhotoImage(file="")
    photo_small = tk.PhotoImage(file="")
    root.iconphoto(False, photo, photo_small)

    main_frame = tk.Frame(root)
    main_frame.configure(background=color_primary)
    main_frame.pack()

    button_frame = tk.Frame(main_frame)
    button_frame.configure(background=color_primary)
    button_frame.pack()
    
    result_frame = tk.Frame(main_frame)
    result_frame.configure(background=color_primary)
    result_frame.pack()

    sumary_frame = tk.Frame(main_frame)
    sumary_frame.configure(background=color_primary)
    sumary_frame.pack()

    load_button = tk.Button(button_frame, text="Cargar Archivos CSV", command=load_files, background=color_secundary)
    load_button.pack(side=tk.LEFT)

    distance_button = tk.Button(button_frame, text="Introducir distancias", background=color_secundary)
    distance_button.pack(side=tk.LEFT)
    
    result_label = tk.Label(result_frame, text="Resultados aparecerán aquí", background=color_primary)
    result_label.pack()

    x_label = tk.Label(sumary_frame, text="X:", background=color_primary)
    y_label = tk.Label(sumary_frame, text="Y:", background=color_primary)
    z_label = tk.Label(sumary_frame, text="Z:", background=color_primary)
    x_label.pack(side=tk.LEFT)
    y_label.pack(side=tk.LEFT)
    z_label.pack(side=tk.LEFT)
    
    root.mainloop()
