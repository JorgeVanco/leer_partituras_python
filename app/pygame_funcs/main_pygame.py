import pickle
import pygame
import pygame_gui
from pygame_funcs.pop_up import pop_up as pop
from Classes.Notas import Partitura
from lectura_partituras.functions.functions import find_complete_path
import os
import cv2 as cv

def actualizar_partitura(partitura:Partitura, PATH:str, complete_path:str):
    image_rectangulos = cv.imread(PATH)
    for pentagrama in partitura.pentagramas:
        count = 0
        
        for nota in pentagrama.notas:
            posiciones = nota.rectangulo
            org = (posiciones[2] + (abs(posiciones[3] - posiciones[2])) //
                            2, pentagrama.posiciones[-1] - 20*(count % 2)-5)
            if nota.nota != "otra figura":
                image_rectangulos = cv.putText(
                    image_rectangulos, nota.nota + " " + str(nota.figura), org, cv.FONT_HERSHEY_SIMPLEX, 0.35, 0, 1, cv.LINE_AA)
            count += 1

    cv.imwrite(complete_path + "app/pygame_funcs/imagen_partitura_modificada.png", image_rectangulos)
    return pygame.image.load(complete_path + "app/pygame_funcs/imagen_partitura_modificada.png")

def get_nombre_partitura(PATH:str) -> str:
    
    name = ""
    i = len(PATH) - 1
    letra = PATH[i]
    while letra != "/" and i >= 0:
        name = letra + name
        i -= 1
        letra = PATH[i]

    return name


def main_pygame():

    complete_path = find_complete_path()

    pygame.init()

    running:bool = True
    RED = (255, 0, 0)
    GRAY = (150, 150, 150)
    manager = pygame_gui.UIManager((800, 600))

    with open(complete_path + "app/pygame_funcs/partes_imagenes.obj", "rb") as fh:
        img = pickle.load(fh)
        notas = pickle.load(fh)
        posiciones_pentagramas = pickle.load(fh)
        PATH = pickle.load(fh)

    

    img = pygame.image.load(PATH)

    w, h = img.get_size()

    screen = pygame.display.set_mode((w, h))
    window_surface = pygame.display.set_mode((w, h))

    img.convert()

    rect = img.get_rect()
    rect.center = w//2, h//2
    moving = False


    partitura = Partitura(posiciones_pentagramas, notas)
    clock = pygame.time.Clock()

    img = actualizar_partitura(partitura, PATH, complete_path)

    i:int = 0
    while running:
        time_delta = clock.tick(60)/1000.0
        cambio = False
        cambio_posicion = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                index = partitura.find_index_nota_at_position(pygame.mouse.get_pos())
                if index:
                    i = index
                    cambio_posicion = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    i -= 1
                    cambio_posicion = True
                elif event.key == pygame.K_RIGHT:
                    i += 1
                    cambio_posicion = True
                elif event.key == pygame.K_RETURN:
                    pop.open_popup(partitura, i)
                    cambio = True
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    partitura.borrar_nota(i)
                    cambio = True
                    cambio_posicion = True
                elif event.key == pygame.K_ESCAPE:
                    running = False
            if cambio_posicion:
                if i >= len(partitura.notas):
                    i = 0
                elif i < 0:
                    i = len(partitura.notas) - 1
                
            if cambio:
                img = actualizar_partitura(partitura, PATH, complete_path)

            manager.process_events(event)
        
        manager.update(time_delta)
        
        screen.fill(GRAY)
        screen.blit(img, rect)
        posiciones = partitura.notas[i].rectangulo
        pygame.draw.rect(screen, RED, pygame.Rect(posiciones[2] - 5,posiciones[0] - 5,posiciones[3] - posiciones[2] + 10,posiciones[1] - posiciones[0] + 10), 2)
        manager.draw_ui(window_surface)
        pygame.display.update()



    with open(complete_path + "app/notas_partituras/notas_pruebas.obj", "wb") as fh:
        pickle.dump(partitura.notas, fh)

    NOMBRE_IMAGEN = get_nombre_partitura(PATH)
    pygame.image.save(img, complete_path + "app/pygame_funcs/" + NOMBRE_IMAGEN)
    os.remove(complete_path + "app/pygame_funcs/imagen_partitura_modificada.png")

    return True