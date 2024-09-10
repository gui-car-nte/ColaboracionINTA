import customtkinter as ctk
from inta.src.front.image_widget import *
from inta.src.front.gui_service import GuiServices
from inta.src.front.panels import *
from inta.src.back.file_handler import FileHandler


class Menu(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')
        self.service = GuiServices(self)

        # Lista para almacenar los nombres de los archivos cargados
        self.files = []

        self.enabled(self.files)

    def enabled(self, files):
        # Tabs
        self.add('Files')

        # Widgets
        # Add files and show files
        self.files_frame = FilesFrame(self.tab('Files'), self.service.load_files, self)

    def show_all_tabs(self):
        """ Muestra los tabs adicionales después de cargar archivos """
        self.add('Distances')
        self.add('Calculates')
        self.add('Export')

        # Widgets adicionales
        DistanceFrame(self.tab('Distances'), self.files)
        CalculateFrame(self.tab('Calculates'))
        ExportFrame(self.tab('Export'))

    def update_files(self, filepaths):
        """ Actualizar la lista de archivos en el marco de archivos """
        self.files = filepaths
        self.files_frame.update_files(self.files)

        self.show_all_tabs()

        # Cambiar a la pestaña de Distances automáticamente
        self.set("Distances")


class FilesFrame(ctk.CTkFrame):
    def __init__(self, parent, import_func, menu_instance):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.import_func = import_func
        self.menu_instance = menu_instance  # Para poder acceder a update_files
        self.file_labels = []

        # Botón para seleccionar archivos
        self.button = ctk.CTkButton(self, text = 'Select files', command = self.import_files)
        self.button.pack(expand=True)

    def import_files(self):
        # Llamar a la función import_func para cargar archivos
        filepaths = filedialog.askopenfilenames(filetypes = [("CSV files", "*.csv")])

        # Si se seleccionaron archivos
        if filepaths:
            self.button.pack_forget()  # Ocultar el botón una vez que se seleccionaron archivos
            self.menu_instance.update_files(filepaths)  # Actualizar los archivos en el menú

    def update_files(self, files):
        """ Actualizar los labels con los nombres de los archivos seleccionados """
        for label in self.file_labels:
            label.destroy()  # Destruir los labels previos

        self.file_labels = []  # Reiniciar la lista de labels

        # Crear un label por cada archivo cargado
        for file in files:
            label = ctk.CTkLabel(master=self, text=file)
            label.pack(pady=5)
            self.file_labels.append(label)


class DistanceFrame(ctk.CTkFrame):
    def __init__(self, parent, files):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.files = files

        self.service = GuiServices(self)
        f = FileHandler(list(files), self)
        sensors = f.count_sensors()

        for index, sensor in enumerate(range(sensors)):
            EntryPanel(self, index)

        ctk.CTkButton(self, text = 'Calculate', command = self.send_data).pack()

    def send_data(self):
        print('Calcular')
        print(self.files)
        self.service.send_distance(self)


class CalculateFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')


class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
