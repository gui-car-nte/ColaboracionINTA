import customtkinter as ctk
from src.front.image_widget import InitialFrame, ResultFrame
from src.front.menu import LeftFrame

class GuiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Main window configuration
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Magnetic Moment Calculation')
        self.minsize(800, 500)
        self.iconbitmap('src/front/resource/inta_icon.ico')

        # Main layout configuration
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1, uniform = 'a')
        self.columnconfigure(1, weight = 4, uniform = 'a')

        self.frame_col1 = InitialFrame(self)

        self.menu = LeftFrame(self, self.replace_frame_col1)
        self.menu.grid(row = 0, column = 0, rowspan = 2, sticky = 'nswe')

        self.mainloop()


    def close_edit(self):
        self.destroy()


    def replace_frame_col1(self, image_path):
        if hasattr(self, 'frame_col1'):
            self.frame_col1.destroy()

        # Create and place the new ScrollFrame
        self.frame_col1 = ResultFrame(self, image_path)
        self.frame_col1.grid(column = 1, row = 0, rowspan = 2, sticky = 'nsew')