import cv2 as cv

def agrandar_derecha(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, aumento_minimo):

    agrandar_derecha = True
    while agrandar_derecha:
        posiciones_cuadrado[3] += 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < aumento_minimo:
            agrandar_derecha = False
            posiciones_cuadrado[3] -= 1
        suma_actual = suma_nueva
    return posiciones_cuadrado

def agrandar_izquierda(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, aumento_minimo):

    agrandar_izquierda = True
    while agrandar_izquierda:
        posiciones_cuadrado[2] -= 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < aumento_minimo:
            agrandar_izquierda = False
            posiciones_cuadrado[2] += 1
        suma_actual = suma_nueva
    return posiciones_cuadrado

def agrandar_arriba(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, aumento_minimo):

    agrandar_arriba = True
    while agrandar_arriba:
        posiciones_cuadrado[0] -= 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < aumento_minimo:
            agrandar_arriba = False
            posiciones_cuadrado[0] += 1
        suma_actual = suma_nueva
    return posiciones_cuadrado

def agrandar_abajo(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, aumento_minimo):

    agrandar_abajo = True
    while agrandar_abajo:
        posiciones_cuadrado[1] += 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < aumento_minimo:
            agrandar_abajo = False
            posiciones_cuadrado[1] -= 1
        suma_actual = suma_nueva
    return posiciones_cuadrado


def agrandar_cuadrado(pentagrama, posiciones_cuadrado, UMBRAL_NEGRO):
    aumento_minimo = 3
    cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
    suma_actual = (cuadrado < UMBRAL_NEGRO).sum()

    posiciones_cuadrado = agrandar_derecha(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, aumento_minimo)
    posiciones_cuadrado = agrandar_izquierda(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, aumento_minimo)
    posiciones_cuadrado = agrandar_arriba(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, aumento_minimo)
    posiciones_cuadrado = agrandar_abajo(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, aumento_minimo)
    return posiciones_cuadrado


def recorrer_pentagrama(pentagrama, distancia, UMBRAL_NEGRO):
    # recorrer cada pentagrama verticalmente y horizontalmente
    kernel_size = distancia

    cv.imshow(str(pentagrama), pentagrama)
    cv.waitKey(0)
    
    posicion_horizontal = 0
    step = kernel_size * 4//3

    figuras_en_pentagrama = []

    while posicion_horizontal < len(pentagrama[0]):
        posicion_vertical = 0
        while posicion_vertical < len(pentagrama):

            cuadrado = pentagrama[posicion_vertical:posicion_vertical + kernel_size, posicion_horizontal:posicion_horizontal + step]
            
            if (cuadrado < UMBRAL_NEGRO).sum() > 0.5*(cuadrado <= 255).sum(): 
                posiciones = [posicion_vertical, posicion_vertical + kernel_size, posicion_horizontal,posicion_horizontal + step]
                posiciones_nuevas = agrandar_cuadrado(pentagrama, posiciones, UMBRAL_NEGRO)
                cuadrado = pentagrama[posiciones_nuevas[0] : posiciones_nuevas[1], posiciones_nuevas[2]: posiciones_nuevas[3]]
                posicion_vertical = len(pentagrama)
                posicion_horizontal = posiciones_nuevas[3]
                figuras_en_pentagrama.append((cuadrado, posiciones_nuevas)) # tupla con el cuadrado y sus posiciones

            posicion_vertical += kernel_size//2  # Es la mitad porque tiene que recorrer
        posicion_horizontal += step
    return figuras_en_pentagrama