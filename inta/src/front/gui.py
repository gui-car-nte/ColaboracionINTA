import os
import customtkinter as ctk
from src.front.image_widget import InitialFrame, ResultFrame
from src.front.menu import LeftFrame
import pyautogui
from src.front.gui_service import GuiServices
from src.front.settings import CLOSE_RED


class GuiApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.services = GuiServices(self)

        print(f'Ruta: {os.path.dirname(__file__)}')

        ctk.set_appearance_mode("dark")
        self.geometry("1000x600")
        self.title("Magnetic Moment Calculation")
        self.minsize(800, 500)
        icon_path = self.services.resource_path("resource\\inta_icon.ico")
        self.iconbitmap(icon_path)
        self.update()
        self.lift()
        self.attributes("-topmost", True)
        self.after_idle(self.attributes, "-topmost", False)
        pyautogui.hotkey("winleft", "up")

        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.columnconfigure(0, weight = 1, uniform = "a")
        self.columnconfigure(1, weight = 4, uniform = "a")

        self.init_app_state()

        self.mainloop()

    def init_app_state(self):
        self.frame_col1 = InitialFrame(self)
        self.frame_col1.grid(row = 0, column = 1, rowspan = 3, sticky = "nswe")

        self.menu = LeftFrame(self, self.replace_frame_col1, self.services)
        self.menu.grid(row = 0, column = 0, rowspan = 3, sticky = "nswe")


        self.reset_button = ctk.CTkButton(
            self, text = "Reset", command = self.reset_app, width = 120, height = 40, hover_color = CLOSE_RED
        )

        self.export_pdf_button = ctk.CTkButton(
            self, text = "Export PDF", command = self.services.export_to_pdf, width = 120, height = 40
        )
        self.reset_button.grid_remove()
        self.export_pdf_button.grid_remove()

    def reset_app(self):
        self.init_app_state()

    def replace_frame_col1(self, image_path):

        self.reset_button.grid(row = 0, column = 1, pady = 10, sticky = "ne")
        self.export_pdf_button.grid(row = 0, column = 1, pady = 10, sticky = "ne", padx = (0,130))

        if self.frame_col1 is not None:
            self.frame_col1.destroy()
        self.frame_col1 = ResultFrame(self, image_path)
        self.frame_col1.grid(row = 1, column = 1, rowspan = 3, sticky = "nswe")
