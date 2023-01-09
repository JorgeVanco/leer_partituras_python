from pysine import sine
import math
import json
import pickle
import time
from lectura_partituras.functions.functions import find_complete_path
# from Classes.Notas import Nota, Pentagrama
def frecuencia(nota:int, octava:int) -> float:
    """
    Donde "octava" es un entero entre 1 y 8, y "nota" es un entero en el rango de 1 a
    12. Do=1, Do#=2, Re=3, Re#=4, Mi=5, Fa=6, Fa#=7, Sol=8, Sol#=9, La=10,
    La#=11, Si=12.
    """
    return 440 * math.exp((octava - 3 + (nota - 10)/12) * math.log(2))

NOTAS_MUSICALES = {0: "Do", 1: "Re", 2: "Mi", 
                        3: "Fa", 4: "Sol", 5: "La", 6: "Si"}
NOTAS_MUSICALES = {v:k for k,v in NOTAS_MUSICALES.items()}
# frecuencias = {
#     "DO": 
# }
# print(frecuencia(10, 3))
# sine(frequency=440.0, duration=1.0)  # plays a 1s sine wave at 440 Hz
# sine(frequency=415.3, duration=1.0)  # plays a 1s sine wave at 440 Hz
def main_musica():
    complete_path = find_complete_path()

    try:
        with open(complete_path + "app/notas_partituras/notas_pruebas.obj", "rb") as fh:
            notas = pickle.load(fh)
    except FileNotFoundError:
        raise FileNotFoundError("No se ha leído ninguna partitura todavía")


    for nota in notas:
        if nota.nota == "silencio":
            time.sleep(0.5)
        elif nota.nota != "clave de sol" and nota.nota != "otra figura":
            # print(getattr(nota, "octava"))
            # octava = 3
            # if nota.octava_alta: octava += 1
            # elif nota.octava_baja: octava -= 1
            frec = frecuencia(NOTAS_MUSICALES[nota.nota] + 1, nota.octava)   
            if nota.figura.lower() == "negra":
                duracion = 0.5
            elif nota.figura.lower() == "blanca":
                duracion = 1
            elif nota.figura.lower() == "redonda":
                duracion = 2
            elif nota.figura.lower() == "corchea":
                duracion = 0.25
            sine(frec, duracion) 
            time.sleep(0.1)