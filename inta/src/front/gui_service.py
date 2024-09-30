import tkinter as tk
import os
import sys
import logging

from tkinter import filedialog, messagebox
from src.back.calculations import Calculations
from src.back.file_handler import FileHandler
from src.front.utils import Utils
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx2pdf import convert

if os.path.exists("error_log.txt"):
    os.remove(path="error_log.txt")

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
        self.sensor_number = 0
        self.sensor_data = {}
        self.utils = Utils(self.window)
        self.calculations = Calculations(self)
        self.operations_steps: str
        self.files_frame = None

    def set_files_frame(self, frame):
        """Establecer el marco donde se muestran los archivos cargados."""
        self.files_frame = frame

    def load_files(self):
        filepaths = filedialog.askopenfilenames(
            filetypes=[
                ("All files", "*"),
                ("CSV files", "*.csv"),
                ("TXT files", "*.txt"),
            ]
        )

        if filepaths:
            try:
                f = FileHandler(self)
                self.sensor_data = f.load_csv_files(list(filepaths))
                self.sensor_number = f.count_sensors()

                self.update_files_ui(filepaths)

                return self.sensor_data

            except Exception as e:  # TODO don't gotta catch em all
                return None

        else:
            return None

    def update_files_ui(self, filepaths):
        """Actualizar la UI para ocultar el botón de selección de archivos y mostrar los nombres."""
        if self.files_frame:
            for widget in self.files_frame.winfo_children():
                widget.destroy()

            for filepath in filepaths:
                filename = os.path.basename(filepath)
                label = tk.Label(self.files_frame, text=filename, bg="white")
                label.pack(pady=5)

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
        self.results = self.calculations.calculate_magnetic_moment(
            self.sensor_data, distances
        )
        return self.results

    def get_list_paths(self):
        self.paths = self.calculations.get_image_paths()
        return self.paths

    def obtain_calculation_details(self):
        details = self.calculations.get_calculation_steps()
        return details

    def centrar_texto_celda(self, celda, texto):
        """Centrar el texto horizontal y verticalmente dentro de una celda."""
        celda.text = texto
        # Centrar horizontalmente
        for paragraph in celda.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Centrar verticalmente
        tc = celda._tc
        tcPr = tc.get_or_add_tcPr()
        vAlign = OxmlElement("w:vAlign")
        vAlign.set(qn("w:val"), "center")
        tcPr.append(vAlign)

    def modificar_tabla_word(self, filepath, nueva_ruta):
        """Modificar una tabla en un archivo Word y guardar los cambios."""
        try:
            # Abrir el documento
            doc = Document(filepath)
            # Seleccionar la segunda tabla (índice 1)
            table = doc.tables[1]

            # Modificar el contenido de la tabla y centrar el texto
            self.centrar_texto_celda(table.cell(1, 1), "9.8 ± 4.2")
            self.centrar_texto_celda(table.cell(1, 2), "5.7 ± 1.5")
            self.centrar_texto_celda(table.cell(1, 3), "5.7 ± 1.5")
            self.centrar_texto_celda(table.cell(1, 4), "5.7 ± 1.5")
            self.centrar_texto_celda(table.cell(1, 5), "< 60")

            self.centrar_texto_celda(table.cell(2, 1), "9.8 ± 4.2")
            self.centrar_texto_celda(table.cell(2, 2), "5.7 ± 1.5")
            self.centrar_texto_celda(table.cell(2, 3), "5.7 ± 1.5")
            self.centrar_texto_celda(table.cell(2, 4), "5.7 ± 1.5")
            self.centrar_texto_celda(table.cell(2, 5), "< 55")

            self.centrar_texto_celda(table.cell(3, 1), "9.8 ± 4.2")
            self.centrar_texto_celda(table.cell(3, 2), "5.7 ± 1.5")
            self.centrar_texto_celda(table.cell(3, 3), "5.7 ± 1.5")
            self.centrar_texto_celda(table.cell(3, 4), "5.7 ± 1.5")
            self.centrar_texto_celda(table.cell(3, 5), "< 45")

            # Guardar el documento modificado
            doc.save(nueva_ruta)
            return True

        except Exception as e:
            print("Error en modificar_tabla_word", str(e))
            return False

    def convertir_word_a_pdf(self, ruta_word, ruta_pdf):
        """Convertir un archivo .docx a PDF."""
        try:
            convert(ruta_word, ruta_pdf)
            return True
        except Exception as e:
            print("Error en convertir_word_a_pdf", str(e))
            return False

    def export_to_pdf(self):
        """Ejecutar el proceso de modificar una tabla en un Word y convertirlo a PDF."""
        
        archivo_word = self.resource_path(
            "resource\\Ejemplo_Informe_de_resultados.docx"
        )
        if archivo_word:
            nueva_ruta_word = self.resource_path("resource\\tabla_modificada.docx")
            ruta_pdf = "Informe_de_resultados.pdf"

            if self.modificar_tabla_word(archivo_word, nueva_ruta_word):
                if self.convertir_word_a_pdf(nueva_ruta_word, ruta_pdf):
                    os.startfile(ruta_pdf)  # Abrir el PDF resultante
                    os.remove(nueva_ruta_word)  # Eliminar el archivo Word temporal
                else:
                    print("No se pudo convertir el documento a PDF", "red")
            else:
                print("No se pudo modificar la tabla del documento", "red")

    def show_message(self, msg, color):
        messagebox.showerror("Error", msg)

    def log_error(self, error_type, error_message):
        logger.error(f"{error_type}: {error_message}")
        self.show_message(f"{error_type}: {error_message}", "red")

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS  # type: ignore # ? issue is non-relevant
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
