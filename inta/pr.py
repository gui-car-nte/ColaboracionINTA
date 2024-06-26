import tkinter as tk
from PIL import Image, ImageTk

# Función para cargar y redimensionar imágenes
def cargar_y_redimensionar_imagen(ruta_imagen, ancho, alto):
    img = Image.open(ruta_imagen)
    img = img.resize((ancho, alto), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)

# Crear la ventana principal
root = tk.Tk()
root.title("Ejemplo de disposición de imágenes y etiquetas")

# Definir rutas de las imágenes locales
ruta_imagen1 = "ruta/a/tu/imagen1.jpg"
ruta_imagen2 = "ruta/a/tu/imagen2.jpg"
ruta_imagen3 = "ruta/a/tu/imagen3.jpg"

# Definir tamaño de las imágenes
ancho, alto = 100, 100

# Cargar y redimensionar las imágenes
imagen1 = cargar_y_redimensionar_imagen(ruta_imagen1, ancho, alto)
imagen2 = cargar_y_redimensionar_imagen(ruta_imagen2, ancho, alto)
imagen3 = cargar_y_redimensionar_imagen(ruta_imagen3, ancho, alto)

# Crear frames para la disposición
frame_superior = tk.Frame(root)
frame_superior.pack(pady=10)

frame_inferior = tk.Frame(root)
frame_inferior.pack(pady=10)

# Añadir primera imagen y su etiqueta al frame superior
frame_imagen1 = tk.Frame(frame_superior)
frame_imagen1.pack(side=tk.LEFT, padx=10)
label_imagen1 = tk.Label(frame_imagen1, image=imagen1)
label_imagen1.pack()
etiqueta1 = tk.Label(frame_imagen1, text="Imagen 1")
etiqueta1.pack()

# Añadir segunda imagen y su etiqueta al frame superior
frame_imagen2 = tk.Frame(frame_superior)
frame_imagen2.pack(side=tk.LEFT, padx=10)
label_imagen2 = tk.Label(frame_imagen2, image=imagen2)
label_imagen2.pack()
etiqueta2 = tk.Label(frame_imagen2, text="Imagen 2")
etiqueta2.pack()

# Añadir tercera imagen y su etiqueta al frame inferior
frame_imagen3 = tk.Frame(frame_inferior)
frame_imagen3.pack()
label_imagen3 = tk.Label(frame_imagen3, image=imagen3)
label_imagen3.pack()
etiqueta3 = tk.Label(frame_imagen3, text="Imagen 3")
etiqueta3.pack()

root.mainloop()
