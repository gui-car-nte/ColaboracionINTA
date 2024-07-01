import tkinter as tk

from src.front.tkinter_settings import GuiServices
from src import config

def start_gui():
    root = tk.Tk()
    root.title("Cálculo del Momento Magnético")
    root.minsize(600, 400)
    photo = tk.PhotoImage(file = 'src/front/resource/logo.png')
    root.wm_iconphoto(False, photo)
    # root.iconbitmap('src/front/resource/logo.ico')
    root.configure(background=config.PRIMARY_COLOR)
    
    settings = GuiServices(root)

    top_frame = settings.create_frame(root, tk.TOP)
    center_frame = settings.create_frame(root, tk.TOP, complete=True, scrollable=True)
    settings.create_image_canvas(center_frame,'src/front/resource/logo.png').configure(background=config.PRIMARY_COLOR)
    bottom_frame = settings.create_frame(root, tk.BOTTOM)

    settings.create_button("csv_button", top_frame, "Cargar Archivos CSV", tk.LEFT, settings.load_files, center_frame)
    settings.create_button("export_button", top_frame, "Exportar a PDF", tk.LEFT, settings.export_to_pdf, '')

    root.mainloop()
