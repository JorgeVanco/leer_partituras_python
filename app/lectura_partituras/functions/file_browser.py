import tkinter as tk
from tkinter.filedialog import askopenfilename

def file_browser() -> str:
    """
    Abre la ventana del explorador de archivos para que el usuario pueda
    elegir la imagen de la partitura que quiere leer

    returns: path (str) : La ruta a la imagen de la partitura elegida
    """
    try:
        root = tk.Tk()
        root.withdraw() # part of the import if you are not using other tkinter functions
        path:str = askopenfilename()
        root.update()
        # root.mainloop()
        root.destroy()
    except tk.TclError as e:
        print("TclError", e)
        path = None
    return path  # returns path to file chosen by user