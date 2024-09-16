import customtkinter as ctk
from tkinter import filedialog, Canvas
from src.front.settings import BACKCGROUND_COLOR, WHITE, CLOSE_RED
from PIL import Image, ImageTk
from typing import List, Tuple


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


class ResultFrame(ctk.CTkFrame):
    def __init__(self, parent, image_data: List[Tuple[str, str]]):
        super().__init__(master=parent)
        self.grid(row=0, column=1, sticky='nsew')
        self.image_data = image_data
        self.current_index = 0

        self.create_widgets()

    def create_widgets(self):
        # Image label (using CTkLabel instead of Canvas)
        self.image_label = ctk.CTkLabel(self, text="", image=None)
        self.image_label.grid(row=0, column=0, columnspan=3, pady=(20, 10), sticky='nsew')

        # Description label
        self.desc_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14))
        self.desc_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        # Navigation buttons
        self.prev_button = ctk.CTkButton(self, text="←", command=self.prev_image, width=40)
        self.prev_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.next_button = ctk.CTkButton(self, text="→", command=self.next_image, width=40)
        self.next_button.grid(row=2, column=2, padx=10, pady=10, sticky='e')

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.update_image()

    def update_image(self):
        image_path, label_text = self.image_data[self.current_index]
        image = Image.open(image_path)

        # Set minimum dimensions for the image
        MIN_WIDTH, MIN_HEIGHT = 650, 480

        # Calculate max_size ensuring positive values and minimum dimensions
        max_width = max(MIN_WIDTH, self.winfo_width() - 40)
        max_height = max(MIN_HEIGHT, self.winfo_height() - 100)
        max_size = (max_width, max_height)

        # Resize image to fit the frame while maintaining aspect ratio
        image.thumbnail(max_size, Image.LANCZOS)

        # Ensure the image is at least the minimum size
        if image.width < MIN_WIDTH or image.height < MIN_HEIGHT:
            image = image.resize((max(image.width, MIN_WIDTH), max(image.height, MIN_HEIGHT)), Image.LANCZOS)

        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(image.width, image.height))

        self.image_label.configure(image=ctk_image)
        self.desc_label.configure(text=label_text)

        # Update button states
        self.prev_button.configure(state="normal" if self.current_index > 0 else "disabled")
        self.next_button.configure(state="normal" if self.current_index < len(self.image_data) - 1 else "disabled")

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