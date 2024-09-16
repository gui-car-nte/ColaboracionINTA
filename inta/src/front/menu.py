import customtkinter as ctk
from tkinter import filedialog
from src.front.gui_service import GuiServices
from src.front.panels import EntryPanel
from src.back.file_handler import FileHandler

class Menu(ctk.CTkFrame):
    def __init__(self, parent, replace_frame_func):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')
        self.service = GuiServices(self)
        self.replace_frame_func = replace_frame_func

        # Lista para almacenar los nombres de los archivos cargados
        self.files = []

        self.tabview = None
        self.enabled(self.files)

    def enabled(self, files):
        # Create a container frame for the button
        self.button_container = ctk.CTkFrame(self, fg_color="transparent")
        self.button_container.grid(row=0, column=0, sticky="nsew")
        self.button_container.grid_columnconfigure(0, weight=1)
        self.button_container.grid_rowconfigure(0, weight=1)

        # Create the select files button
        self.select_files_button = ctk.CTkButton(
            self.button_container,
            text="Select Files",
            command=self.import_files,
            width=120,  # Set a fixed width
            height=40   # Set a fixed height
        )
        self.select_files_button.grid(row=0, column=0)

        # Configure grid for the main frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def import_files(self):
        filepaths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        if filepaths:
            self.files = filepaths
            self.show_all_tabs()

    def show_all_tabs(self):
        # Remove the button container
        self.button_container.destroy()

        # Create the tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Add tabs
        self.tabview.add("Files")
        self.tabview.add("Distances")
        self.tabview.add("Calculates")
        self.tabview.add("Export")

        # Add content to tabs
        self.files_frame = FilesFrame(self.tabview.tab("Files"), self.service.load_files, self)
        self.files_frame.grid(row=0, column=0, sticky="nsew")
        self.tabview.tab("Files").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Files").grid_rowconfigure(0, weight=1)

        DistanceFrame(self.tabview.tab("Distances"), self.files, self.replace_frame_func)
        CalculateFrame(self.tabview.tab("Calculates"))
        ExportFrame(self.tabview.tab("Export"))

        # Update files in FilesFrame
        self.files_frame.update_files(self.files)

        # Switch to the Distances tab
        self.tabview.set("Distances")

# The rest of the classes (FilesFrame, DistanceFrame, CalculateFrame, ExportFrame) remain unchanged

class FilesFrame(ctk.CTkFrame):
    def __init__(self, parent, import_func, menu_instance):
        super().__init__(master=parent, fg_color='transparent')
        self.import_func = import_func
        self.menu_instance = menu_instance
        self.file_labels = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def update_files(self, files):
        for label in self.file_labels:
            label.destroy()

        self.file_labels = []
        
        y_margin = 0.4
        for file in files:
            reversed_filepath = file[::-1]
            sliced_index = reversed_filepath.find("/")
            file_string = reversed_filepath[:sliced_index]
            label = ctk.CTkLabel(master = self, text = file_string[::-1])
            
            label.place(relx = 0.25, rely = y_margin, anchor = "w")
            y_margin += 0.04
            self.file_labels.append(label)

class DistanceFrame(ctk.CTkFrame):
    def __init__(self, parent, files, replace_frame_func):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(row=0, column=0, sticky="nsew")
        self.files = files
        self.replace_frame_func = replace_frame_func

        self.service = GuiServices(self)
        f = FileHandler(list(files), self)
        sensors = f.count_sensors()

        for index in range(sensors):
            EntryPanel(self, index).grid(row=index, column=0, sticky="ew", padx=10, pady=5)

        ctk.CTkButton(self, text='Calculate', command=self.send_data).grid(row=sensors, column=0, pady=10, padx=10, sticky="ew")

        self.grid_columnconfigure(0, weight=1)
        for i in range(sensors + 1):
            self.grid_rowconfigure(i, weight=1)

    def send_data(self):
        print('calculate')
        # Example image data (replace with your actual data)
        image_data = [
            ('src/front/resource/X_axis_graph.png', 'Eje X'),
            ('src/front/resource/Y_axis_graph.png', 'Eje Y'),
            ('src/front/resource/Z_axis_graph.png', 'Eje Z'),
        ]
        self.replace_frame_func(image_data)

class CalculateFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(row=0, column=0, sticky="nsew")

class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(row=0, column=0, sticky="nsew")