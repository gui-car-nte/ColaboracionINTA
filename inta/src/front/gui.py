import customtkinter as ctk
from PIL import Image, ImageTk
from inta.src.front.image_widget import InitialFrame, ResultFrame
from inta.src.front.menu import Menu
from tkinter import Canvas
from inta.src.front.settings import *

class GuiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configuración de la ventana
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Magnetic Moment Calculation')
        self.minsize(800, 500)
        self.iconbitmap('src/front/resource/inta_icon.ico')

        # Configuración del layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=3, uniform='a')

        self.frame_col1 = InitialFrame(self)

        # Crear los widgets
        self.menu = Menu(self, self.replace_frame_col1)
        self.menu.grid(row=0, column=0, rowspan=2, sticky='nswe')

        self.mainloop()

    def close_edit(self):
        self.destroy()

    def replace_frame_col1(self, image_path):
        # Destroy the existing frame_col1
        if hasattr(self, 'frame_col1'):
            self.frame_col1.destroy()

        # Create and place the new ScrollFrame
        self.frame_col1 = ResultFrame(self, image_path)
        self.frame_col1.grid(column=1, row=0, rowspan=2, sticky='nsew')