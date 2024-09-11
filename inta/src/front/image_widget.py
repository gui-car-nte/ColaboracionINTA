import customtkinter as ctk
from tkinter import filedialog, Canvas
from inta.src.front.settings import *
from PIL import Image, ImageTk

class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        super().__init__(master = parent)
        self.grid(column = 0, columnspan = 2, row = 0, sticky = 'ns')
        self.import_func = import_func

        ctk.CTkButton(self, text = 'select files', command = self.open_dialog).pack(expand = True)

    def open_dialog(self):
        path = filedialog.askopenfile()
        self.import_func(path)


class ScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, image):
        super().__init__(master=parent)
        self.grid(row=0, column=1, sticky='nsew')
        # self.resize = resize_image

        self.add_canvas(image)

    def add_canvas(self, path_image):
        ImageOutput(self)


class ImageOutput(Canvas):
    def __init__(self, parent, path_image):
        super().__init__(master = parent, background = BACKCGROUND_COLOR, bd = 0, highlightthickness = 0, relief = 'ridge')
        self.grid(row = 0, column = 1, sticky = 'nsew')
        # self.bind('<Configure>', resize_image)


class CloseOutput(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(
            master = parent,
            command = close_func,
            text = 'X',
            text_color = WHITE,
            fg_color = 'transparent',
            width = 40, height = 40,
            corner_radius = 0,
            hover_color = CLOSE_RED
        )
        self.place(relx = 0.99, rely = 0.01, anchor = 'ne')