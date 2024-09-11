import customtkinter as ctk
from PIL import Image, ImageTk
from inta.src.front.image_widget import ScrollFrame
from inta.src.front.menu import Menu
from tkinter import Canvas
from inta.src.front.settings import *
from inta.src.front import gui_service


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
        self.columnconfigure(0, weight=1, uniform='a')  # Columna izquierda
        self.columnconfigure(1, weight=3, uniform='a')  # Columna derecha

        # Crear los widgets
        self.menu = Menu(self)
        self.menu.grid(row=0, column=0, rowspan = 2, sticky='nswe')

        # Crear el ScrollFrame con la imagen inicial
        # self.image_output = ScrollFrame(self, 'src/front/resource/logo.png')
        # self.image_output.grid(row=0, column=1, sticky='nswe')

        self.add_initial_image('src/front/resource/logo.png')

        self.mainloop()

    def add_initial_image(self, image_path):
        """Muestra la imagen inicial con su tamaño por defecto"""
        # self.clear_images()  # Limpiar cualquier imagen existente

        # Crear canvas para la imagen
        self.canvas = Canvas(self, bg=BACKCGROUND_COLOR, bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=1, sticky='s')

        # Cargar la imagen
        image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(image)  # Usar ImageTk.PhotoImage

        # Mostrar la imagen en el canvas
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.config(width=image.width,
                           height=image.height)

        self.label = ctk.CTkLabel(self, text = '\nMagnetic Moment Calculation', font = ('Calibri', 40, 'bold'))
        self.label.grid(row = 1, column = 1, sticky = 'n')

    def close_edit(self):
        self.destroy()
