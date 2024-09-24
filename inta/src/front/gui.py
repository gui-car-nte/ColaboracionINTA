import customtkinter as ctk
from src.front.image_widget import InitialFrame, ResultFrame
from src.front.menu import LeftFrame
import pyautogui


class GuiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Main window configuration
        ctk.set_appearance_mode("dark")
        self.geometry("1000x600")
        self.title("Magnetic Moment Calculation")
        self.minsize(800, 500)
        self.iconbitmap("src/front/resource/inta_icon.ico")
        self.update()
        self.lift()
        self.attributes("-topmost", True)
        self.after_idle(self.attributes, "-topmost", False)
        pyautogui.hotkey("winleft", "up")

        # Configuración del layout principal
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=4, uniform="a")

        # Configurar el estado inicial de la aplicación
        self.init_app_state()

        self.mainloop()

    def init_app_state(self):
        # Inicializa el frame inicial en la columna 0 y 1
        self.frame_col1 = InitialFrame(self)
        self.frame_col1.grid(row=0, column=1, rowspan=3, sticky="nswe")

        self.menu = LeftFrame(self, self.replace_frame_col1)
        self.menu.grid(row=0, column=0, rowspan=3, sticky="nswe")

        # Botón de reinicio
        self.reset_button = ctk.CTkButton(
            self, text="Reset", command=self.reset_app
        )
        self.reset_button.grid(row=0, column=1, pady=10, sticky="ne")

    def reset_app(self):
        # Destruir frames actuales solo si existen
        # if self.menu is not None:
        #     self.menu.destroy()
        # if self.frame_col1 is not None:
        #     self.frame_col1.destroy()

        # Restaurar el estado inicial de la aplicación
        self.init_app_state()

    def replace_frame_col1(self, image_path):
        if self.frame_col1 is not None:
            self.frame_col1.destroy()
        self.frame_col1 = ResultFrame(self, image_path)
        self.frame_col1.grid(row=1, column=1, rowspan=3, sticky="nswe")
