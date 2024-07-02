import tkinter as tk
import logging

# TODO review non-used variables
# TODO english translation
from src import config
from src.front.tkinter_settings import GuiServices
from src.front.utils import Utils

def start_gui():

    utils = Utils()

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
    root.configure(background = config.PRIMARY_COLOR)

    settings = GuiServices(root)

    top_frame = utils.create_frame(root, tk.TOP)
    center_frame = utils.create_frame(root, tk.TOP, complete=True, scrollable=True)
    utils.create_image_canvas(center_frame, "src/front/resource/logo.png").configure(
        background=config.PRIMARY_COLOR
    )
    bottom_frame = utils.create_frame(root, tk.BOTTOM)

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
    )

    root.mainloop()
