import customtkinter as ctk
from src.front.gui_service import GuiServices
from src.front.panels import EntryPanel
from src.front.settings import IMAGES


class LeftFrame(ctk.CTkFrame):
    def __init__(self, parent, replace_frame_func):
        super().__init__(master=parent, width=100)
        self.grid(row=0, column=0, sticky="nsew")

        self.service = GuiServices(self)
        self.replace_frame_func = replace_frame_func

        self.tabview = ctk.CTkTabview(self, width=100)
        self.tabview.add("Files")
        self.files_frame = FilesFrame(self.tabview.tab("Files"), self)

        # Lista para almacenar los nombres de los archivos cargados
        self.files = {}

        self.enable_file_selection_button()


    def enable_file_selection_button(self):
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
            height=40,  # Set a fixed height
        )
        self.select_files_button.grid(row=0, column=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def import_files(self):
        self.files = self.service.load_files()

        if self.files:
            self.files_frame.update_files(self.files)
            self.show_all_tabs()
        else:
            print(
                "No files selected or failed to load files"
            )  # TODO replace with error call

    def show_all_tabs(self):
        self.button_container.destroy()

        self.tabview.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview.add("Distances")
        self.tabview.add("Calculations")
        self.tabview.add("Export")

        self.files_frame.grid(row=0, column=0, sticky="nsew")
        self.tabview.tab("Files").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Files").grid_rowconfigure(0, weight=1)

        calculate_frame_instance = CalculateFrame(self.tabview.tab("Calculations"), self.service)
        DistanceFrame(self.tabview.tab("Distances"), self.files, self.service.sensor_number, self.replace_frame_func, self.service, calculate_frame_instance)
        ExportFrame(self.tabview.tab("Export"))

        self.tabview.set("Distances")


class FilesFrame(ctk.CTkFrame):
    def __init__(self, parent, menu_instance):
        super().__init__(master=parent, fg_color="transparent")
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
            label = ctk.CTkLabel(master=self, text=file)

            label.place(relx=0.25, rely=y_margin, anchor="w")
            y_margin += 0.04
            self.file_labels.append(label)
            


class DistanceFrame(ctk.CTkFrame):
    def __init__(self, parent, files, sensor_number, replace_frame_func, service, calculate_frame):
        super().__init__(master=parent, fg_color="transparent")
        self.pack( fill = 'x')
        self.files = files
        self.replace_frame_func = replace_frame_func
        self.service = service
        self.calculate_frame = calculate_frame

        for index in range(self.service.sensor_number):
            EntryPanel(self, index).grid(
                row=index, column=0, sticky="ew", padx=2, pady=4
            )

        ctk.CTkButton(self, text="Calculate", command=self.send_data).grid(
            row=service.sensor_number, column=0, pady=10, padx=10, sticky="ew"
        )

        self.grid_columnconfigure(0, weight=1)
        for i in range(service.sensor_number):
            self.grid_rowconfigure(i, weight=1)

    def send_data(self):
        distances_list = self.service.get_values(self)
        final_calculation = self.service.create_result(distances_list)
        
        image_data = []
        for i in range(len(final_calculation)):
            if i < len(IMAGES):
                image_data.append((
                    str(IMAGES[i]), 
                    str(f'Magnetic moment (mAm^2): {final_calculation[i]} (J/T)')
                ))
        
        self.replace_frame_func(image_data)
        
        self.calculate_frame.update_calculation_details()


class CalculateFrame(ctk.CTkFrame):
    def __init__(self, parent, service):
        super().__init__(master = parent, fg_color = 'transparent')
        #self.grid(row = 0, column = 0, sticky = "nsew") # TODO: Alberto
        self.pack(expand = True, fill = "both") 
        self.service = service

        # self.scrollable_frame = ctk.CTkScrollableFrame(self, width = 400, height = 1200)
        # self.scrollable_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "nsew") # TODO: Alberto
        # self.scrollable_frame.pack(expand = True, fill = "x") 

        self.text_widget = ctk.CTkTextbox(self, wrap = 'word')
        #self.text_widget.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "nsew") # TODO: Alberto
        self.text_widget.pack(expand = True, fill = "both") 

    def update_calculation_details(self):
        details = self.service.obtain_calculation_details()
        self.text_widget.delete("1.0", "end")  
        self.text_widget.insert("1.0", details)


class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(row=0, column=0, sticky="nsew")
