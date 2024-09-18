import customtkinter as ctk
from src.front.gui_service import GuiServices
from src.front.panels import EntryPanel

class LeftFrame(ctk.CTkFrame):
    def __init__(self, parent, replace_frame_func):
        super().__init__(master = parent, width = 100)
        self.grid(row = 0, column = 0, sticky = 'nsew')
        self.service = GuiServices(self)
        self.replace_frame_func = replace_frame_func
        
        self.tabview = ctk.CTkTabview(self, width = 100)
        self.tabview.add("Files")
        self.files_frame = FilesFrame(self.tabview.tab("Files"), self)

        # Lista para almacenar los nombres de los archivos cargados
        self.files = {}

        self.fileSelectionButtonEnabled()

    def fileSelectionButtonEnabled(self):
        # Create a container frame for the button
        self.button_container = ctk.CTkFrame(self, fg_color = "transparent")
        self.button_container.grid(row = 0, column = 0, sticky = "nsew")
        self.button_container.grid_columnconfigure(0, weight = 1)
        self.button_container.grid_rowconfigure(0, weight = 1)

        # Create the select files button
        self.select_files_button = ctk.CTkButton(
            self.button_container,
            text = "Select Files",
            command = self.import_files,
            width = 120,  # Set a fixed width
            height = 40   # Set a fixed height
        )
        self.select_files_button.grid(row = 0, column = 0)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

    def import_files(self):
        self.files = self.service.load_files()
        
        if self.files:
            self.files_frame.update_files(self.files)
            self.show_all_tabs()
        else:
            print("No files selected or failed to load files") # TODO replace with error call

    def show_all_tabs(self):
        self.button_container.destroy()

        self.tabview.grid(row = 0, column = 0, sticky = "nsew")
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.tabview.add("Distances")
        self.tabview.add("Calculates")
        self.tabview.add("Export")

        self.files_frame.grid(row = 0, column = 0, sticky = "nsew")
        self.tabview.tab("Files").grid_columnconfigure(0, weight = 1)
        self.tabview.tab("Files").grid_rowconfigure(0, weight = 1)

        DistanceFrame(self.tabview.tab("Distances"), self.files, self.replace_frame_func, self.service.sensor_number)
        CalculateFrame(self.tabview.tab("Calculates"))
        ExportFrame(self.tabview.tab("Export"))

        self.tabview.set("Distances")

class FilesFrame(ctk.CTkFrame):
    def __init__(self, parent, menu_instance):
        super().__init__(master = parent, fg_color = 'transparent')
        self.menu_instance = menu_instance
        self.file_labels = []

        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

    def update_files(self, files):
        for label in self.file_labels:
            label.destroy()

        self.file_labels = []
        
        y_margin = 0.4
        for file in files:
            label = ctk.CTkLabel(master = self, text = file)
            
            label.place(relx = 0.25, rely = y_margin, anchor = "w")
            y_margin += 0.04
            self.file_labels.append(label)

class DistanceFrame(ctk.CTkFrame):
    def __init__(self, parent, files, replace_frame_func, sensors):
        super().__init__(master = parent, fg_color = 'transparent')
        
        # Centro el frame dentro del tab "Distances"
        self.grid(row = 0, column = 0, sticky = "nsew")
        parent.grid_columnconfigure(0, weight = 1)  # Columna del contenedor ajustable
        # parent.grid_rowconfigure(0, weight = 1, minsize = 5)    # Fila del contenedor ajustable

        self.files = files
        self.replace_frame_func = replace_frame_func

        # Configuración de widgets internos
        for index in range(sensors):
            EntryPanel(self, index).grid(row = index, column = 0, sticky = "ew", padx = 4, pady = 8)

        # Botón centrado con `sticky = "ew"` para que ocupe todo el ancho disponible
        ctk.CTkButton(self, text = 'Calculate', command = self.send_data, width = 120, height = 40).grid(row = sensors, column = 0, pady = 10, padx = 10)

        # Ajustar las columnas y filas para que se expandan correctamente
        self.grid_columnconfigure(0, weight = 1)
        for i in range(sensors):
            self.grid_rowconfigure(i, weight = 1)

        # Última fila ajustable para centrar el botón
        self.grid_rowconfigure(sensors + 1, weight = 1)

    def send_data(self):
        image_data = [
            ('src/front/resource/X_axis_graph.png', 'Eje X'),
            ('src/front/resource/Y_axis_graph.png', 'Eje Y'),
            ('src/front/resource/Z_axis_graph.png', 'Eje Z'),
        ]
        self.replace_frame_func(image_data)


class CalculateFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = 'transparent')
        self.grid(row = 0, column = 0, sticky = "nsew")

class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = 'transparent')
        self.grid(row = 0, column = 0, sticky = "nsew")