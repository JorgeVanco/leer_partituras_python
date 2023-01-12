import tkinter as tk

def save(root, pentagrama, nota, entries, value_var):
    i: int = 0
    for var in vars(nota).keys():
        if var != "rectangulo" and var != "pentagrama" and var != "alteracion":
            value = entries[i].get()
            if value.isdecimal():
                value = int(value)
            else:
                value = value.capitalize()
                if var == "figura" and value not in ["Blanca", "Corchea", "Redonda", "Negra"]\
                        or var == "nota" and value not in ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si", "Silencio", "Clave de sol", "Otra figura"]:
                    value = getattr(nota, var)
            pentagrama.cambiar_nota(nota, var, value)
            i += 1
        elif var == "alteracion":
            pentagrama.cambiar_nota(nota, var, value_var.get())
        
    root.destroy()


def remove(root, partitura, index: int):
    partitura.borrar_nota(index)
    root.destroy()


def onKeyPress(event, root, pentagrama, nota, entries):
    if event.keysym == "Return":
        save(root, pentagrama, nota, entries)




def open_popup(partitura, index: int):

    nota = partitura.notas[index]
    pentagrama = nota.pentagrama

    root = tk.Tk()
    root.geometry("750x270")

    root.title("Configuración nota")

    labels = []
    entries = []
    i: int = 0

    for var, value in vars(nota).items():
        if var != "rectangulo" and var != "pentagrama" and var != "alteracion":
            labels.append(tk.Label(root, text = var).grid(row=i, column=0))
            entry = tk.Entry(root)
            entry.grid(row=i, column=1)
            entry.insert(0, value)
            if i == 0:
                entry.focus_force()
            entries.append(entry)
            i += 1
        elif var == "alteracion":
            label = tk.Label(root, text="Alteración")
            label.grid(row = i, column = 1)
            i += 1
            value_var = tk.StringVar()
            value_var.set(nota.alteracion)

            b1 = tk.Radiobutton(root, text="Natural", variable=value_var,
                        value="Natural")
            b1.grid(row = i, column = 1)
            i += 1
            b2 = tk.Radiobutton(root, 
            text="Sostenido", variable=value_var,
                        value="Sostenido")
            b2.grid(row = i, column = 1)
            i += 1
            b3 = tk.Radiobutton(root, text="Bemol", variable=value_var,
                        value="Bemol")
            b3.grid(row = i, column = 1)
            i += 1
    
    button_borrar = tk.Button(root, text="Borrar nota", padx=19, pady=5, command=lambda: remove(
        root, partitura, index), background="red")
    button_borrar.grid(row=i, column=0, columnspan=3)
    button_guardar = tk.Button(root, text="Guardar", padx=19, pady=5, command=lambda: save(
        root, pentagrama, nota, entries, value_var), background="green")
    button_guardar.grid(row=i+1, column=0, columnspan=3)
    root.bind('<KeyPress>', lambda event: onKeyPress(
        event, root, pentagrama, nota, entries))

    root.mainloop()

    return True