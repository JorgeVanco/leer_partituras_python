from Classes.Notas import Nota

def get_distancia(punto_medio:int, row:int) -> int:
    """
    Calcula la distancia desde el punto medio de la figura a la fila

    Args: 
        punto_medio (int): El punto medio del cuadrado que contiene a la figura
        row (int): La fila en la que nos encontramos, es la fila de la línea del pentagrama
    
    Returns:
        La distancia entre el punto medio y la fila (int)
    """
    return abs(row - punto_medio)


def encontrar_menor_distancia(punto_medio:float, rows_pentagrama:list[int]) -> tuple[int]:
    """
    Encuentra la menor distancia desde el punto medio a una de las líneas del pentagrama o el punto medio entre ellas

    Args:
        punto_medio (float): El punto medio del cuadrado que contiene a la figura
        rows_pentagrama (list): Lista con las posiciones de las líneas del pentagrama
    
    Returns:
        menor_distancia (int): La menor distancia entre el punto medio y una de las líneas del pentagrama o el punto medio entre ellas
        row_menor_distancia (int): La fila del pentagrama a la cual más cerca se encuentra el punto
    """
    menor_distancia:int = None
    row_menor_distancia:int = 0
    index_row:int = 1
    while index_row < 10:  # un pentagrama tiene 5 lineas, no queremos llegar hasta la última con el bucle. Va de arriba a abajo

        # impares para las lineas del pentagrama, para para el medio
        if index_row % 2 == 1:
            # coge las lineas del pentagrama por orden
            punto_actual_del_pentagrama = rows_pentagrama[index_row - (
                index_row + 1)//2]

        else:
            # coge el punto medio entre las lineas del pentagrama
            punto_actual_del_pentagrama = rows_pentagrama[index_row // 2 - 1] + (
                rows_pentagrama[index_row // 2] - rows_pentagrama[index_row // 2 - 1]) // 2

        distancia_punto_medio_actual = get_distancia(
            punto_medio, punto_actual_del_pentagrama)

        if menor_distancia != None and distancia_punto_medio_actual > menor_distancia:
            index_row = 11
        else:
            menor_distancia = distancia_punto_medio_actual
            row_menor_distancia = index_row
            index_row += 1
    return menor_distancia, row_menor_distancia


# medir las distancias a las distintas filas(con el la mitad entre ellas tambien)
def encontrar_posicion_en_pentagrama(punto_medio:float, rows_pentagrama:int, distancia:int) -> int:
    """
    Encuentra la posición de la nota en el pentagrama

    Args:
        punto_medio (float): El punto medio del cuadrado que contiene a la figura
        rows_pentagrama (list): Lista con las posiciones de las líneas del pentagrama
        distancia (int): La distancia entre las líneas del pentagrama

    Returns:
        row_menor_distancia (int): La fila del pentagrama a la cual más cerca se encuentra el punto
    """
    menor_distancia, row_menor_distancia = encontrar_menor_distancia(
        punto_medio, rows_pentagrama)
    # ver si es mayor la distancia que la (distancia entre pentagramas) /2 para saber la nota adecuada si sale por encima o por debajo del pentagrama
    if menor_distancia >= distancia / 4:
        if row_menor_distancia == 1:
            row_menor_distancia -= menor_distancia // (distancia / 2)
        elif row_menor_distancia == 9:
            row_menor_distancia += menor_distancia // (distancia / 2)
    return row_menor_distancia

def diferenciar_blanca_redonda(posiciones_cuadrado:list[int], posiciones_rectangulo:list[int]) -> str:
    """
    Diferencia entre blanca y redonda

    Args:
        posiciones_cuadrado (list): Las posiciones del cuadrado que contiene a la nota
        posiciones_rectangulo (list): Las posiciones del rectángulo que contiene a la nota y al cuadrado

    Returns:
        "redonda" si es redonda
        "blanca" si es blanca
    """
    is_blanca = abs(posiciones_rectangulo[1] - posiciones_rectangulo[0]) > 1.5*abs(posiciones_cuadrado[1] - posiciones_cuadrado[0])
    if is_blanca:
        return "blanca"
    return "redonda"

def diferenciar_entre_figuras_negras(posiciones_cuadrado:list[int], posiciones_rectangulo:list[int]) -> str:
    """
    Diferencia entre negra y corchea

    Args:
        posiciones_cuadrado (list): Las posiciones del cuadrado que contiene a la nota
        posiciones_rectangulo (list): Las posiciones del rectángulo que contiene a la nota y al cuadrado

    Returns:
        "negra" si es negra
        "corchea" si es corchea
    """
    if posiciones_cuadrado[3] - posiciones_cuadrado[2] < posiciones_rectangulo[3] - posiciones_rectangulo[2]:
        return "corchea"
    return "negra"

def encontrar_longitud_nota(figura:list, UMBRAL_NEGRO:int, posiciones_cuadrado:list[int], posiciones_rectangulo:list[int]) -> str:
    """
    Encuentra qué tipo de figura es (blanca, negra, redonda, corchea)

    Args:
        figura (list): La figura que hay que estudiar
        UMBRAL_NEGRO (int): Valor a partir del cual un pixel se puede considerar negro (0 - 255)
        posiciones_cuadrado (list): Las posiciones del cuadrado que contiene a la nota
        posiciones_rectangulo (list): Las posiciones del rectángulo que contiene a la nota y al cuadrado

    Returns:
        figura (str): La figura que es
    """
    pixeles = len(figura) * len(figura[0])
    numero_pixeles_negros = (figura < UMBRAL_NEGRO).sum()
    porcentaje = numero_pixeles_negros / pixeles
    is_negra:bool = porcentaje > 0.65
    figura  = "negra"

    if is_negra:
        figura = diferenciar_entre_figuras_negras(posiciones_cuadrado, posiciones_rectangulo)
    else:
        figura = diferenciar_blanca_redonda(posiciones_cuadrado, posiciones_rectangulo)

    return figura


def get_octava(index_row_pentagrama: int) -> int:
    """
    Encuentra que octava es para poder usarla en la fórmula para tocar las notas

    Args:
        index_row_pentagrama (int): índice en la lista que contiene las posiciones de las filas del pentagrama

    Returns:
        octava (int): la octava que hay que introducir en la fórmula para que suene adecuadamente
    """
    octava_alta = 11 - index_row_pentagrama >= 7
    octava_baja = 11 - index_row_pentagrama < 0

    if octava_alta:
        octava = 4
    elif octava_baja:
        octava = 2
    else:
        octava = 3

    return octava

def diferenciar_figuras(figura:list, posiciones_cuadrado:list, posiciones_rectangulo:list, rows_pentagrama:list, distancia:int, UMBRAL_NEGRO:int) -> Nota:
    """
    Estudia la nota del pentagrama

    Args:
        figura (list): La figura que hay que estudiar
        posiciones_cuadrado (list): Las posiciones del cuadrado que contiene a la nota
        posiciones_rectangulo (list): Las posiciones del rectángulo que contiene a la nota y al cuadrado
        rows_pentagrama (list): Lista con las posiciones de las líneas del pentagrama
        distancia (int): La distancia entre las líneas del pentagrama
        UMBRAL_NEGRO (int): Valor a partir del cual un pixel se puede considerar negro (0 - 255)
    
    Returns:
        Nota (Nota): Objeto de la nota que se ha estudiado con todas sus características
    """
    NOTAS_MUSICALES = {0: "Do", 1: "Re", 2: "Mi", 
                        3: "Fa", 4: "Sol", 5: "La", 6: "Si"}

    # punto inferior menos punto superior entre 2
    altura:int = posiciones_cuadrado[1] - posiciones_cuadrado[0]
    altura_pentagrama:int = rows_pentagrama[-1] - rows_pentagrama[0]
    if  altura >= altura_pentagrama:
        # se quita las claves de sol, el tiempo, las lineas verticales
        if posiciones_cuadrado[3] - posiciones_cuadrado[2] > 1/3 * altura:
            return Nota("clave de sol", 0, posiciones_rectangulo)
        return Nota("otra figura", 0, posiciones_rectangulo)

    elif altura >= 0.5 * (altura_pentagrama):
        return Nota("silencio", 0, posiciones_rectangulo)

    punto_medio:float = posiciones_cuadrado[0] + (posiciones_cuadrado[1] - posiciones_cuadrado[0]) / 2

    index_row_pentagrama = encontrar_posicion_en_pentagrama(
        punto_medio, rows_pentagrama, distancia)

    octava = get_octava(index_row_pentagrama)

    
    figura:str = encontrar_longitud_nota(figura, UMBRAL_NEGRO, posiciones_cuadrado, posiciones_rectangulo)
    return Nota(NOTAS_MUSICALES[(11-index_row_pentagrama) % 7], octava, posiciones_rectangulo, figura)