import pickle
import pygame
from pygame_funcs.pop_up import pop_up as pop
from Classes.Notas import Partitura, Nota
from Classes.Ajustes import Ajustes
from lectura_partituras.functions.functions import find_complete_path, get_nombre_fichero, resize_image, get_ajustes
import os
import cv2 as cv
from Classes.Errors import ErrorPentagramas
from pygame_funcs.pop_up.select_partitura import elegir_partitura

def get_notas_afectadas_por_armadura(armadura:Nota, ORDEN_SOSTENIDOS_ARMADURA:list[str], ORDEN_BEMOLES_ARMADURA:list[str]) -> list[str]:
    """
    Determina las notas que son alteradas a partir del número de alteraciones en la armadura

    Args:
        armadura (Nota): La nota que es la armadura
        ORDEN_SOSTENIDOS_ARMADURA (list[str]): Lista con las notas en orden de aparición por sostenidos en la armadura
        ORDEN_BEMOLES_ARMADURA (list[str]): Lista con las notas en orden de aparición por bemoles en la armadura

    Returns:
        notas_afectadas_por_armadura (list[str]): Lista con el nombre de las notas que son alteradas por la armadura
    """
    alteracion_armadura = armadura.alteracion
    if alteracion_armadura == "Sostenido":
        notas_afectadas_por_armadura = ORDEN_SOSTENIDOS_ARMADURA[:armadura.numero_alteraciones]
    elif alteracion_armadura == "Bemol":
        notas_afectadas_por_armadura = ORDEN_BEMOLES_ARMADURA[:armadura.numero_alteraciones]
    else:
        notas_afectadas_por_armadura = []
    return notas_afectadas_por_armadura

def set_alteracion_nota(nota:Nota, notas_afectadas_por_armadura:list[str], alteracion_armadura:str) -> None:
    """
    Determina la alteraición de la nota a partir de la armadura y si ha sido editada manualmente la propia nota

    Args:
        nota (Nota): La nota
        notas_afectadas_por_armadura (list[str]): Lista con el nombre de las notas que son alteradas por la armadura
        alteracion_armadura (str): La alteración de la armadura
    """
    if nota.nota in notas_afectadas_por_armadura and not nota.alteracion_manual:
        nota.alteracion = alteracion_armadura
    elif not nota.alteracion_manual:
        nota.alteracion = "Natural"  # Para que se eliminen las alteraciones cuando bajamos el número de alteraciones en la armadura


def actualizar_partitura(partitura:Partitura, PATH:str, complete_path:str, ORDEN_SOSTENIDOS_ARMADURA:list[str], ORDEN_BEMOLES_ARMADURA:list[str], SIMBOLOS_ALTERACIONES:dict) -> pygame.Surface:
    """
    Dibuja el nombre de las notas en la partitura

    Args:
        partitura (Partitura): La partitura que se está editando
        path (str) : La ruta a la imagen de la partitura elegida
        complete_path (str): La ruta absoluta hasta el directorio app
        ORDEN_SOSTENIDOS_ARMADURA (list[str]): Lista con las notas en orden de aparición por sostenidos en la armadura
        ORDEN_BEMOLES_ARMADURA (list[str]): Lista con las notas en orden de aparición por bemoles en la armadura
        SIMBOLOS_ALTERACIONES (dict): El símbolo correspondiente a cada alteración

    Returns:
        La imagen de la partitura con el nombre de las notas en formato pygame
    """
    image_rectangulos = cv.imread(PATH)
    alteracion_armadura:str = None
    notas_afectadas_por_armadura:list = []

    AJUSTES:Ajustes = get_ajustes()
    
    for pentagrama in partitura.pentagramas:
        count = 0
        
        for nota in pentagrama.notas:
            figura = nota.figura
            if nota.nota == "Armadura":
                notas_afectadas_por_armadura = get_notas_afectadas_por_armadura(nota, ORDEN_SOSTENIDOS_ARMADURA, ORDEN_BEMOLES_ARMADURA)
                alteracion_armadura  = nota.alteracion
                figura = str(nota.numero_alteraciones)
            
            posiciones = nota.rectangulo
            org = (posiciones[2] + (abs(posiciones[3] - posiciones[2])) //
                            2, pentagrama.posiciones[-1] - 20*(count % 2)-5)
            if nota.nota != "Otra figura":
                if nota.nota not in ["Clave de sol", "Armadura", "Silencio"]:
                    set_alteracion_nota(nota, notas_afectadas_por_armadura, alteracion_armadura)
                image_rectangulos = cv.putText(
                    image_rectangulos, nota.nota + SIMBOLOS_ALTERACIONES[nota.alteracion] + str(figura), org, cv.FONT_HERSHEY_SIMPLEX, AJUSTES.FONT_SIZE, 0, 1, cv.LINE_AA)
            count += 1

    saved_correctly = cv.imwrite(complete_path + "app/pygame_funcs/imagenes_editadas/imagen_partitura_modificada.png", image_rectangulos)

    if not saved_correctly:
        os.mkdir(complete_path + "app/pygame_funcs/imagenes_editadas/")
        cv.imwrite(complete_path + "app/pygame_funcs/imagenes_editadas/imagen_partitura_modificada.png", image_rectangulos)

    return pygame.image.load(complete_path + "app/pygame_funcs/imagenes_editadas/imagen_partitura_modificada.png")


