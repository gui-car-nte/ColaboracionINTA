import tkinter as tk
from tkinter import filedialog

from src.back.calculations import Calculations
from src.back.file_handler import FileHandler
from src.front.tkinter_settings import GuiServices, COLOR_PRIMARY, COLOR_SECUNDARY

def start_gui():

    settings = GuiServices()

    root = tk.Tk()
    root.title("Cálculo del Momento Magnético")
    root.configure(background=COLOR_PRIMARY)

    top_frame = settings.create_frame(root, tk.TOP, False)

    center_frame = settings.create_frame( root, tk.TOP, True)
    left_center = settings.create_frame( center_frame, tk.LEFT, False)
    center_center = settings.create_frame( center_frame, tk.LEFT, False)
    right_center = settings.create_frame( center_frame, tk.LEFT, False)

    bottom_frame = settings.create_frame(root, tk.BOTTOM, True)

    settings.create_label("x_label", left_center, "X:", tk.LEFT, False)
    settings.create_label("y_label", left_center, "Y:", tk.LEFT, False)
    settings.create_label("z_label", left_center, "Z:", tk.LEFT, False)

    result_label = settings.create_label('result', center_center, "", tk.LEFT, False)
    button1 = tk.Button(top_frame, text="Cargar Archivos CSV", command=lambda: settings.load_files(result_label), background=COLOR_SECUNDARY)
    button1.pack(side=tk.LEFT, padx=10)
    settings.create_button("distance_button",top_frame, "Introducir Distancias", tk.LEFT)
    settings.create_button("export_button", top_frame, "Exportar a PDF", tk.LEFT)

    root.mainloop()