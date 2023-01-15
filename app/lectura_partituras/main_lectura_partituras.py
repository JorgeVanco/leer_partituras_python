import cv2 as cv
from lectura_partituras.functions.file_browser import file_browser
from lectura_partituras.functions.encontrar_pentagramas import encontrar_pentagramas
from lectura_partituras.functions.recorrer_pentagrama import recorrer_pentagrama
from lectura_partituras.functions.diferenciar_figuras import diferenciar_figuras
import lectura_partituras.functions.functions as f
from pygame_funcs.main_edicion_partituras import main_edicion_partituras
from Classes.Errors import ImageNotSelected, ErrorPentagramas, ErrorPath
from Classes.Ajustes import Ajustes
from Classes.Notas import Partitura
import pickle
import os

def guardar_partitura_analizada(partitura:Partitura) -> None:
    """
    Guarda todo lo obtenido por el análisis en ficheros de bytes

    Args:
        notas (list): La lista de notas
        corte_pentagramas (list[tuple]): lista con la posición inicial y final para cada corte en la imagen
        path (str) : La ruta a la imagen de la partitura elegida
        resized (bool): Si la partitura ha sido cambiada de tamaño o no
        fraccion (float): La fracción con la que ha sido cambiada de tamaño
    """
    complete_path = f.find_complete_path(__file__)
    try:
        with open(complete_path + "app/notas_partituras/notas_pruebas.obj", "wb") as fh:
            pickle.dump(partitura.notas, fh)
    except FileNotFoundError:
        os.mkdir(complete_path + "app/notas_partituras")
        with open(complete_path + "app/notas_partituras/notas_pruebas.obj", "wb") as fh:
            pickle.dump(partitura.notas, fh)


    with open(complete_path + "app/pygame_funcs/partes_imagenes.obj", "wb") as fh:
        pickle.dump(partitura, fh)

def main_lectura_partituras() -> bool:
    """
    La lógica de la lectura de partituras.

    Se pide al usuario elegir una imagen.
    Se analiza la partitura y se guardan los resultados.
    Se llama a la edición de la partitura.

    Returns:
        True: Para que el programa continue
    """
    # Se abre un menú para elegir la imagen
    try:
        path = file_browser()
        
        if path:
            img = cv.imread(path)
        else:
            img = None
        if img is None:
            raise ImageNotSelected("Could not read the image.")
    except cv.error:
        raise ImageNotSelected("No image selected")
    except ErrorPath as e:
        raise ErrorPath(e)

    
    # Se cambia la imagen a blanco y negro
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Se cargan los ajustes
    AJUSTES:Ajustes = f.get_ajustes()

    # Busca los pentagramas en la imagen
    pentagramas, corte_pentagramas, distancia, grosor = encontrar_pentagramas(
        img, AJUSTES.UMBRAL_NEGRO, AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS)

    # Cambia el tamaño de la partitura para que sea del mejor tamaño posible para hacer el análisis
    resized = False
    fraccion = 1
    if AJUSTES.CAMBIAR_SIZE and pentagramas and pentagramas[0][-1] - pentagramas[0][0] != AJUSTES.SIZE_PENTAGRAMA_IDEAL:
        fraccion = AJUSTES.SIZE_PENTAGRAMA_IDEAL / (pentagramas[0][-1] - pentagramas[0][0])

        img = f.resize_image(fraccion, img)
        img = f.limpiar_img(AJUSTES.UMBRAL_NEGRO, img)
        pentagramas, corte_pentagramas, distancia, grosor = encontrar_pentagramas(
            img, AJUSTES.UMBRAL_NEGRO, AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS)
        resized = True

    if not pentagramas:
        raise ErrorPentagramas("No se han encontrado pentagramas, compruebe los ajustes")

    notas: list = []
    for index_pentagrama in range(len(corte_pentagramas)):
        
        imagen_para_recorrer, desfase = f.calcular_imagen_a_recorrer_y_desfase(img, pentagramas,index_pentagrama, corte_pentagramas, distancia)
        
        figuras_en_pentagrama = recorrer_pentagrama(imagen_para_recorrer, distancia, AJUSTES.UMBRAL_NEGRO, grosor, pentagramas[index_pentagrama], AJUSTES.DETECTAR_CORCHEAS, AJUSTES.PORCENTAJE_DETECTAR_NOTA)
        
        for figura, posiciones, posiciones_rectangulo in figuras_en_pentagrama:
            
            # Sumar desfase por distinto pentagrama
            posiciones = f.sumar_desfase(posiciones, desfase)
            posiciones_rectangulo = f.sumar_desfase(posiciones_rectangulo, desfase)
            
            nota = diferenciar_figuras(
                figura, posiciones, posiciones_rectangulo, pentagramas[index_pentagrama], distancia, AJUSTES.UMBRAL_NEGRO, AJUSTES.PORCENTAJE_DIFERENCIAR_NEGRA_BLANCA)
            notas.append(nota)

    NOMBRE_IMAGEN = f.get_nombre_fichero(path)
    NOMBRE_PARTITURA = NOMBRE_IMAGEN[:NOMBRE_IMAGEN.find(".")]
    partitura:Partitura = Partitura(corte_pentagramas, notas, NOMBRE_PARTITURA, path, resized, fraccion)
    guardar_partitura_analizada(partitura)

    
    main_edicion_partituras()


    return True