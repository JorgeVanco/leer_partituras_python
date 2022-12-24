
def agrandar_lado(posiciones_cuadrado:list[int], suma_actual:int, UMBRAL_NEGRO:int, pentagrama:list[list[int]], AUMENTO_MINIMO:int, lado:int) -> tuple[list[int], int]:
    """
    Agranda un lado del cuadrado de la figura hasta que el número de píxeles negros que aumentan no superan el umbral de AUMENTO_MINIMO

    Args:
        posiciones_cuadrado (list[int]): Las posiciones de los lados de arriba, abajo, izquierda, derecha del cuadrado en el pentagrama
        suma_actual (int): La cantidad de pixeles negros en el cuadrado actualmente
        UMBRAL_NEGRO (int): Valor a partir del cual un pixel se puede considerar negro (0 - 255)
        pentagrama (list): Lista con los valores de todos los pixeles
        AUMENTO_MINIMO (int): El número de píxeles que como mínimo se tiene que aumentar para seguir aumentando el lado del cuadrado
        lado (int): El lado que se quiere aumentar
                    0 -> Arriba
                    1 -> Abajo
                    2 -> Izquierda
                    3 -> Derecha
    """

    cantidad_a_sumar:int = (-1)**lado

    agrandar_lado:bool = True
    while agrandar_lado:
        posiciones_cuadrado[lado] -= cantidad_a_sumar
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < AUMENTO_MINIMO:
            agrandar_lado = False
            posiciones_cuadrado[lado] += cantidad_a_sumar
        suma_actual = suma_nueva
    return posiciones_cuadrado, suma_actual

def agrandar_cuadrado(pentagrama:list[list[int]], posiciones_cuadrado:list[int], UMBRAL_NEGRO:int) -> list[int]:
    AUMENTO_MINIMO:int = 3
    cuadrado:list[list[int]] = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
    suma_actual:int = (cuadrado < UMBRAL_NEGRO).sum()

    # Se agrandan todos los lados, va del 3 al 0 porque si se agranda primero arriba y abajo se supera siempre el AUMENTO_MINIMO
    for lado in range(3,-1, -1):
        posiciones_cuadrado, suma_actual = agrandar_lado(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, AUMENTO_MINIMO, lado)

    return posiciones_cuadrado


def recorrer_pentagrama(pentagrama, distancia:int, UMBRAL_NEGRO:int):
    '''
    Recorre cada pentagrama verticalmente y horizontalmente
    
    Args: pentagrama (list)
        distancia (int): Distancia entre dos líneas del pentagrama
        UMBRAL_NEGRO (int)

    Returns: figuras_en_pentagrama (dict): figuras del pentagrama

    '''

    # cv.imshow(str(pentagrama), pentagrama)
    
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