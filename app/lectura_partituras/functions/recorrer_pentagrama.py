
def asignar_aumento_minimo(lado:int, AUMENTO_MINIMO_ARRIBA_ABAJO:int, AUMENTO_MINIMO_LATERALES:int) -> int:
    if lado <= 1:
        AUMENTO_MINIMO = AUMENTO_MINIMO_ARRIBA_ABAJO
    else:
        AUMENTO_MINIMO = AUMENTO_MINIMO_LATERALES
    return AUMENTO_MINIMO

def agrandar_lado(posiciones_cuadrado:list[int], suma_actual:int, UMBRAL_NEGRO:int, pentagrama:list[list[int]], AUMENTO_MINIMO:int, AUMENTO_MINIMO_LATERALES:int, lado:int, posiciones_rectangulo:list = None, fijado_cuadrado:bool = False) -> tuple[list[int], list[int], int]:
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
    if not posiciones_rectangulo:
        posiciones_rectangulo:list = posiciones_cuadrado.copy()

    agrandar_lado:bool = True
    while agrandar_lado:
        posiciones_rectangulo[lado] -= cantidad_a_sumar
        nuevo_cuadrado = pentagrama[posiciones_rectangulo[0] : posiciones_rectangulo[1], posiciones_rectangulo[2] : posiciones_rectangulo[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()

        if not fijado_cuadrado and suma_nueva - suma_actual < AUMENTO_MINIMO_LATERALES:
            posiciones_cuadrado = posiciones_rectangulo.copy()
            posiciones_cuadrado[lado] += cantidad_a_sumar
            fijado_cuadrado = True
        
        if suma_nueva - suma_actual < AUMENTO_MINIMO:
            agrandar_lado = False
            posiciones_rectangulo[lado] += cantidad_a_sumar
            
        suma_actual = suma_nueva
    return posiciones_cuadrado, posiciones_rectangulo, suma_actual

def agrandar_cuadrado(pentagrama:list[list[int]], posiciones_cuadrado:list[int], UMBRAL_NEGRO:int, GROSOR:int, AUMENTO_MINIMO_LATERALES:int, AUMENTO_MINIMO_ARRIBA_ABAJO:int, posiciones_pentagrama:list, partitura_fina:bool, DETECTAR_CORCHEAS:bool) -> tuple[list[int], list[int]]:
    cuadrado:list[list[int]] = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
    suma_actual:int = (cuadrado < UMBRAL_NEGRO).sum()
    # AUMENTO_MINIMO_LATERALES = GROSOR * (posiciones_cuadrado[1] - posiciones_cuadrado[0]) // (posiciones_pentagrama[-1] - posiciones_pentagrama[0]//5) * 7//4
    # Se agrandan todos los lados, va del 3 al 0 porque si se agranda primero arriba y abajo se supera siempre el AUMENTO_MINIMO
    AUMENTO_MINIMO:int = AUMENTO_MINIMO_LATERALES
    for lado in range(3, -1, -1):

        if lado == 1:
            AUMENTO_MINIMO = AUMENTO_MINIMO_ARRIBA_ABAJO
        posiciones_cuadrado, posiciones_rectangulo, suma_actual = agrandar_lado(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, AUMENTO_MINIMO, AUMENTO_MINIMO_LATERALES, lado)

    if not partitura_fina and DETECTAR_CORCHEAS:#and not posiciones_cuadrado[-1] - posiciones_cuadrado[0] > 0.8*(posiciones_pentagrama[-1] - posiciones_pentagrama[0]):
        AUMENTO_MINIMO_LATERALES = GROSOR * (posiciones_rectangulo[1] - posiciones_rectangulo[0]) // ((posiciones_pentagrama[-1] - posiciones_pentagrama[0] )/ 5) 
        
        posiciones_cuadrado, posiciones_rectangulo, suma_actual = agrandar_lado(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, AUMENTO_MINIMO_LATERALES, AUMENTO_MINIMO_LATERALES, 3, posiciones_rectangulo, fijado_cuadrado= True)
        posiciones_cuadrado, posiciones_rectangulo, suma_actual = agrandar_lado(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama, AUMENTO_MINIMO_LATERALES, AUMENTO_MINIMO_LATERALES, 2, posiciones_rectangulo, fijado_cuadrado= True)

    return posiciones_cuadrado, posiciones_rectangulo


def recorrer_pentagrama(pentagrama:list, distancia:int, UMBRAL_NEGRO:int, GROSOR:int, posiciones_pentagrama:list[int,int], partitura_fina:bool, DETECTAR_CORCHEAS: bool) -> list[tuple]:
    '''
    Recorre cada pentagrama verticalmente y horizontalmente
    
    Args: 
        pentagrama (list)
        distancia (int): Distancia entre dos líneas del pentagrama
        UMBRAL_NEGRO (int)

    Returns: figuras_en_pentagrama (dict): figuras del pentagrama
    '''
    
    posicion_horizontal:int = 0
    step:int = distancia * 4//3

    figuras_en_pentagrama = []

    if GROSOR <= 2:
        GROSOR = 2

    if partitura_fina:
        UMBRAL_NEGRO = 1
    
    AUMENTO_MINIMO_LATERALES:int = GROSOR * 6//4  #(posiciones_pentagrama[-1] - posiciones_pentagrama[0]//5) // (posiciones_cuadrado[1] - posiciones_cuadrado[0]) #grosor * 2
    AUMENTO_MINIMO_ARRIBA_ABAJO:int = GROSOR*3//5

    while posicion_horizontal < len(pentagrama[0]):  # Recorre el pentagrama horizontalmente
        posicion_vertical = 0
        while posicion_vertical < len(pentagrama):  # Recorre el pentagrama verticalmente

            cuadrado = pentagrama[posicion_vertical:posicion_vertical + distancia, posicion_horizontal:posicion_horizontal + step]
            
            if len(cuadrado) == distancia and (cuadrado < UMBRAL_NEGRO).sum() > 0.4*(cuadrado <= 255).sum(): 
                posiciones = [posicion_vertical, posicion_vertical + distancia, posicion_horizontal,posicion_horizontal + step]
                posiciones_nuevas, posciiones_rectangulo = agrandar_cuadrado(pentagrama, posiciones, UMBRAL_NEGRO, GROSOR, AUMENTO_MINIMO_LATERALES, AUMENTO_MINIMO_ARRIBA_ABAJO, posiciones_pentagrama, partitura_fina, DETECTAR_CORCHEAS)  
                cuadrado = pentagrama[posiciones_nuevas[0] : posiciones_nuevas[1], posiciones_nuevas[2]: posiciones_nuevas[3]]
                posicion_vertical = len(pentagrama)
                posicion_horizontal = posiciones_nuevas[3]
                figuras_en_pentagrama.append((cuadrado, posiciones_nuevas, posciiones_rectangulo)) # tupla con el cuadrado y sus posiciones

            posicion_vertical += distancia//2  # Es la mitad porque tiene que recorrer
        posicion_horizontal += step
    return figuras_en_pentagrama