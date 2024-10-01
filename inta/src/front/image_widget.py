import customtkinter as ctk
from tkinter import filedialog, Canvas
from src.front.settings import BACKGROUND_COLOR
from PIL import Image, ImageTk
from typing import List, Tuple
from src.front.gui_service import GuiServices


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        super().__init__(master = parent)
        self.grid(column = 0, columnspan = 2, row = 0, sticky = "ns")
        self.import_func = import_func

        ctk.CTkButton(self, text = "select files", command = self.open_dialog).pack(
            expand = True
        )

    def open_dialog(self):
        path = filedialog.askopenfile()
        self.import_func(path)


class InitialFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = BACKGROUND_COLOR)
        self.grid(column = 1, columnspan = 2, row = 0, sticky = "nsew")

        self.service = GuiServices(self)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)

        # Create image for canvas
        self.canvas = Canvas(self, bg = BACKGROUND_COLOR, bd = 0, highlightthickness = 0)
        self.canvas.place(relx = 0.5, rely = 0.45, anchor = "center")

        # Load image
        image_path = self.service.resource_path("resource\\inta_logo.png")
        image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(image)

        # show image
        self.canvas.create_image(0, 0, anchor = "nw", image = self.photo)
        self.canvas.config(width = image.width, height = image.height)

        self.label = ctk.CTkLabel(
            self, text = "Magnetic Moment Calculation", font = ("Calibri", 40, "bold"), fg_color='transparent'
        )
        self.label.place(relx = 0.5, rely = 0.65, anchor = "center")


class ResultFrame(ctk.CTkFrame):
    def __init__(self, parent, image_data: List[Tuple[str, str]]):
        super().__init__(master = parent)
        self.grid(column = 1, rowspan = 2)
        self.image_data = image_data
        self.current_index = 0
        self.service = GuiServices(self)

        self.create_widgets()

    def create_widgets(self):
        # Image label (using CTkLabel instead of Canvas)
        self.image_label = ctk.CTkLabel(self, text = "", image = None)
        self.image_label.grid(
            row = 0, column = 0, columnspan = 3, pady = (20, 10), sticky = "nsew"
        )

        # Description label
        self.desc_label = ctk.CTkLabel(self, text = "", font = ("Helvetica", 14))
        self.desc_label.grid(row = 1, column = 0, columnspan = 3, pady = (0, 20))

        # Navigation buttons

        # Left
        # Cargar y ajustar la imagen
        image_path1 = self.service.resource_path("resource\\arrow_pointing_left.png")
        image1 = Image.open(image_path1)
        image1 = image1.resize((500, 500))
        photo1 = ctk.CTkImage(image1)

        self.prev_button = ctk.CTkButton(
            self, text = "", command = self.prev_image, width = 40, image = photo1
        )
        # self.prev_button.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "w")
        self.prev_button.grid_remove()

        # Right

        image_path2 = self.service.resource_path("resource\\arrow_pointing_right.png")
        image2 = Image.open(image_path2)
        image2 = image2.resize((5000, 5000))
        photo2 = ctk.CTkImage(image2)

        self.next_button = ctk.CTkButton(
            self, text = "", command = self.next_image, width = 40, image = photo2
        )
        self.next_button.grid(row = 2, column = 2, padx = 10, pady = 10, sticky = "e")

        # Configure grid
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.update_image()

    def update_image(self):
        image_path, label_text = self.image_data[self.current_index]
        
        # Asegurarnos de que la ruta sea correcta y el archivo exista
        image = Image.open(self.service.resource_path(image_path))

        # Set minimum dimensions for the image
        MIN_WIDTH, MIN_HEIGHT = 650, 480

        # Obtener el tamaño actual del widget para redimensionar correctamente
        current_width = self.winfo_width()
        current_height = self.winfo_height()

        # Calculate max_size ensuring positive values and minimum dimensions
        max_width = max(MIN_WIDTH, current_width - 40)  # Resta márgenes
        max_height = max(MIN_HEIGHT, current_height - 100)  # Resta márgenes
        max_size = (max_width, max_height)

        # Redimensionar la imagen para ajustarse al frame, manteniendo el aspecto
        image.thumbnail(max_size, Image.LANCZOS) # type: ignore

        # Convertir la imagen a un CTkImage
        ctk_image = ctk.CTkImage(
            light_image=image, dark_image=image, size=(image.width, image.height)
        )

        # Actualizar la imagen y la etiqueta descriptiva
        self.image_label.configure(image=ctk_image)
        self.desc_label.configure(text=label_text)

        # Comprobar el estado de los botones
        if self.current_index > 0:
            self.prev_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        else:
            self.prev_button.grid_remove()

        if self.current_index < len(self.image_data) - 1:
            self.next_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")
        else:
            self.next_button.grid_remove()

        # Asegurar que el layout se refresque correctamente
        self.update_idletasks()

    def next_image(self):
        if self.current_index < len(self.image_data) - 1:
            self.current_index += 1
            self.update_image()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_image()

    def on_resize(self, event):
        self.update_image()