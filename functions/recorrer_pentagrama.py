import cv2 as cv

def agrandar_derecha(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, AUMENTO_MINIMO):

    agrandar_derecha = True
    while agrandar_derecha:
        posiciones_cuadrado[3] += 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < AUMENTO_MINIMO:
            agrandar_derecha = False
            posiciones_cuadrado[3] -= 1
        suma_actual = suma_nueva
    return posiciones_cuadrado

def agrandar_izquierda(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO:int, pentagrama, AUMENTO_MINIMO):

    agrandar_izquierda = True
    while agrandar_izquierda:
        posiciones_cuadrado[2] -= 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < AUMENTO_MINIMO:
            agrandar_izquierda = False
            posiciones_cuadrado[2] += 1
        suma_actual = suma_nueva
    return posiciones_cuadrado

def agrandar_arriba(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO:int, pentagrama, AUMENTO_MINIMO):

    agrandar_arriba:bool = True
    while agrandar_arriba:
        posiciones_cuadrado[0] -= 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < AUMENTO_MINIMO:
            agrandar_arriba = False
            posiciones_cuadrado[0] += 1
        suma_actual = suma_nueva
    return posiciones_cuadrado

def agrandar_abajo(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO:int, pentagrama, AUMENTO_MINIMO):

    agrandar_abajo:bool = True
    while agrandar_abajo:
        posiciones_cuadrado[1] += 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < AUMENTO_MINIMO:
            agrandar_abajo = False
            posiciones_cuadrado[1] -= 1
        suma_actual = suma_nueva
    return posiciones_cuadrado


def agrandar_cuadrado(pentagrama, posiciones_cuadrado, UMBRAL_NEGRO:int):
    AUMENTO_MINIMO:int = 3
    cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
    suma_actual:int = (cuadrado < UMBRAL_NEGRO).sum()

    posiciones_cuadrado = agrandar_derecha(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, AUMENTO_MINIMO)
    posiciones_cuadrado = agrandar_izquierda(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, AUMENTO_MINIMO)
    posiciones_cuadrado = agrandar_arriba(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, AUMENTO_MINIMO)
    posiciones_cuadrado = agrandar_abajo(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, AUMENTO_MINIMO)
    return posiciones_cuadrado


def recorrer_pentagrama(pentagrama, distancia:int, UMBRAL_NEGRO:int):
    '''
    Recorre cada pentagrama verticalmente y horizontalmente
    
    Args: pentagrama (list)
        distancia (int): Distancia entre dos líneas del pentagrama
        UMBRAL_NEGRO (int)

    Returns: figuras_en_pentagrama (dict): figuras del pentagrama

    '''

    cv.imshow(str(pentagrama), pentagrama)
    
    posicion_horizontal:int = 0
    step:int = distancia * 4//3

    figuras_en_pentagrama = []

    while posicion_horizontal < len(pentagrama[0]):
        posicion_vertical = 0
        while posicion_vertical < len(pentagrama):

            cuadrado = pentagrama[posicion_vertical:posicion_vertical + distancia, posicion_horizontal:posicion_horizontal + step]
            
            if (cuadrado < UMBRAL_NEGRO).sum() > 0.5*(cuadrado <= 255).sum(): 
                posiciones = [posicion_vertical, posicion_vertical + distancia, posicion_horizontal,posicion_horizontal + step]
                posiciones_nuevas = agrandar_cuadrado(pentagrama, posiciones, UMBRAL_NEGRO)
                cuadrado = pentagrama[posiciones_nuevas[0] : posiciones_nuevas[1], posiciones_nuevas[2]: posiciones_nuevas[3]]
                posicion_vertical = len(pentagrama)
                posicion_horizontal = posiciones_nuevas[3]
                figuras_en_pentagrama.append((cuadrado, posiciones_nuevas)) # tupla con el cuadrado y sus posiciones

            posicion_vertical += distancia//2  # Es la mitad porque tiene que recorrer
        posicion_horizontal += step
    return figuras_en_pentagrama