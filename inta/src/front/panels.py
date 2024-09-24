import customtkinter as ctk
from src.front.settings import BACKGROUND_COLOR

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = BACKGROUND_COLOR) #, fg_color = 'BACKCGROUND_COLOR'
        self.grid(sticky = "ew", padx = 4, pady = 20, column = 0,)
        self.grid_rowconfigure(0, minsize = 50)  # Aumentar la altura de la fila
        # self.grid_columnconfigure(0, weight = 1)

class EntryPanel(Panel):
    def __init__(self, parent, number_of_entries, calculation_button):
        super().__init__(parent = parent)
        self.number_of_entries = number_of_entries
        self.entries = []
        self.create_widgets()
        self.calculation_button = calculation_button


    def create_widgets(self):
        for index in range(self.number_of_entries):
            ctk.CTkLabel(self, text=f"Sensor {index + 1}").grid(row=index, column=0, sticky="w", padx=5)
            
            input_entry = ctk.CTkEntry(self, placeholder_text=f"Distance for sensor {index + 1}", validate = 'key', validatecommand = (self.register(self.verify_key_pressed_is_valid), '%P'))
            input_entry.bind("<KeyRelease>", self.verify_form_is_valid)
            input_entry.grid(row=index, column=1, sticky="ew", padx=5)
            
            self.entries.append(input_entry)  # Añadir la entrada a la lista

        self.grid_columnconfigure(1, weight=1)

    def verify_key_pressed_is_valid(self, new_value):
        # Permitir solo números, un solo punto decimal o vacío
        if new_value == "" or new_value.replace(".", "", 1).isdigit():
            return True
        return False

    def verify_form_is_valid(self, event):
        if all(entrada.get().strip() for entrada in self.entries):
            print("Form is valid")
            self.calculation_button.configure(state="enabled")
            # self.boton
        else:
            print("Form is not valid")
            self.calculation_button.configure(state="disabled")


class SliderPanel(Panel):
    def __init__(self, parent, text, data_var, min_value, max_value):
        super().__init__(parent = parent)
        self.data_var = data_var
        self.create_widgets(text, min_value, max_value)


    def create_widgets(self, text, min_value, max_value):
        ctk.CTkLabel(self, text = text).grid(row = 0, column = 0, sticky = "w", padx = 5)
        ctk.CTkSlider(self, from_ = min_value, to = max_value, variable = self.data_var).grid(row = 0, column = 1, sticky = "ew", padx = 5)
        ctk.CTkEntry(self, textvariable = self.data_var, width = 50).grid(row = 0, column = 2, padx = 5)
        self.grid_columnconfigure(1, weight = 1)


class SegmentedPanel(Panel):
    def __init__(self, parent, text, data_var, options):
        super().__init__(parent = parent)
        self.data_var = data_var
        self.create_widgets(text, options)


    def create_widgets(self, text, options):
        ctk.CTkLabel(self, text = text).grid(row = 0, column = 0, sticky = "w", padx = 5)
        ctk.CTkSegmentedButton(self, variable = self.data_var, values = options).grid(row = 0, column = 1, sticky = "ew", padx = 5)
        self.grid_columnconfigure(1, weight = 1)


class SwitchPanel(Panel):
    def __init__(self, parent, text, data_var):
        super().__init__(parent = parent)
        self.data_var = data_var
        self.create_widgets(text)


    def create_widgets(self, text):
        ctk.CTkLabel(self, text = text).grid(row = 0, column = 0, sticky = "w", padx = 5)
        ctk.CTkSwitch(self, text = '', variable = self.data_var).grid(row = 0, column = 1, sticky = "e", padx = 5)
        self.grid_columnconfigure(1, weight = 1)