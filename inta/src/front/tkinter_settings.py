import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from src.back.calculations import Calculations
from src.back.file_handler import FileHandler

COLOR_PRIMARY = "#E7EFE7" # Blanco
COLOR_SECUNDARY = "#1F62B1" # Azul
RUTA_IMAGEN = 'src/front/resource/imagen.png'

class GuiServices:

    numbers_sensors = 0
    sensor_data = ""

    def __init__(self, frame_main) -> None:
        self.window = frame_main

    def load_files(self, next_frame):

        f = FileHandler()
        
        filepaths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        self.sensor_data = f.load_csv_files(filepaths)
        # numero sensores
        self.numbers_sensors = f.count_sensors()
        self.input_distance(next_frame)

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

    def create_button(self, name_in, frame_in, text_in, side_in, command_in, parameter_in):

        if parameter_in != "":
            button = tk.Button(frame_in, text=text_in, background=COLOR_SECUNDARY, name=name_in, command=lambda: command_in(parameter_in))
            if side_in == "":
                button.pack(pady=10)
            else:
                button.pack(side=side_in, pady=10)
        else:
            button = tk.Button(frame_in, text=text_in, background=COLOR_SECUNDARY, name=name_in, command=command_in)
            if side_in == "":
                button.pack(pady=10)
            else:
                button.pack(side=side_in, pady=10)

        return button

    def create_label(self, name_in, frame_in, text_in, side_in, diff):

        if diff:
            result_label = tk.Label(frame_in, text=text_in, wraplength=300, justify=side_in)
            result_label.pack(pady=20)
        else:
            label = tk.Label(frame_in, text=text_in, name=name_in)
            label.configure(background=COLOR_PRIMARY)
            if side_in == "":
                label.pack()
            else:
                label.pack(side=side_in)

        return label
    
    def create_input(self, frame_in):
        
        entry = tk.Entry(frame_in)
        entry.pack()
    
    def input_distance(self, next_frame):
        
        for sensor in range(self.numbers_sensors):

            frame_input = self.create_frame(next_frame, tk.TOP, False)
            self.create_label(f'sensor{sensor}', frame_input, f'Distancia sensor {sensor}: ', tk.LEFT, False)
            self.create_input(frame_input)
        
        self.create_button("calculate", next_frame, "Calcular", "", self.send_distance, next_frame)

    def send_distance(self, frame_main: tk.Frame):
        
        distances = self.recoger_valores(frame_main)
        print(distances)

        self.vaciar_frame(frame_main)

        new_frame = self.create_frame(frame_main, tk.TOP, False)

        self.create_result(new_frame, distances)   

    def vaciar_frame(self, frame_main):
        for widget in frame_main.winfo_children():
            if isinstance(widget, tk.Frame):
                self.vaciar_frame(widget)
            widget.destroy()

    def recoger_valores(self, frame):
        valores = []
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Entry):
                valores.append(widget.get())
            elif isinstance(widget, tk.Frame):
                valores.extend(self.recoger_valores(widget))
        return valores
    
    def create_result(self, frame_main, distances):
        c = Calculations()
        results = c.calculate_magnetic_moment(self.sensor_data, distances)
        for result in results:
            self.mostrar_imagen_desde_archivo(frame_main, result)    

    def mostrar_imagen_desde_archivo(self, frame_main, result):

        frame_img = self.create_frame(frame_main, tk.LEFT, True)
        # Abrir la imagen usando Pillow
        img = Image.open(RUTA_IMAGEN)
        img = img.resize((400,300))
        img_tk = ImageTk.PhotoImage(img)

        # Crear un label para mostrar la imagen
        label = tk.Label(frame_img, image=img_tk)
        label.image = img_tk  # Mantener una referencia a la imagen para evitar que sea recolectada por el garbage collector
        label.pack(pady=10, padx=20)

        label_result = self.create_label('pr', frame_img, f'Momento Magnetico: {result}', "", False)