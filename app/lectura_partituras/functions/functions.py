import cv2 as cv
import numpy as np

def calcular_imagen_a_recorrer_y_desfase(img:list, pentagramas:list, index_pentagrama:int, corte_pentagramas:list, distancia:int) -> tuple[list, int]:
    """
    Determina la imagen del pentagrama a partir de las posiciones de los pentagramas

    Args:
        img (list): Imagen de la partitura
        pentagramas (list): 

    Returns:
        imagen_para_recorrer (list): La imagen del pentagrama para ser recorrida
        desfase (int): El desfase que hay que sumar a las posiciones de las notas para que aparezcan
                    adecuadamente, es la posición de la primera línea del pentagrama
    """
    if pentagramas[index_pentagrama][0] - corte_pentagramas[index_pentagrama][0] > 6 * distancia:
        imagen_para_recorrer = img[pentagramas[index_pentagrama]
                                [0] - 6*distancia: corte_pentagramas[index_pentagrama][-1]]
        desfase = pentagramas[index_pentagrama][0] - 6*distancia
    else:
        imagen_para_recorrer = img[corte_pentagramas[index_pentagrama]
                                [0]: corte_pentagramas[index_pentagrama][-1]]
        desfase = corte_pentagramas[index_pentagrama][0]
    return imagen_para_recorrer, desfase

def sumar_desfase(posiciones:list[int], desfase:int) -> list:
    """
    Suma un desfase a las posiciones de los cuadrados para que aparezcan en el pentagrama correspondiente

    Args:
        posiciones (list): Las posiciones del cuadrado
        desfase (int): El desfase que hay que sumar
    
    Returns:
        posiciones (list): Las posiciones del cuadrado tras haber sumado el desfase
    """
    posiciones[0] = desfase + posiciones[0]
    posiciones[1] = desfase + posiciones[1]
    return posiciones

def resize_image(fraccion:float, img:list) -> list:
    """
    Cambia el tamaño de la imagen multiplicando sus dimensiones por la fracción

    Args:
        fraccion (float): La fracción por la que multiplicar las dimensiones de la imagen
        img (list): La imagen que hay que redimensionar

    Returns:
        img (list): La imagen redimensionada
    """
    print("Resizing...")
    w, h = img.shape[:2]
    # fraccion = 1
    print(w, h, end=" -> ")
    w = int(np.round(fraccion * w))
    h = int(np.round(fraccion * h))
    print(w, h)
    return cv.resize(img, (h, w))

def find_complete_path() -> str:
    """
    Encuentra la ruta absoluta del directorio Lectura_partituras_python para poder ejecutar el programa desde cualquier lugar

    Returns:
        file_path (str): La ruta
    """
    file_path = __file__.replace("\\", "/")
    index = file_path.find("app")
    return file_path[:index]


def get_nombre_fichero(PATH:str) -> str:
    """
    Consigue el nombre del fichero a partir de su ruta

    Args:
        PATH (str): La ruta del fichero
    
    Returns:
        name (str): El nombre del fichero con su extensión
    """
    name:str = ""
    i:int = len(PATH) - 1
    letra:str = PATH[i]
    while letra != "/" and i >= 0:
        name = letra + name
        i -= 1
        letra = PATH[i]

    return name

def limpiar_img(UMBRAL_NEGRO:int, img:list) -> list:
    """
    Convierte todos los pixeles de la imagen a blanco o negro a partir del umbral

    Args:
        UMBRAL_NEGRO (int): Valor a partir del cual un pixel se puede considerar negro (0 - 255)
        img (list): La imagen en blanco y negro, con tonos de grises
    
    Returns:
        img (list): La imagen en blanco y negro, sin tonos de grises
    """
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i,j] < UMBRAL_NEGRO:
                img[i,j] = 0
            else:
                img[i,j] = 255
    return img