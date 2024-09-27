from cx_Freeze import setup, Executable
import os

# Definir archivos de datos a incluir
files = [("src/front/resource", ["src/front/resource/inta_icon.png", "src/front/resource/inta_icon.ico"])]

# Incluir ícono y archivo principal
executables = [
    Executable(
        script="main.py",  # Tu archivo principal de Python
        icon="src/front/resource/inta_icon.ico",  # Ícono del ejecutable
    )
]

# Configuración del paquete
setup(
    name="Magnetic Moment Calculation",
    version="1.0",
    description="Aplicación para calcular el momento magnético",
    options={
        "build_exe": {
            "packages": ["os", "sys", "customtkinter","reportlab","numpy","pandas","pillow"],  # Incluye las dependencias
            "include_files": files,  # Archivos de recursos
        }
    },
    executables=executables,
)
