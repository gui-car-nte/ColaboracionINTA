import tkinter as tk
import logging

# TODO review non-used variables
# TODO english translation
from src import config
from src.front.gui_service import GuiServices
from src.front.utils import Utils

def start_gui():

    # Configure the logger at the start of your application
    logging.basicConfig(
        filename='error_log.txt',
        filemode='a',
        format='%(asctime)s,%(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.ERROR
    )

    logger = logging.getLogger('urbanGUI')

    root = tk.Tk()
    root.title("Cálculo del Momento Magnético")
    root.minsize(600, 400)
    icon = tk.PhotoImage(file='src/front/resource/logo.png')
    root.iconphoto(True, icon)
    root.configure(background = config.PRIMARY_COLOR)

    utils = Utils(root)

    top_frame = utils.create_frame(root, tk.TOP)
    center_frame = utils.create_frame(root, tk.TOP, complete=True, scrollable=True)
    utils.create_image_canvas(center_frame, "src/front/resource/logo.png").configure(
        background=config.PRIMARY_COLOR
    )
    bottom_frame = utils.create_frame(root, tk.BOTTOM)
    message_label = utils.create_label(bottom_frame, "", tk.TOP)
    
    settings = GuiServices(root)

    utils.create_button(
        "csv_button",
        top_frame,
        "Upload CSV files",
        tk.LEFT,
        settings.load_files,
        center_frame,
    )
    utils.create_button(
        "export_button",
        top_frame,
        "Export to PDF",
        tk.LEFT,
        settings.export_to_pdf,
        "",
    ).config(state=tk.DISABLED)

    root.mainloop()
