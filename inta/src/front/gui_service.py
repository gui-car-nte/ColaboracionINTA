import tkinter as tk
import os
import logging
import platform

from tkinter import filedialog, messagebox
from inta.src.back.calculations import Calculations
from inta.src.back.file_handler import FileHandler
from inta.src.front.utils import Utils
from inta.src import config
from inta.src.front.panels import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

if os.path.exists('error_log.txt'):
    os.remove(path='error_log.txt')

logging.basicConfig(
    filename="error_log.txt",
    filemode="a",
    format="[%(asctime)s] - [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.ERROR,
)

logger = logging.getLogger("urbanGUI")


class GuiServices:

    def __init__(self, frame_main) -> None:
        self.window = frame_main
        self.numbers_sensors = 0
        self.sensor_data = {}
        self.utils = Utils(self.window)
        self.operations_steps: str
        self.files_frame = None  # Referencia al frame de archivos para actualizar la interfaz

    def set_files_frame(self, frame):
        """ Establecer el marco donde se muestran los archivos cargados. """
        self.files_frame = frame

    def load_files(self):
        # No necesitamos crear otra instancia de GuiServices
        filepaths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])

        if filepaths:
            # Procesar los archivos utilizando FileHandler
            f = FileHandler(list(filepaths), self)
            self.sensor_data = f.load_csv_files(list(filepaths))
            self.numbers_sensors = f.count_sensors()

            # Ocultar el botón de selección de archivos y mostrar los nombres de los archivos
            self.update_files_ui(filepaths)

            # Cambiar automáticamente a la pestaña de entrada de distancias
            self.change_to_distances_tab()

    def update_files_ui(self, filepaths):
        """ Actualizar la UI para ocultar el botón de selección de archivos y mostrar los nombres. """
        if self.files_frame:
            # Eliminar el botón de cargar archivos
            for widget in self.files_frame.winfo_children():
                widget.destroy()

            # Mostrar los nombres de los archivos cargados
            for filepath in filepaths:
                filename = os.path.basename(filepath)  # Extraer solo el nombre del archivo
                label = tk.Label(self.files_frame, text=filename, bg="white")
                label.pack(pady=5)

    def change_to_distances_tab(self):
        """ Cambiar a la pestaña de entrada de distancias (asumiendo que tienes un TabView). """
        try:
            # Cambiar a la pestaña 'Distances'. Asumiendo que el método se llama así en el TabView
            self.window.set("Distances")
        except Exception as e:
            logger.error(f"Error al cambiar de pestaña: {e}")
            messagebox.showerror("Error", "No se pudo cambiar a la pestaña de distancias.")

    def input_distance(self, next_frame):
        for sensor in range(self.numbers_sensors):
            frame_input = self.utils.create_frame(next_frame, tk.TOP, False)
            self.utils.create_label(frame_input, f"Sensor Distance {sensor + 1} ", tk.LEFT)
            EntryPanel(frame_input)

        self.utils.create_button(
            "calculate", next_frame, "Calculate", "", self.send_distance, next_frame
        )

    def send_distance(self, frame_main: tk.Frame):
        distances = self.get_values(frame_main)
        new_frame = self.utils.create_frame(frame_main, tk.TOP, False)
        self.create_result(new_frame, distances)

    def drop_frame(self, frame_main):
        for widget in frame_main.winfo_children():
            if isinstance(widget, tk.Frame):
                self.drop_frame(widget)
            widget.destroy()

    def get_values(self, frame):
        values = []
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Entry):
                new_values = widget.get().replace(",", ".")
                values.append(new_values)
            elif isinstance(widget, tk.Frame):
                values.extend(self.get_values(widget))

        return values

    def create_result(self, frame_main, distances):
        # No crear una nueva instancia de GuiServices, usa la existente (self)
        calculations = Calculations(self)
        self.results = calculations.calculate_magnetic_moment(self.sensor_data, distances)

        # Habilitar botón de exportación
        button = self.window.nametowidget(".!frame.export_button")
        button.config(state=tk.NORMAL)

        # Obtener y mostrar los resultados
        self.operations_steps = calculations.get_calculation_steps()
        for result, image_path in zip(self.results, config.IMAGES):
            self.utils.create_image_canvas(frame_main, image_path)
            self.utils.create_label(frame_main, f"Magnetic Moment: {result}", "").configure(
                padx=10, pady=10
            )

    def clear_and_add(self, parent, row = 0, column = 1, sticky='nsew'):
        # Eliminar los widgets en la posición especificada (misma columna y fila)
        for widget in parent.grid_slaves(row=row, column=column):
            widget.destroy()

        # Añadir el nuevo widget usando grid
        new_widget = (parent)
        new_widget.grid(row=row, column=column, sticky=sticky)

    def export_to_pdf(self):
        types = ["x", "y", "z"]
        pdf_path = "magnetic_moment.pdf"

        canva = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        canva.setFont("Helvetica-Bold", 18)
        title = "Magnetic Moment"
        canva.drawCentredString(width / 2.0, height - 50, title)

        y_offset = height - 100

        for i, (axis, moment_magnetic, image) in enumerate(zip(types, self.results, config.IMAGES)):
            if y_offset < 300:
                canva.showPage()
                y_offset = height - 100

            canva.setFont("Helvetica-Bold", 12)
            canva.drawString(100, y_offset, f"Axis {axis}")

            y_offset -= 80

            canva.drawImage(ImageReader(image), 100, y_offset - 200, width=400, height=300)

            y_offset -= 220

            canva.setFont("Helvetica", 12)
            canva.drawString(100, y_offset, f"Magnetic Moment {moment_magnetic}")

            y_offset -= 40

        canva.showPage()

        canva.setFont("Helvetica-Bold", 18)
        title = "Detailed Calculation Steps"
        canva.drawCentredString(width / 2.0, height - 50, title)

        canva.setFont("Helvetica", 8)
        calculation_steps = self.operations_steps.split('\n')
        y_offset = height - 100

        for line in calculation_steps:
            if y_offset < 40:
                canva.showPage()
                canva.setFont("Helvetica", 8)
                y_offset = height - 100
            canva.drawString(20, y_offset, line)
            y_offset -= 20

        canva.save()

        if platform.system() == 'Windows':
            os.startfile(pdf_path)  # type: ignore
        elif platform.system() == 'Linux':
            os.system(f"xdg-open {pdf_path}")

    def show_message(self, msg, color):
        messagebox.showerror('Error', msg)

    def log_error(self, error_type, error_message):
        logger.error(f'{error_type}: {error_message}')
        self.show_message(f'{error_type}: {error_message}', 'red')
