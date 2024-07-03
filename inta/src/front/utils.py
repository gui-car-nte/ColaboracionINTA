import tkinter as tk
import re

from src import config
from PIL import Image, ImageTk


class Utils():
    def __init__(self, windows) -> None:
        self.root = windows

    def create_frame(self, frame_in, side_in, complete = False, scrollable = False):
        frame = tk.Frame(frame_in)
        frame.configure(background = config.PRIMARY_COLOR)

        if complete:
            frame.pack(side = side_in, fill =  tk.BOTH, expand = True, pady = 10)
        else:
            frame.pack(side = side_in, pady = 10)

        if scrollable:
            frame = self.create_scroll(frame)
            
        return frame

    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion = canvas.bbox("all"))

    def _on_mouse_wheel(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_button(
        self, name_in, frame_in, text_in, side_in, command_in, parameter_in
    ):
        if parameter_in != "":
            button = tk.Button(
                frame_in,
                text = text_in,
                background = config.SECONDARY_COLOR,
                name = name_in,
                command = lambda: command_in(parameter_in),
            )
            button.configure(fg="white")
            if side_in == "":
                button.pack(pady = 10, anchor = tk.NW)
            else:
                button.pack(side=side_in, pady = 10, anchor = tk.NW)
        else:
            button = tk.Button(
                frame_in,
                text = text_in,
                background = config.SECONDARY_COLOR,
                name = name_in,
                command = command_in,
            )
            button.configure(fg="white")
            if side_in == "":
                button.pack(pady = 10)
            else:
                button.pack(side = side_in, pady = 10)

        return button

    def create_label(self, frame_in, text_in, side_in, diff = False):
        if diff:
            result_label = tk.Label(
                frame_in, text = text_in, wraplength = 300, justify = side_in
            )
            result_label.pack(pady=20)
        else:
            label = tk.Label(frame_in, text = text_in)
            label.configure(background = config.PRIMARY_COLOR)
            if side_in == "":
                label.pack()
            else:
                label.pack(side = side_in)
                
        return label

    def create_input(self, frame_in):
        # Aqui tendremos que llamar a la clase de check y poner la funcion en ella
        vcmd = (frame_in.register(self._validate_numeric), '%P')

        entry = tk.Entry(frame_in, validate="key", validatecommand=vcmd)
        entry.pack()

    def create_image_canvas(self, frame, image_path = ""):
        if image_path == "":
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)

            canvas = tk.Canvas(frame, width = image.width, height = image.height)
            canvas.pack(pady = 10)
            canvas.create_image(0, 0, anchor = "center", image = photo, tags='img')

            # Keep a reference to the image to prevent garbage collection # TODO research garbage collector
            canvas.image = photo # type: ignore
      
        else:
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)

            canvas = tk.Canvas(frame, width = image.width, height = image.height)
            canvas.pack(pady = 10)
            canvas.create_image(0, 0, anchor = "nw", image = photo)

            # Keep a reference to the image to prevent garbage collection # TODO research garbage collector
            canvas.image = photo # type: ignore
            
        return canvas

    # TODO could be moved to utils folder or another file to shorten code, go case by case
    # TODO '=' spacing
    def create_scroll(self, frame_main):
        canvas = tk.Canvas(frame_main, bg = config.PRIMARY_COLOR)
        canvas.pack(side=tk.LEFT, fill = tk.BOTH, expand = True)

        scrollbar_y = tk.Scrollbar(frame_main, orient = tk.VERTICAL, command = canvas.yview)
        scrollbar_y.pack(side = tk.RIGHT, fill = tk.Y)
        canvas.configure(yscrollcommand = scrollbar_y.set)

        inner_frame = tk.Frame(canvas, bg = config.PRIMARY_COLOR)
        window = canvas.create_window((0, 0), window = inner_frame, anchor = "n")

        def center_frame(event):
            canvas_width = event.width
            canvas.coords(window, canvas_width // 2, 0)
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", center_frame)
        inner_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.bind_all(
            "<MouseWheel>", lambda event: self._on_mouse_wheel(event, canvas)
        )

        return inner_frame
  
    def _validate_numeric(self, new_value):
        if new_value == "":
            return True  # Permitir eliminar el contenido
        try:
            float(new_value)  # Intentar convertir el valor a float
            return True  # Permitir el nuevo valor si es numérico
        except ValueError:
            return False  # Rechazar el nuevo valor si no es numérico