import customtkinter as ctk
from tkinter import filedialog, Canvas
from inta.src.front.settings import *
from PIL import Image, ImageTk

class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column=0, columnspan=2, row=0, sticky='ns')
        self.import_func = import_func

        ctk.CTkButton(self, text='select files', command=self.open_dialog).pack(expand=True)

    def open_dialog(self):
        path = filedialog.askopenfile()
        self.import_func(path)

class InitialFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.grid(column=1, columnspan=2, row=0, sticky='nsew')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.configure(fg_color=BACKCGROUND_COLOR)

        # Crear canvas para la imagen
        self.canvas = Canvas(self, bg=BACKCGROUND_COLOR, bd=0, highlightthickness=0)
        self.canvas.grid(row=1, column=1, sticky='s')
        # Cargar la imagen
        image = Image.open('src/front/resource/logo.png')
        self.photo = ImageTk.PhotoImage(image)

        # Mostrar la imagen en el canvas
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.config(width=image.width,
                           height=image.height)

        self.label = ctk.CTkLabel(self, text='\nMagnetic Moment Calculation', font=('Calibri', 40, 'bold'))
        self.label.grid(row=2, column=1, sticky='n')

class ScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, image_path):
        super().__init__(master=parent)
        self.grid(row=0, column=1, sticky='nsew')
        self.add_canvas(image_path)

    def add_canvas(self, image_path):
        ImageOutput(self, image_path)

class ImageOutput(Canvas):
    def __init__(self, parent, path_image):
        super().__init__(master=parent, background=BACKCGROUND_COLOR, bd=0, highlightthickness=0, relief='ridge')
        self.display_image(path_image)
        self.grid(row=0, column=0, sticky='nsew')

    def display_image(self, path_image):
        # Cargar la imagen usando PIL
        image = Image.open(path_image)
        self.photo = ImageTk.PhotoImage(image)
        self.create_image(0, 0, anchor='nw', image=self.photo)
        self.config(width=image.width, height=image.height)

class CloseOutput(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(
            master=parent,
            command=close_func,
            text='X',
            text_color=WHITE,
            fg_color='transparent',
            width=40, height=40,
            corner_radius=0,
            hover_color=CLOSE_RED
        )
        self.place(relx=0.99, rely=0.01, anchor='ne')