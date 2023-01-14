import tkinter as tk
from Classes.Notas import Partitura, Pentagrama, Nota

def remove(root:tk.Tk, partitura:Partitura, index: int) -> None:
    """
    Borra la nota de la partitura

    Args:
        root (tk.Tk): La instancia de tkinter
        partitura (Partitura): La partitura que se está editando
        index (int): El indice de la nota que se quiere borrar
    """
    partitura.borrar_nota(index)
    root.destroy()


def onKeyPress(event, root:tk.Tk):
    """
    Si se presiona Enter, se quita el pop up

    Args:
        Event: EL evento de la tecla presionada
        root (tk.Tk): La instancia de tkinter
    """
    if event.keysym == "Return":
        root.destroy()


def set_nota(root:tk.Tk, partitura:Partitura, pentagrama:Pentagrama, POSIBILIDADES:dict, atributo:str,value, index:int, alteracion_manual:bool = False) -> None:
    """
    Cambia el valor de algún atributo de la nota

    Args:
        root (tk.Tk): La instancia de tkinter
        partitura (Partitura): La partitura que se está editando
        pentagrama (Pentagrama): El pentagrama en el que se encuentra la nota
        POSIBILIDADES (dict): Diccionario con las distintas posibilidades para cada atributo
        atributo (str): El atributo que se va a cambiar
        value (any): El nuevo valor del atributo
        index (int): El índice de la nota a modificar en la lista de notas de la partitura
        alteracion_manual (bool): Si la alteración de la nota se ha editado en particular o a través de la armadura
    """
    nota = partitura.notas[index]
    if alteracion_manual:
        nota.alteracion_manual = True
    if atributo == "octava":
        POSIBILIDADES_OCTAVAS_REVERSE = {v:k for k,v in POSIBILIDADES["OCTAVAS"].items()}
        value = POSIBILIDADES_OCTAVAS_REVERSE[value]
    pentagrama.cambiar_nota(nota, atributo, value)
    draw(root, partitura, POSIBILIDADES, index)

def draw(root:tk.Tk, partitura:Partitura, POSIBILIDADES:dict, index:int) -> None:
    """
    Dibuja la ingerfaz gráfica de la edición de una nota

    Args:
        root (tk.Tk): La instancia de tkinter
        partitura (Partitura): La partitura que se está editando
        POSIBILIDADES (dict): Diccionario con las distintas posibilidades para cada atributo
        index (int): El índice de la nota a modificar en la lista de notas de la partitura
    """
    for widget in root.winfo_children():
        widget.destroy()


    nota:Nota = partitura.notas[index]
    pentagrama:Pentagrama = nota.pentagrama


    variable_nota:tk.StringVar = tk.StringVar()
    variable_nota.set(nota.nota)

    tk.Label(root, text = "Nota: ").grid(row=0, column=0)
    opciones_nota:tk.OptionMenu = tk.OptionMenu(root, variable_nota, *POSIBILIDADES["NOTAS_POSIBLES"], command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "nota", value, index))
    opciones_nota.grid(row = 0, column = 1)

    i: int = 1

    if nota.nota not in ["Clave de sol", "Otra figura", "Silencio", "Armadura"]:
        tk.Label(root, text = "Octava: ").grid(row=1, column=0)
        variable_octava:tk.StringVar = tk.StringVar()
        variable_octava.set(POSIBILIDADES["OCTAVAS"][nota.octava])
        opciones_octava = tk.OptionMenu(root, variable_octava, *POSIBILIDADES["OCTAVAS"].values(), command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "octava", value, index))
        opciones_octava.grid(row = 1, column = 1)
        
        tk.Label(root, text = "Figura: ").grid(row=2, column=0)
        variable_figura:tk.StringVar = tk.StringVar()
        variable_figura.set(nota.figura)
        opciones_figura = tk.OptionMenu(root, variable_figura, *POSIBILIDADES["FIGURAS_POSIBLES"], command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "figura", value, index))
        opciones_figura.grid(row = 2, column = 1)
        
        tk.Label(root, text = "Alteración: ").grid(row=3, column=0)
        variable_alteracion:tk.StringVar = tk.StringVar()
        variable_alteracion.set(nota.alteracion)
        opciones_alteracion = tk.OptionMenu(root, variable_alteracion, *POSIBILIDADES["ALTERACIONES_POSIBLES"], command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "alteracion", value, index, True))
        opciones_alteracion.grid(row = 3, column = 1)
        
        i = 4


    elif nota.nota == "Silencio":
        tk.Label(root, text = "Figura: ").grid(row=1, column=0)
        variable_figura:tk.StringVar = tk.StringVar()
        variable_figura.set(nota.figura)
        opciones_figura = tk.OptionMenu(root, variable_figura, *POSIBILIDADES["SILENCIOS_POSIBLES"], command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "figura", value, index))
        opciones_figura.grid(row = 1, column = 1)
        
        i = 2
        
    elif nota.nota == "Armadura":
        tk.Label(root, text = "Alteración: ").grid(row=1, column=0)
        variable_alteracion:tk.StringVar = tk.StringVar()
        variable_alteracion.set(nota.alteracion)
        opciones_alteracion = tk.OptionMenu(root, variable_alteracion, *POSIBILIDADES["ALTERACIONES_POSIBLES"], command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "alteracion", value, index))
        opciones_alteracion.grid(row = 1, column = 1)

        tk.Label(root, text = "Número alteraciones: ").grid(row=2, column=0)
        variable_numero_alteraciones:tk.StringVar = tk.StringVar()
        variable_numero_alteraciones.set(nota.numero_alteraciones)
        opciones_numero_alteraciones = tk.OptionMenu(root, variable_numero_alteraciones, 1,2,3,4,5,6,7, command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "numero_alteraciones", value, index))
        opciones_numero_alteraciones.grid(row = 2, column = 1)
        
        i = 3

    button_borrar = tk.Button(root, text="Borrar nota", padx=19, pady=5, command = lambda: remove(
        root, partitura, index), background="red")
    button_borrar.grid(row=i, column=0, columnspan=1)

    button_guardar = tk.Button(root, text="Cerrar", padx=19, pady=5, command = lambda: root.destroy(), background="green")
    button_guardar.grid(row=i, column=1, columnspan=1)
    root.bind('<KeyPress>', lambda event: onKeyPress(event, root))



def open_popup(partitura:Partitura, index: int) -> bool:
    """
    Inicia la interfaz gráfica para la edición de la nota

    Args:
        partitura (Partitura): La partitura que se está editando
        index (int): El índice de la nota a modificar en la lista de notas de la partitura

    Returns:
        True: Para que se actualice la partitura
    """
    POSIBILIDADES:dict = {
        "NOTAS_POSIBLES" : ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si", "Silencio", "Clave de sol", "Armadura", "Otra figura"],
        "OCTAVAS" : {2: "Octava baja", 3: "Octava normal", 4: "Octava alta"},
        "FIGURAS_POSIBLES" : ["Corchea", "Negra", "Blanca", "Redonda"],
        "ALTERACIONES_POSIBLES" : ["Natural", "Sostenido", "Bemol"],
        "SILENCIOS_POSIBLES" :  ["Silencio de negra", "Silencio de blanca", "Silencio de redonda", "Silencio de corchea"]
    }
    
    
    root = tk.Tk()
    root.geometry("240x180")
        
    
    root.title("Configuración nota")
    
    draw(root, partitura, POSIBILIDADES, index)
    
    root.mainloop()
    
    return True