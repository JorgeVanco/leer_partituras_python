import cv2 as cv
import numpy as np

def calcular_imagen_a_recorrer_y_desfase(img:list, pentagramas:list, index_pentagrama:int, corte_pentagramas:list, distancia:int) -> tuple[list, int]:
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
    posiciones[0] = desfase + posiciones[0]
    posiciones[1] = desfase + posiciones[1]
    return posiciones

def create_start_end_points(posiciones:list[int]):
    start_point: tuple[int] = (posiciones[2], posiciones[0])
    end_point: tuple[int] = (posiciones[3], posiciones[1])

    return start_point, end_point

def resize_image(fraccion:float, img:list):
    w, h = img.shape[:2]
    print(fraccion)
    # fraccion = 1
    print(w, h, end=" -> ")
    w = int(np.round(fraccion * w))
    h = int(np.round(fraccion * h))
    print(w, h)
    return cv.resize(img, (h, w))

def find_complete_path():
    file_path = __file__.replace("\\", "/")
    index = file_path.find("app")
    return file_path[:index]