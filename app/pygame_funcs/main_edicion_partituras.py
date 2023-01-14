import pickle
import pygame
import pygame_gui
from pygame_funcs.pop_up import pop_up as pop
from Classes.Notas import Partitura
from lectura_partituras.functions.functions import find_complete_path, get_nombre_fichero, resize_image
import os
import cv2 as cv
from Classes.Errors import ErrorPentagramas

def actualizar_partitura(partitura:Partitura, PATH:str, complete_path:str):
    image_rectangulos = cv.imread(PATH)
    SIMBOLOS_ALTERACIONES:dict = {"Sostenido": "# ", "Natural": " ", "Bemol": " b "}
    alteracion_armadura:str = None
    notas_afectadas_por_armadura:list = []
    ORDEN_SOSTENIDOS_ARMADURA = ["Fa", "Do", "Sol", "Re", "La", "Mi", "Si"]
    ORDEN_BEMOLES_ARMADURA = ORDEN_SOSTENIDOS_ARMADURA[::-1]
    for pentagrama in partitura.pentagramas:
        count = 0
        
        for nota in pentagrama.notas:

            if nota.nota == "Armadura":
                alteracion_armadura = nota.alteracion
                if alteracion_armadura == "Sostenido":
                    notas_afectadas_por_armadura = ORDEN_SOSTENIDOS_ARMADURA[:nota.numero_alteraciones]
                elif alteracion_armadura == "Bemol":
                    notas_afectadas_por_armadura = ORDEN_BEMOLES_ARMADURA[:nota.numero_alteraciones]
                else:
                    notas_afectadas_por_armadura = []

            posiciones = nota.rectangulo
            org = (posiciones[2] + (abs(posiciones[3] - posiciones[2])) //
                            2, pentagrama.posiciones[-1] - 20*(count % 2)-5)
            if nota.nota != "Otra figura":
                if nota.nota not in ["Clave de sol", "Armadura", "Silencio"]:
                    if nota.nota in notas_afectadas_por_armadura:
                        nota.alteracion = alteracion_armadura
                    elif not nota.alteracion_manual:
                        nota.alteracion = "Natural"
                image_rectangulos = cv.putText(
                    image_rectangulos, nota.nota + SIMBOLOS_ALTERACIONES[nota.alteracion] + str(nota.figura), org, cv.FONT_HERSHEY_SIMPLEX, 0.35, 0, 1, cv.LINE_AA)
            count += 1

    saved_correctly = cv.imwrite(complete_path + "app/pygame_funcs/imagenes_editadas/imagen_partitura_modificada.png", image_rectangulos)

    if not saved_correctly:
        os.mkdir(complete_path + "app/pygame_funcs/imagenes_editadas/")
        cv.imwrite(complete_path + "app/pygame_funcs/imagenes_editadas/imagen_partitura_modificada.png", image_rectangulos)

    return pygame.image.load(complete_path + "app/pygame_funcs/imagenes_editadas/imagen_partitura_modificada.png")


def limpiar(complete_path:str, resized:bool) -> None:
    os.remove(complete_path + "app/pygame_funcs/imagenes_editadas/imagen_partitura_modificada.png")

    if resized:
        os.remove(complete_path+"app/pygame_funcs/imagen_resized.png")

def main_edicion_partituras():

    complete_path = find_complete_path(__file__)

    running:bool = True
    RED = (255, 0, 0)
    GRAY = (150, 150, 150)
    manager = pygame_gui.UIManager((800, 600))

    with open(complete_path + "app/pygame_funcs/partes_imagenes.obj", "rb") as fh:
        notas = pickle.load(fh)
        posiciones_pentagramas = pickle.load(fh)
        PATH = pickle.load(fh)
        resized = pickle.load(fh)
        fraccion = pickle.load(fh)

    
    NOMBRE_IMAGEN = get_nombre_fichero(PATH)
    NOMBRE_PARTITURA = NOMBRE_IMAGEN[:NOMBRE_IMAGEN.find(".")]
    img = pygame.image.load(PATH)

    if resized:
        img = cv.imread(PATH)
        img = resize_image(fraccion, img)
        cv.imwrite(complete_path + "app/pygame_funcs/imagen_resized.png", img)
        PATH = complete_path + "app/pygame_funcs/imagen_resized.png"
        img = pygame.image.load(complete_path+"app/pygame_funcs/imagen_resized.png")
        

    w, h = img.get_size()

    screen = pygame.display.set_mode((w, h))
    window_surface = pygame.display.set_mode((w, h))
    pygame.display.set_caption(NOMBRE_PARTITURA)

    img.convert()

    rect = img.get_rect()
    rect.center = w//2, h//2


    partitura = Partitura(posiciones_pentagramas, notas, NOMBRE_PARTITURA)
    clock = pygame.time.Clock()

    img = actualizar_partitura(partitura, PATH, complete_path)
    if len(notas) == 0:
        limpiar(complete_path, resized)
        raise ErrorPentagramas("No se han encontrado notas")
    i:int = 0
    while running:

        time_delta = clock.tick(60)/1000.0
        cambio = False
        cambio_posicion = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1:
                    index = partitura.find_index_nota_at_position(pygame.mouse.get_pos())
                    if index:
                        i = index
                        cambio_posicion = True
                    
                else:
                    cambio = pop.open_popup(partitura, i)
                    

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    i -= 1
                    cambio_posicion = True
                elif event.key == pygame.K_RIGHT:
                    i += 1
                    cambio_posicion = True
                elif event.key == pygame.K_RETURN:
                    cambio = pop.open_popup(partitura, i)
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
        try:
            posiciones = partitura.notas[i].rectangulo
        except IndexError:
            limpiar(complete_path, resized)
            raise ErrorPentagramas("Se han eliminado todas las notas")
        pygame.draw.rect(screen, RED, pygame.Rect(posiciones[2] - 5,posiciones[0] - 5,posiciones[3] - posiciones[2] + 10,posiciones[1] - posiciones[0] + 10), 2)
        manager.draw_ui(window_surface)
        pygame.display.update()


    img_path = complete_path + "app/pygame_funcs/imagenes_editadas/" + NOMBRE_IMAGEN
    partitura.img_path = img_path


    pygame.image.save(img, partitura.img_path)

    limpiar(complete_path, resized)

    with open(complete_path + "app/notas_partituras/notas_pruebas.obj", "wb") as fh:
        pickle.dump(partitura, fh)
    return True