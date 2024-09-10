import customtkinter as ctk
from PIL import Image, ImageTk
from inta.src.front.image_widget import ImageImport, ImageOutput, CloseOutput
from inta.src.front.menu import Menu
from tkinter import filedialog
from inta.src.back.file_handler import FileHandler
from inta.src.front import gui_service

class GUI_APP(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configuración de la ventana
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('INTA')
        self.minsize(800, 500)

        # Configuración del layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1, uniform='a')  # Columna izquierda
        self.columnconfigure(1, weight=3, uniform='a')  # Columna derecha

        # Crear los widgets
        # self.menu = ImageImport(self, self.import_image)
        self.menu = Menu(self)
        self.menu.grid(row=0, column=0, sticky='nswe')

        self.image_output = ImageOutput(self, self.resize_image)
        self.image_output.grid(row=0, column=1, sticky='nswe')

        # self.close_button = CloseOutput(self, self.close_edit)

        # Cargar una imagen por defecto en el lado derecho
        self.default_image_path = 'src/front/resource/logo.png'
        self.image = Image.open(self.default_image_path)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_output.create_image(0, 0, anchor='ne', image=self.image_tk)

        self.mainloop()

    def resize_image(self, event):
        # Ajustar el tamaño de la imagen cuando cambie el tamaño de la ventana
        canvas_ratio = event.width / event.height
        image_ratio = self.image.size[0] / self.image.size[1]

        if canvas_ratio > image_ratio:
            new_height = event.height
            new_width = int(new_height * image_ratio)
        else:
            new_width = event.width
            new_height = int(new_width / image_ratio)

        resized_image = self.image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(0, 0, anchor='nw', image=self.image_tk)

    def close_edit(self):
        self.destroy()
