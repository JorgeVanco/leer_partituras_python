import tkinter as tk
from tkinter import filedialog
from Classes.Errors import ErrorPath

def file_browser() -> str:
    """
    Abre la ventana del explorador de archivos para que el usuario pueda
    elegir la imagen de la partitura que quiere leer

    returns: path (str) : La ruta a la imagen de la partitura elegida
    """
    try:
        top = tk.Tk()
        top.withdraw()  # hide window

        file_name = filedialog.askopenfilename(parent=top, title = "Select file", filetypes = (("image", ".jpeg"),
                        ("image", ".png"),
                        ("image", ".jpg"),))
        top.destroy()
        return file_name
    except tk.TclError as e:
        raise ErrorPath(f"No se ha podido abrir: {e}")
