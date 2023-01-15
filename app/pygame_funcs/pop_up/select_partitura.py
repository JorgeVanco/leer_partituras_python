import tkinter as tk
from Classes.Notas import Partitura

class Indice:
    """
    Clase para guardar el valor del índice de la partitura y poderlo modificar
    con tkinter
    """
    def __init__(self, index:int):
        self.index = index

def selected_item(listbox:tk.Listbox, indice:Indice, root:tk.Tk) -> None:
    """
    Guarda el índice de la selección

    Args:
        listbox (tk.Listbox): La variable que guarda la lista de las partituras
        indice (Indice): El objeto que guarda el índice
        root (tk.Tk): La superficie de tkinter
    """
    try:
        indice.index = listbox.curselection()[0]
        root.destroy()
    except IndexError: # Si no hay ninguna seleccionada, se mantiene abierta la pestaña
        pass

def elegir_partitura(partituras_existentes:list[Partitura]) -> int:
    """
    Abre una pantalla con todas las partituras posibles para poder elegir
    la que se quiera

    Args:
        partituras_existentes (list[Partitura]): La lista de partituras

    Returns:
        indice.index (int): El índice de la partitura seleccionada en la lista de partituras
    """
    indice = Indice(len(partituras_existentes) - 1) # Para que se devuelva el último como defecto

    root = tk.Tk()
    root.geometry("400x420")
    root.title("Elija la partitura")

    listbox = tk.Listbox(borderwidth=0, width=50, height=180)
    listbox.insert(tk.END, *(f"{i + 1}.-"+str(partituras_existentes[i]) for i in range(len(partituras_existentes))))

    button = tk.Button(root, text='Select', command = lambda : selected_item(listbox, indice, root), width=42)

    button.pack(side='bottom')
    listbox.pack()


    root.mainloop()
    
    return indice.index