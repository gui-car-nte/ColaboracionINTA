import tkinter as tk
import os
import logging

from tkinter import filedialog

from src.back.calculations import Calculations
from src.back.file_handler import FileHandler
from src.front.utils import Utils
from src import config
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from src.front.utils import Utils

# Configura el logger al inicio de tu aplicación
logging.basicConfig(
    filename="error_log.txt",
    filemode="a",
    format="%(asctime)s,%(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.ERROR,
)

logger = logging.getLogger("urbanGUI")

# TODO
# poner icono en el center_frame para no estar vacio
# poner iconos en el programa
# fix data types

class GuiServices:

    def __init__(self, frame_main) -> None:
        self.window = frame_main
        self.numbers_sensors = 0
        self.sensor_data = {}
        self.utils = Utils(self.window)
        self.operations_steps: str

    def load_files(self, next_frame):
        gui_services = GuiServices(self.window) #TODO run test, 2nd parameter was empty, note: tests ran, nothing seemingly wrong
        filepaths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        f = FileHandler(list(filepaths), gui_services)
        self.sensor_data = f.load_csv_files(list(filepaths))
        # numero sensores
        self.numbers_sensors = f.count_sensors()
        self.drop_frame(next_frame)
        self.input_distance(next_frame)

    def input_distance(self, next_frame):
        for sensor in range(self.numbers_sensors):
            frame_input = self.utils.create_frame(next_frame, tk.TOP, False)
            self.utils.create_label(frame_input, f"Sensor Distance {sensor + 1} ", tk.LEFT)
            self.utils.create_input(frame_input)

        self.utils.create_button(
            "calculate", next_frame, "Calculate", "", self.send_distance, next_frame
        )

    def send_distance(self, frame_main: tk.Frame):
        distances = self.get_values(frame_main)
        self.drop_frame(frame_main)
        new_frame = self.utils.create_frame(frame_main, tk.TOP, False)
        self.create_result(new_frame, distances)

    def drop_frame(self, frame_main):
        for widget in frame_main.winfo_children():
            if isinstance(widget, tk.Frame):
                self.drop_frame(widget)
            widget.destroy()

    # TODO change name & var names
    def get_values(self, frame):
        valores = []
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Entry):
                new_values = widget.get().replace(",",".")
                valores.append(new_values)
            elif isinstance(widget, tk.Frame):
                valores.extend(self.get_values(widget))
                
        return valores

    def create_result(self, frame_main, distances):
        gui_services = GuiServices(self.window) #TODO run test, 2nd parameter was empty note: tests ran, nothing seemingly wrong
        calculations = Calculations(gui_services)

        self.results = calculations.calculate_magnetic_moment(self.sensor_data, distances)
        button = self.window.nametowidget(".!frame.export_button")
        button.config(state=tk.NORMAL)
        self.operations_steps = calculations.get_calculation_steps()
        for result, image_path in zip(self.results, config.IMAGES):
            self.utils.create_image_canvas(frame_main, image_path)
            # TODO aqui iria la operacion completa
            self.utils.create_label(frame_main, f"Magnetic Moment: {result}", "").configure(
                padx = 10, pady = 10
            )

    # TODO make 'c' variable more descriptive & english tl
    def export_to_pdf(self):
        types = ["x", "y", "z"]
        pdf_path = "magnetic_moment.pdf"
        txt_path = "calculation_steps.txt"

        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Add title
        c.setFont("Helvetica-Bold", 18)
        title = "Magnetic Moment"
        c.drawCentredString(width / 2.0, height - 50, title)

        y_offset = height - 100

        for i, (axis, moment_magnetic, image) in enumerate(zip(types, self.results, config.IMAGES)):
            if y_offset < 300:
                c.showPage()
                y_offset = height - 100

            # Add axis label
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, y_offset, f"Axis {axis}")

            y_offset -= 20

            # Add image
            c.drawImage(ImageReader(image), 100, y_offset - 200, width=400, height=200)

            y_offset -= 220

            # Add magnetic moment
            c.setFont("Helvetica", 12)
            c.drawString(100, y_offset, f"Magnetic Moment {moment_magnetic}")

            y_offset -= 40

        # Add a new page for calculation steps
        c.showPage()

        c.setFont("Helvetica-Bold", 18)
        title = "Detailed Calculation Steps"
        c.drawCentredString(width / 2.0, height - 50, title)

        calculations = Calculations(GuiServices(self.window))
        c.setFont("Helvetica", 8)
        calculation_steps = self.operations_steps.split('\n')
        y_offset = height - 100

        for line in calculation_steps:
            if y_offset < 40:
                c.showPage()
                y_offset = height - 100
            c.drawString(100, y_offset, line)
            y_offset -= 20

        print(calculations.get_calculation_steps())

        c.save()

        # TODO: Conditional to detect operating system and open the correct file
        # os.startfile(pdf_path) # Windows
        # os.system(f"xdg-open {pdf_path}") # Linux


    def show_message(self, msg, color):
        popup_root = tk.Tk()
        popup_root.minsize(400,50)
        frame_popup = self.utils.create_frame(popup_root, tk.TOP)
        self.utils.create_label(frame_popup, msg, tk.TOP)

        popup_root.mainloop()

    def log_error(self, error_type, error_message):
        logger.error(f'{error_type}: {error_message}')
        self.show_message(f'{error_type}: {error_message}', 'red')
