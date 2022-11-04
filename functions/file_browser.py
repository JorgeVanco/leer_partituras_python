import tkinter as tk
from tkinter.filedialog import askopenfilename

def file_browser():
    root = tk.Tk()
    root.withdraw() # part of the import if you are not using other tkinter functions
    path = askopenfilename()
    root.update()
    return path  # returns path to file chosen by user