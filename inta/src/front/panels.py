import customtkinter as ctk
from src.front.settings import *

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = BACKCGROUND_COLOR)
        self.grid(sticky="ew", padx=4, pady=4)
        self.grid_columnconfigure(0, weight=1)

class EntryPanel(Panel):
    def __init__(self, parent, index):
        super().__init__(parent = parent)
        self.index = index
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text=f"Sensor {self.index + 1}").grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkEntry(self, placeholder_text=f"Distance for Sensor {self.index + 1}").grid(row=0, column=1, sticky="ew", padx=5)
        self.grid_columnconfigure(1, weight=1)

class SliderPanel(Panel):
    def __init__(self, parent, text, data_var, min_value, max_value):
        super().__init__(parent = parent)
        self.data_var = data_var
        self.create_widgets(text, min_value, max_value)

    def create_widgets(self, text, min_value, max_value):
        ctk.CTkLabel(self, text = text).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkSlider(self, from_ = min_value, to = max_value, variable = self.data_var).grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkEntry(self, textvariable = self.data_var, width = 50).grid(row=0, column=2, padx=5)
        self.grid_columnconfigure(1, weight=1)

class SegmentedPanel(Panel):
    def __init__(self, parent, text, data_var, options):
        super().__init__(parent = parent)
        self.data_var = data_var
        self.create_widgets(text, options)

    def create_widgets(self, text, options):
        ctk.CTkLabel(self, text = text).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkSegmentedButton(self, variable = self.data_var, values = options).grid(row=0, column=1, sticky="ew", padx=5)
        self.grid_columnconfigure(1, weight=1)

class SwitchPanel(Panel):
    def __init__(self, parent, text, data_var):
        super().__init__(parent = parent)
        self.data_var = data_var
        self.create_widgets(text)

    def create_widgets(self, text):
        ctk.CTkLabel(self, text = text).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkSwitch(self, text = '', variable = self.data_var).grid(row=0, column=1, sticky="e", padx=5)
        self.grid_columnconfigure(1, weight=1)