def limpiar(complete_path:str, resized:bool) -> None:
    """
    Elimina las imagenes temporales creadas durante la edición

    Args:
        complete_path (str): La ruta absoluta hasta el directorio app
        resized (bool): Si la partitura ha sido cambiada de tamaño o no
    """
    os.remove(complete_path + "app/pygame_funcs/imagenes_editadas/imagen_partitura_modificada.png")

    if resized:
        os.remove(complete_path + "app/pygame_funcs/imagen_resized.png")


def main_edicion_partituras() -> bool:
    """
    Dibuja imagen de la partitura con el nombre de las notas y te permite editarlas y eliminarlas.
    Se puede cambiar de nota clickeando en ella o con las flechas del teclado
    Se guarda automáticamente

    Returns:
        True: Para que el programa  siga corriendo
    """
    ORDEN_SOSTENIDOS_ARMADURA:list[str] = ["Fa", "Do", "Sol", "Re", "La", "Mi", "Si"]
    ORDEN_BEMOLES_ARMADURA:list[str] = ORDEN_SOSTENIDOS_ARMADURA[::-1]
    SIMBOLOS_ALTERACIONES:dict = {"Sostenido": "# ", "Natural": " ", "Bemol": " b "}

    complete_path = find_complete_path(__file__)

    running:bool = True
    RED = (255, 0, 0)
    GRAY = (150, 150, 150)

    # Carga los datos de la partitura
    try:
        with open(complete_path + "app/notas_partituras/partituras_guardadas.obj", "rb") as fh:
            partituras_existentes:list[Partitura] = pickle.load(fh)
    except FileNotFoundError:
        raise FileNotFoundError("No se ha leído ninguna partitura todavía")

    INDICE_PARTITURA = elegir_partitura(partituras_existentes)
    if INDICE_PARTITURA == None:
        return True
    partitura:Partitura = partituras_existentes[INDICE_PARTITURA]

    PATH = partitura.path_img_original
    NOMBRE_IMAGEN = get_nombre_fichero(PATH)

    img = pygame.image.load(PATH)

    if partitura.resized:
        # Crea una nueva imagen con el nuevo tamaño
        img = cv.imread(PATH)
        img = resize_image(partitura.fraccion, img)
        cv.imwrite(complete_path + "app/pygame_funcs/imagen_resized.png", img)
        PATH = complete_path + "app/pygame_funcs/imagen_resized.png"
        img = pygame.image.load(complete_path+"app/pygame_funcs/imagen_resized.png")
        

    w, h = img.get_size()
    rect = img.get_rect()

    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption(partitura.nombre)

    clock = pygame.time.Clock()

    img = actualizar_partitura(partitura, PATH, complete_path, ORDEN_SOSTENIDOS_ARMADURA, ORDEN_BEMOLES_ARMADURA, SIMBOLOS_ALTERACIONES)
    
    if len(partitura.notas) == 0:
        limpiar(complete_path, partitura.resized)
        raise ErrorPentagramas("No se han encontrado notas")

    i:int = 0  # Índice de la nota en la lita de notas de la partitura
    while running:

        clock.tick(60)/1000.0
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
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    cambio = pop.open_popup(partitura, i)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    partitura.borrar_nota(i)
                    cambio = True
                    cambio_posicion = True
                elif event.key == pygame.K_ESCAPE:
                    running = False
            if cambio_posicion:
                # Comprueba que el índice esté en el rango de la lista
                if i >= len(partitura.notas):
                    i = 0
                elif i < 0:
                    i = len(partitura.notas) - 1
                
            if cambio:  # Actualiza la partitura
                img = actualizar_partitura(partitura, PATH, complete_path, ORDEN_SOSTENIDOS_ARMADURA, ORDEN_BEMOLES_ARMADURA, SIMBOLOS_ALTERACIONES)

        screen.fill(GRAY)
        screen.blit(img, rect)

        try:
            posiciones = partitura.notas[i].rectangulo
        except IndexError:
            limpiar(complete_path, partitura.resized)
            raise ErrorPentagramas("Se han eliminado todas las notas")

        pygame.draw.rect(screen, RED, pygame.Rect(posiciones[2] - 5,posiciones[0] - 5,posiciones[3] - posiciones[2] + 10,posiciones[1] - posiciones[0] + 10), 2)

        pygame.display.update()


    partitura.img_path = complete_path + "app/pygame_funcs/imagenes_editadas/" + NOMBRE_IMAGEN

    pygame.image.save(img, partitura.img_path)

    limpiar(complete_path, partitura.resized)

    with open(complete_path + "app/notas_partituras/partituras_guardadas.obj", "wb") as fh:
        partituras_existentes[:-1].append(partitura)
        partituras_existentes = partituras_existentes[:INDICE_PARTITURA] + [partitura] + partituras_existentes[INDICE_PARTITURA + 1:]
        pickle.dump(partituras_existentes, fh)
    return True