import cv2 as cv
import numpy as np

def agrandar_derecha(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama):

    agrandar_derecha = True
    while agrandar_derecha:
        posiciones_cuadrado[3] += 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < 3:
            agrandar_derecha = False
            posiciones_cuadrado[3] -= 1
        suma_actual = suma_nueva
    return posiciones_cuadrado

def agrandar_izquierda(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama):

    agrandar_izquierda = True
    while agrandar_izquierda:
        posiciones_cuadrado[2] -= 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < 3:
            agrandar_izquierda = False
            posiciones_cuadrado[2] += 1
        suma_actual = suma_nueva
    return posiciones_cuadrado

def agrandar_arriba(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama):

    agrandar_arriba = True
    while agrandar_arriba:
        posiciones_cuadrado[0] -= 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < 3:
            agrandar_arriba = False
            posiciones_cuadrado[0] += 1
        suma_actual = suma_nueva
    return posiciones_cuadrado

def agrandar_abajo(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama):

    agrandar_abajo = True
    while agrandar_abajo:
        posiciones_cuadrado[1] += 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < 3:
            agrandar_abajo = False
            posiciones_cuadrado[1] -= 1
        suma_actual = suma_nueva
    return posiciones_cuadrado


def agrandar_cuadrado(pentagrama, posiciones_cuadrado, UMBRAL_NEGRO):

    cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
    suma_actual = (cuadrado < UMBRAL_NEGRO).sum()

    posiciones_cuadrado = agrandar_derecha(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama)
    posiciones_cuadrado = agrandar_izquierda(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama)
    posiciones_cuadrado = agrandar_arriba(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama)
    posiciones_cuadrado = agrandar_abajo(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama)
    return posiciones_cuadrado


def recorrer_pentagrama(pentagrama, distancia, UMBRAL_NEGRO):
    # recorrer cada pentagrama verticalmente y horizontalmente
    kernel_size = distancia
    trozo_vertical = []
    show= True
    cv.imshow(str(pentagrama), pentagrama)

    # cv.imshow(str(pentagrama), cuadrado)
    cv.waitKey(0)
    
    posicion_horizontal = 0
    step = kernel_size * 4//3

    while posicion_horizontal < len(pentagrama[0]):
        posicion_vertical = 0
        while posicion_vertical < len(pentagrama):
            kernel = []
            
            fragmento_horizontal_kernel = []
            cuadrado = pentagrama[posicion_vertical:posicion_vertical + kernel_size, posicion_horizontal:posicion_horizontal + step]
            #cuadrado = np.asarray(cuadrado, dtype=np.uint8)
            
            if (cuadrado < UMBRAL_NEGRO).sum() > 0.5*(cuadrado <= 255).sum():#(cuadrado >= UMBRAL_NEGRO).sum():  
                posiciones = [posicion_vertical, posicion_vertical + kernel_size, posicion_horizontal,posicion_horizontal + step]
                posiciones_nuevas = agrandar_cuadrado(pentagrama, posiciones, UMBRAL_NEGRO)
                cuadrado = pentagrama[posiciones_nuevas[0] : posiciones_nuevas[1], posiciones_nuevas[2]: posiciones_nuevas[3]]
                cv.imshow("AGRANDADo cuadrado"+str(posicion_vertical) + str(posicion_horizontal), cuadrado)
                posicion_vertical = len(pentagrama)
                posicion_horizontal = posiciones_nuevas[3]

            posicion_vertical += kernel_size//2  # Es la mitad porque tiene que recorrer
        posicion_horizontal += step
    cv.waitKey(0)
    return #np.asarray(trozo_vertical, dtype=np.uint8)