from pysine import sine
import math
import pygame
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

NOTAS_MUSICALES = {"Do":1, "Re":3, "Mi":5, "Fa":6, "Sol":8, "La":10, "Si":12}
ALTERACIONES = {"Sostenido" : 1, "Natural": 0, "Bemol": -1}

def main_musica():
    complete_path = find_complete_path(__file__)
    pygame.init()

    try:
        with open(complete_path + "app/notas_partituras/notas_pruebas.obj", "rb") as fh:
            partitura = pickle.load(fh)
    except FileNotFoundError:
        raise FileNotFoundError("No se ha leído ninguna partitura todavía")

    RED = (255, 0, 0)
    GRAY = (150, 150, 150)

    img = pygame.image.load(partitura.img_path)


    w, h = img.get_size()

    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption(partitura.nombre)
    img.convert()

    rect = img.get_rect()
    rect.center = w//2, h//2

    i = 0

    running = True
    for nota in partitura.notas:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        if not running:
            break

        screen.fill(GRAY)
        screen.blit(img, rect)
        posiciones = nota.rectangulo
        pygame.draw.rect(screen, RED, pygame.Rect(posiciones[2] - 5,posiciones[0] - 5,posiciones[3] - posiciones[2] + 10,posiciones[1] - posiciones[0] + 10), 2)
        pygame.display.update()
        if nota.nota == "Silencio":
            time.sleep(0.5)
        elif nota.nota != "Clave de sol" and nota.nota != "Otra figura":
            frec = frecuencia(NOTAS_MUSICALES[nota.nota] + nota.alteracion, nota.octava)   
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

        i += 1
        

    return False