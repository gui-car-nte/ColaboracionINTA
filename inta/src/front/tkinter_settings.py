import tkinter as tk
from tkinter import filedialog

from src.back.calculations import Calculations
from src.back.file_handler import FileHandler

COLOR_PRIMARY = "#E7EFE7" # Blanco
COLOR_SECUNDARY = "#1F62B1" # Azul

class GuiServices:

    def load_files(self,result_label):

        c = Calculations()
        f = FileHandler()

        filepaths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        sensor_data = f.load_csv_files(filepaths)
        # numbers_sensor = f.count_sensors()
        # pasar lista con las distancias
        result = c.calculate_magnetic_moment(sensor_data)
        result_label.config(text=str(result))

    def create_frame(self, frame_in, side_in, complete):

        if complete:
            frame = tk.Frame(frame_in)
            frame.configure(background=COLOR_PRIMARY)
            frame.pack(side=side_in, fill=tk.BOTH, expand=True, pady=10)
        else:
            frame = tk.Frame(frame_in)
            frame.configure(background=COLOR_PRIMARY)
            frame.pack(side=side_in, pady=10)
        return frame

    def create_button(self, name_in, frame_in, text_in, side_in):
        button = tk.Button(frame_in, text=text_in, background=COLOR_SECUNDARY, name=name_in)
        button.pack(side=side_in, pady=10)

        return button

    def create_label(self, name_in, frame_in, text_in, side_in, diff):

        if diff:
            result_label = tk.Label(frame_in, text=text_in, wraplength=300, justify=tk.LEFT)
            result_label.pack(pady=20)
        else:
            label = tk.Label(frame_in, text=text_in, name=name_in)
            label.configure(background=COLOR_PRIMARY)
            label.pack(side=side_in)

        return label
    
    def input_distance():
        pass