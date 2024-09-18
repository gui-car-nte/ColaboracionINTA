import tkinter as tk
import os
import logging
import platform

from tkinter import filedialog, messagebox
from src.back.calculations import Calculations
from src.back.file_handler import FileHandler
from src.front.utils import Utils
from src.front.settings import IMAGES
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

if os.path.exists('error_log.txt'):
    os.remove(path = 'error_log.txt')

logging.basicConfig(
    filename = "error_log.txt",
    filemode = "a",
    format = "[%(asctime)s] - [%(levelname)s] %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
    level = logging.ERROR,
)

logger = logging.getLogger("urbanGUI")


class GuiServices:

    def __init__(self, frame_main) -> None:
        self.window = frame_main
        self.sensor_number = 0
        self.sensor_data = {}
        self.utils = Utils(self.window)
        self.operations_steps: str
        self.files_frame = None  # Referencia al frame de archivos para actualizar la interfaz

    def set_files_frame(self, frame):
        """ Establecer el marco donde se muestran los archivos cargados. """
        self.files_frame = frame

    def load_files(self):
        filepaths = filedialog.askopenfilenames(filetypes = [("All files", "*"), ("CSV files", "*.csv"), ("TXT files", "*.txt")])

        if filepaths:
            try:
                f = FileHandler(self)
                self.sensor_data = f.load_csv_files(list(filepaths))
                self.sensor_number = f.count_sensors()

                self.update_files_ui(filepaths)
                
                return self.sensor_data
            
            except Exception as e: # TODO don't gotta catch em all
                return None
        
        else:
            return None

    def update_files_ui(self, filepaths):
        """ Actualizar la UI para ocultar el botón de selección de archivos y mostrar los nombres. """
        if self.files_frame:
            # Eliminar el botón de cargar archivos
            for widget in self.files_frame.winfo_children():
                widget.destroy()

            # Mostrar los nombres de los archivos cargados
            for filepath in filepaths:
                filename = os.path.basename(filepath)  # Extraer solo el nombre del archivo
                label = tk.Label(self.files_frame, text = filename, bg = "white")
                label.pack(pady = 5)

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
        button.config(state = tk.NORMAL)

        # Obtener y mostrar los resultados
        self.operations_steps = calculations.get_calculation_steps()
        for result, image_path in zip(self.results, IMAGES):
            self.utils.create_image_canvas(frame_main, image_path)
            self.utils.create_label(frame_main, f"Magnetic Moment: {result}", "").configure(
                padx = 10, pady = 10
            )

    def export_to_pdf(self):
        # Create a PDF document
        pdf_file = "generated_report.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize = A4)

        # Create a sample stylesheet
        styles = getSampleStyleSheet()

        # Title
        title = Paragraph("Informe de Resultados", styles['Title'])

        # Sample table data
        data = [
            ['Parametro', 'Resultado', 'Unidad'],
            ['Masa', '70', 'kg'],
            ['Altura', '1.75', 'm'],
            ['Edad', '30', 'años']
        ]

        # Create a table
        table = Table(data, colWidths = [6 * cm, 4 * cm, 3 * cm])

        # Add table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Create the PDF elements list
        elements = [title, Spacer(1, 12), table]

        # Build the PDF
        doc.build(elements)

        print(f"PDF '{pdf_file}' created successfully.")


    def show_message(self, msg, color):
        messagebox.showerror('Error', msg)

    def log_error(self, error_type, error_message):
        logger.error(f'{error_type}: {error_message}')
        self.show_message(f'{error_type}: {error_message}', 'red')
