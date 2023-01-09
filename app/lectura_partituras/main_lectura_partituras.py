import cv2 as cv
from lectura_partituras.functions.file_browser import file_browser
from lectura_partituras.functions.encontrar_pentagramas import encontrar_pentagramas
from lectura_partituras.functions.recorrer_pentagrama import recorrer_pentagrama
from lectura_partituras.functions.diferenciar_figuras import diferenciar_figuras
import lectura_partituras.functions.functions as f
from pygame_funcs.main_pygame import main_pygame
from Classes.Errors import ImageNotSelected, ErrorPentagramas

import pickle

def limpiar_img(UMBRAL_NEGRO, img):
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i,j] < UMBRAL_NEGRO:
                img[i,j] = 0
            else:
                img[i,j] = 255
    return img


def main_lectura_partituras():
    # Se abre un menú para elegir la imagen
    try:
        print("TRYING")
        path = file_browser()
        if path:
            img = cv.imread(path)
        else:
            img = None
        if img is None:
            raise ImageNotSelected("Could not read the image.")
    except cv.error:
        raise ImageNotSelected("No image selected")

    complete_path = f.find_complete_path()

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # img = cv.resize(img, tuple([i * 5 for i in img.shape[:2]]))
    # PARAMETROS

    try:
        with open(complete_path + "app/ajustes/ajustes.obj", "rb") as fh:
            AJUSTES = pickle.load(fh)
    except FileNotFoundError:
        raise FileNotFoundError()

    UMBRAL_NEGRO: int = AJUSTES.UMBRAL_NEGRO  # considero negro cualquier valor menor que 140
    FRACCION_MINIMA_PIXELES_NEGROS: float = AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS
    SIZE_PENTAGRAMA_IDEAL:int = AJUSTES.SIZE_PENTAGRAMA_IDEAL
    notas: list = []
    partitura_fina:bool = False

    pentagramas, corte_pentagramas, distancia, grosor = encontrar_pentagramas(
        img, UMBRAL_NEGRO, FRACCION_MINIMA_PIXELES_NEGROS)

    if not pentagramas:
        raise ErrorPentagramas("No se han encontrado pentagramas, compruebe los ajustes")

    resized = False
    fraccion = 1
    if AJUSTES.CAMBIAR_SIZE and pentagramas[0][-1] - pentagramas[0][0] != SIZE_PENTAGRAMA_IDEAL:
        fraccion = SIZE_PENTAGRAMA_IDEAL / (pentagramas[0][-1] - pentagramas[0][0])
        if fraccion > 1.5:
            partitura_fina = True

        img = f.resize_image(fraccion, img)
        img = limpiar_img(UMBRAL_NEGRO, img)
        pentagramas, corte_pentagramas, distancia, grosor = encontrar_pentagramas(
            img, UMBRAL_NEGRO, FRACCION_MINIMA_PIXELES_NEGROS)
        resized = True

    # image_rectangulos = img
    PUNTOS_MEDIO = []
    for index_pentagrama in range(len(corte_pentagramas)):

        imagen_para_recorrer, desfase = f.calcular_imagen_a_recorrer_y_desfase(img, pentagramas,index_pentagrama, corte_pentagramas, distancia)

        figuras_en_pentagrama = recorrer_pentagrama(imagen_para_recorrer, distancia, UMBRAL_NEGRO, grosor, pentagramas[index_pentagrama], partitura_fina, AJUSTES.DETECTAR_CORCHEAS)

        count = 0
        for figura, posiciones, posiciones_rectangulo in figuras_en_pentagrama:

            # Sumar desfase por distinto pentagrama
            posiciones = f.sumar_desfase(posiciones, desfase)
            posiciones_rectangulo = f.sumar_desfase(posiciones_rectangulo, desfase)

            nota = diferenciar_figuras(
                figura, posiciones, posiciones_rectangulo, pentagramas[index_pentagrama], distancia, UMBRAL_NEGRO, imagen_para_recorrer)  # pentagramas
            notas.append(nota)

            punto_medio = posiciones[0] + (posiciones[1] - posiciones[0]) // 2
            PUNTOS_MEDIO.append((posiciones[2], punto_medio))

            count += 1


    with open(complete_path + "app/notas_partituras/notas_pruebas.obj", "wb") as fh:
        pickle.dump(notas, fh)

    with open(complete_path + "app/pygame_funcs/partes_imagenes.obj", "wb") as fh:
        pickle.dump(notas, fh)
        pickle.dump(corte_pentagramas, fh)
        pickle.dump(path, fh)
        pickle.dump(resized, fh)
        pickle.dump(fraccion, fh)

    main_pygame()

    return True

# intentar analizar las figuras a la vez que las voy buscando
# clave de sol, silencios,... por altura y anchura
# Resizing