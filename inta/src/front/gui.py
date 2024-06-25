import tkinter as tk

from src.front.tkinter_settings import GuiServices, COLOR_PRIMARY, COLOR_SECUNDARY

def delete_frame(old_frame: tk.Frame):
    old_frame.pack_forget()
    old_frame.destroy()

def start_gui():

    root = tk.Tk()
    root.title("Cálculo del Momento Magnético")
    root.minsize(600,400)
    root.configure(background=COLOR_PRIMARY,)
    
    settings = GuiServices(root)

    top_frame = settings.create_frame(root, tk.TOP, False)

    center_frame = settings.create_frame( root, tk.TOP, True)

    bottom_frame = settings.create_frame(root, tk.BOTTOM, True)

    settings.create_button("csv_button", top_frame, "Cargar Archivos CSV", tk.LEFT, settings.load_files, center_frame)
    # button1 = tk.Button(top_frame, text="Cargar Archivos CSV",
    #                      command=lambda: settings.load_files(center_frame), background=COLOR_SECUNDARY)
    # button1.pack(side=tk.LEFT, padx=10)
    # settings.create_button("export_button", top_frame, "Exportar a PDF", tk.LEFT, '','')

    root.mainloop()