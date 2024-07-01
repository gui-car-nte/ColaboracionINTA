import tkinter as tk
import os

from tkinter import filedialog
from PIL import Image, ImageTk

from src.back.calculations import Calculations
from src.back.file_handler import FileHandler
from src import config
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

COLOR_PRIMARY = "#E7EFE7"  # Blanco
COLOR_SECUNDARY = "#1F62B1"  # Azul
RUTA_IMAGEN = 'src/front/resource/imagen.png'

# TODO
# poner icono en el center_frame para no estar vacio
# poner iconos en el programa

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
        self.drop_frame(next_frame)
        self.input_distance(next_frame)

    def create_frame(self, frame_in, side_in, complete=False, scrollable=False):
        frame = tk.Frame(frame_in)
        frame.configure(background=COLOR_PRIMARY)

        if complete:
            frame.pack(side=side_in, fill=tk.BOTH, expand=True, pady=10)
        else:
            frame.pack(side=side_in, pady=10)

        if scrollable:
            frame = self.create_scroll(frame)
        return frame

    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_mouse_wheel(self, event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_button(self, name_in, frame_in, text_in, side_in, command_in, parameter_in):
        if parameter_in != "":
            button = tk.Button(frame_in, text=text_in, background=COLOR_SECUNDARY, name=name_in, command=lambda: command_in(parameter_in))
            button.configure(fg='white')
            if side_in == "":
                button.pack(pady=10, anchor=tk.NW)
            else:
                button.pack(side=side_in, pady=10, anchor=tk.NW)
        else:
            button = tk.Button(frame_in, text=text_in, background=COLOR_SECUNDARY, name=name_in, command=command_in)
            button.configure(fg='white')
            if side_in == "":
                button.pack(pady=10)
            else:
                button.pack(side=side_in, pady=10)

        return button

    def create_label(self, frame_in, text_in, side_in, diff=False):
        if diff:
            result_label = tk.Label(frame_in, text=text_in, wraplength=300, justify=side_in)
            result_label.pack(pady=20)
        else:
            label = tk.Label(frame_in, text=text_in)
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
            self.create_label(frame_input, f'Distancia sensor {sensor + 1} ', tk.LEFT)
            self.create_input(frame_input)
        
        self.create_button("calculate", next_frame, "Calcular", "", self.send_distance, next_frame)

    def send_distance(self, frame_main: tk.Frame):
        distances = self.recoger_valores(frame_main)
        print(distances)
        self.drop_frame(frame_main)
        new_frame = self.create_frame(frame_main, tk.TOP, False)
        self.create_result(new_frame, distances)   

    def drop_frame(self, frame_main):
        for widget in frame_main.winfo_children():
            if isinstance(widget, tk.Frame):
                self.drop_frame(widget)
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

        self.results = c.calculate_magnetic_moment(self.sensor_data, distances)
        for result, image_path in zip(self.results, config.IMAGES):
            self.create_image_canvas(frame_main, image_path)
            self.create_label(frame_main, f"Momento Magnetico: {result}", "").configure(padx=10, pady=10)

    def create_image_canvas(self, frame, image_path=""):
        if image_path == "":
            image = Image.open(image)
            photo = ImageTk.PhotoImage(image)
            
            canvas = tk.Canvas(frame, width=image.width, height=image.height)
            canvas.pack(pady=10)
            canvas.create_image(0, 0, anchor="nw", image=photo)
            
            # Keep a reference to the image to prevent garbage collection
            canvas.image = photo
        else:
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            
            canvas = tk.Canvas(frame, width=image.width, height=image.height)
            canvas.pack(pady=10)
            canvas.create_image(0, 0, anchor="nw", image=photo)
            
            # Keep a reference to the image to prevent garbage collection
            canvas.image = photo
        return canvas

    def create_scroll(self, frame_main):
        # Crear el lienzo
        canvas = tk.Canvas(frame_main, bg=COLOR_PRIMARY)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear la barra de desplazamiento
        scrollbar_y = tk.Scrollbar(frame_main, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar_y.set)

        # Crear un marco dentro del lienzo
        inner_frame = tk.Frame(canvas, bg=COLOR_PRIMARY)
        window = canvas.create_window((0, 0), window=inner_frame, anchor='n')

        def center_frame(event):
            canvas_width = event.width
            canvas.coords(window, canvas_width // 2, 0)
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind('<Configure>', center_frame)
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Evento de rueda del ratón para desplazar
        canvas.bind_all("<MouseWheel>", lambda event: self._on_mouse_wheel(event, canvas))

        return inner_frame
    
    def export_to_pdf(self):
        tipos = ['x', 'y', 'z']
        pdf_path = "momento_magnetico.pdf"
        
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 18)
        titulo = "Momento Magnético"
        c.drawCentredString(width / 2.0, height - 50, titulo)
        
        y_offset = 100
        
        for i, (eje, momento_magnetico) in enumerate(zip(tipos, self.results)):
            # imagen = generar_grafico(eje)
            imagen = 'src/front/resource/imagen.png'
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(275, 660, f"Eje {eje}")
            
            c.drawImage(ImageReader(imagen), 100, 450, width=400, height=200)
            
            c.setFont("Helvetica", 12)
            c.drawString(200, 425, f"Momento Magnético: {momento_magnetico}")
            
            y_offset += 300
            c.showPage()
        
        c.save()
        print('pdf creado')
        

        # os.startfile(pdf_path)
        os.system(f"xdg-open {pdf_path}")
        
    def log_error(self, error):
        # self.create_labe, error, tk.TOP)
        pass