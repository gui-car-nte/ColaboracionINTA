import tkinter as tk
import os
import logging
import platform

from tkinter import filedialog, messagebox
from src.back.calculations import Calculations
from src.back.file_handler import FileHandler
from src.front.utils import Utils
from src.front.settings import IMAGES
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

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
        self.files_frame = None

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
            for widget in self.files_frame.winfo_children():
                widget.destroy()

            for filepath in filepaths:
                filename = os.path.basename(filepath) 
                label = tk.Label(self.files_frame, text = filename, bg = "white")
                label.pack(pady = 5)


    def send_distance(self, frame_main: tk.Frame):
        distances = self.get_values(frame_main)
        new_frame = self.utils.create_frame(frame_main, tk.TOP, False)
        self.create_result(distances)


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


    def create_result(self, distances):
        calculations = Calculations(self)
        self.results = calculations.calculate_magnetic_moment(self.sensor_data, distances)


    def export_to_pdf(self):
        types = ["x", "y", "z"]
        pdf_path = "magnetic_moment.pdf"

        canva = canvas.Canvas(pdf_path, pagesize = letter)
        width, height = letter

        canva.setFont("Helvetica-Bold", 18)
        title = "Magnetic Moment"
        canva.drawCentredString(width / 2.0, height - 50, title)

        y_offset = height - 100

        for i, (axis, moment_magnetic, image) in enumerate(zip(types, self.results, IMAGES)):
            if y_offset < 300:
                canva.showPage()
                y_offset = height - 100

            canva.setFont("Helvetica-Bold", 12)
            canva.drawString(100, y_offset, f"Axis {axis}")

            y_offset -= 80

            canva.drawImage(ImageReader(image), 100, y_offset - 200, width = 400, height = 300)

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
