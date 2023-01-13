import tkinter as tk

def remove(root, partitura, index: int):
    partitura.borrar_nota(index)
    root.destroy()


def onKeyPress(event, root):
    if event.keysym == "Return":
        root.destroy()


def set_nota(root, partitura, pentagrama, POSIBILIDADES, atributo,value, index):
    nota = partitura.notas[index]
    if atributo == "octava":
        POSIBILIDADES_OCTAVAS_REVERSE = {v:k for k,v in POSIBILIDADES["OCTAVAS"].items()}
        value = POSIBILIDADES_OCTAVAS_REVERSE[value]
    pentagrama.cambiar_nota(nota, atributo, value)
    draw(root, partitura, POSIBILIDADES, index)

def draw(root, partitura, POSIBILIDADES, index):
    
    for widget in root.winfo_children():
        widget.destroy()


    nota = partitura.notas[index]
    pentagrama = nota.pentagrama


    variable_nota = tk.StringVar()
    variable_nota.set(nota.nota)

    tk.Label(root, text = "Nota: ").grid(row=0, column=0)
    opciones_nota = tk.OptionMenu(root, variable_nota, *POSIBILIDADES["NOTAS_POSIBLES"], command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "nota", value, index))
    opciones_nota.grid(row = 0, column = 1)

    form = [("nota", opciones_nota)]

    i: int = 1

    if nota.nota not in ["Clave de sol", "Otra figura", "Silencio"]:
        tk.Label(root, text = "Octava: ").grid(row=1, column=0)
        variable_octava = tk.StringVar()
        variable_octava.set(POSIBILIDADES["OCTAVAS"][nota.octava])
        opciones_octava = tk.OptionMenu(root, variable_octava, *POSIBILIDADES["OCTAVAS"].values(), command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "octava", value, index))
        opciones_octava.grid(row = 1, column = 1)

        tk.Label(root, text = "Figura: ").grid(row=2, column=0)
        variable_figura = tk.StringVar()
        variable_figura.set(nota.figura)
        opciones_figura = tk.OptionMenu(root, variable_figura, *POSIBILIDADES["FIGURAS_POSIBLES"], command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "figura", value, index))
        opciones_figura.grid(row = 2, column = 1)

        tk.Label(root, text = "Alteración: ").grid(row=3, column=0)
        variable_alteracion = tk.StringVar()
        variable_alteracion.set(nota.alteracion)
        opciones_alteracion = tk.OptionMenu(root, variable_alteracion, *POSIBILIDADES["ALTERACIONES_POSIBLES"], command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "alteracion", value, index))
        opciones_alteracion.grid(row = 3, column = 1)

        form.append(("octava", variable_octava))
        form.append(("figura", variable_figura))
        form.append(("alteracion", variable_alteracion))

        i = 4


    elif nota.nota == "Silencio":
        tk.Label(root, text = "Figura: ").grid(row=1, column=0)
        variable_figura = tk.StringVar()
        variable_figura.set(nota.figura)
        opciones_figura = tk.OptionMenu(root, variable_figura, *POSIBILIDADES["SILENCIOS_POSIBLES"], command = lambda value: set_nota(root, partitura, pentagrama, POSIBILIDADES, "figura", value, index))
        opciones_figura.grid(row = 1, column = 1)
        
        
        i = 2


    button_borrar = tk.Button(root, text="Borrar nota", padx=19, pady=5, command = lambda: remove(
        root, partitura, index), background="red")
    button_borrar.grid(row=i, column=0, columnspan=1)

    button_guardar = tk.Button(root, text="Cerrar", padx=19, pady=5, command = lambda: root.destroy(), background="green")
    button_guardar.grid(row=i, column=1, columnspan=1)
    root.bind('<KeyPress>', lambda event: onKeyPress(event, root))



def open_popup(partitura, index: int):
    POSIBILIDADES = {
        "NOTAS_POSIBLES" : ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si", "Silencio", "Clave de sol", "Otra figura"],
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