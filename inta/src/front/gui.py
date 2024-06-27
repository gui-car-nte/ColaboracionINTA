import tkinter as tk

from src.front.tkinter_settings import GuiServices, COLOR_PRIMARY, COLOR_SECUNDARY

# def start_gui():

#     root = tk.Tk()
#     root.title("Cálculo del Momento Magnético")
#     root.minsize(600,400)
#     root.configure(background=COLOR_PRIMARY,)
    
#     settings = GuiServices(root)

#     top_frame = settings.create_frame(root, tk.TOP)
#     center_frame = settings.create_frame(root, tk.TOP, True)
#     bottom_frame = settings.create_frame(root, tk.BOTTOM)

#     settings.create_button("csv_button", top_frame, "Cargar Archivos CSV", tk.LEFT, settings.load_files, center_frame)
#     settings.create_button("export_button", top_frame, "Exportar a PDF", tk.LEFT, '','')

#     root.mainloop()

import tkinter as tk

from src.front.tkinter_settings import GuiServices, COLOR_PRIMARY, COLOR_SECUNDARY

def start_gui():
    root = tk.Tk()
    root.title("Cálculo del Momento Magnético")
    root.minsize(600, 400)
    root.configure(background=COLOR_PRIMARY)
    
    settings = GuiServices(root)

    top_frame = settings.create_frame(root, tk.TOP)
    center_frame = settings.create_frame(root, tk.TOP, complete=True, scrollable=True)
    settings.create_image_canvas(center_frame,'src/front/resource/logo.png').configure(background=COLOR_PRIMARY)
    bottom_frame = settings.create_frame(root, tk.BOTTOM)

    settings.create_button("csv_button", top_frame, "Cargar Archivos CSV", tk.LEFT, settings.load_files, center_frame)
    settings.create_button("export_button", top_frame, "Exportar a PDF", tk.LEFT, '', '')

    root.mainloop()
