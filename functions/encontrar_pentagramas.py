def get_distancia_entre_lineas(distancias: list):
    '''
    Busca la distancia entre las líneas más común

    Args: distancias (list): Lista de todas las distancias entre las listas

    Returns: distancia (int)

    '''
    conteo_distancias: dict = {}
    for distancia in distancias:
        if distancia > 1:
            if distancia not in conteo_distancias:
                conteo_distancias[distancia] = 0

            conteo_distancias[distancia] += 1

    if conteo_distancias:
        frecuencias_distancias = list(conteo_distancias.values())
        frecuencia_distancia_mas_comun = max(frecuencias_distancias)

        for cada_distancia in conteo_distancias:
            if conteo_distancias[cada_distancia] == frecuencia_distancia_mas_comun:
                distancia = cada_distancia

    return distancia


def lista_pentagramas(lineas:list, distancia:int):
    """
    Agrupa todas las líneas por pentagramas

    Args:
        lineas (list): lista con todas las posiciones de las lineas de la imagen
        distancia (int): distancia más común entre todas las líneas

    Returns:
        pentagrams (list): Lista de tuplas que contienen las cinco líneas de cada pentagrama
    """

    pentagramas: list = []
    pentagrama: list = []
    for linea in lineas:

        # si ya hay algún pentagrama y estamos empezando otro nuevo, se coge la última línea
        if len(pentagramas) > 0 and len(pentagrama) == 0:
            ultima_linea_pentagramas = pentagramas[-1][-1]

        else:
            # si no, se coge esa línea menos la distancia
            ultima_linea_pentagramas = linea - distancia

        # si es la primera línea del pentagrama y la diferencia coon la última línea es mayor o igual que la distancia
        if len(pentagrama) == 0 and linea - ultima_linea_pentagramas >= distancia:
            pentagrama.append(linea)  # se añade la línea al pentagrama

        elif 0 < len(pentagrama) < 5:   #
            # tiene que tener algo de margen porque no siempre son los mismos pixeles
            if linea - pentagrama[len(pentagrama) - 1] in range(distancia - 3, distancia + 5):
                pentagrama.append(linea)

                if len(pentagrama) == 5:
                    pentagramas.append(pentagrama)
                    pentagrama = []

    return pentagramas


def get_corte_pentagramas(pentagramas: list, length_img: int):
    """
    Crea unos cortes en la imagen que contienen a un pentagrama cada uno.
    Cada corte se encuentra en la mitad entre dos pentagramas

    Args:
        pentagramas (list): Lista con las posiciones iniciales y finales de las filas de los pentagramas
        length_img (int): la lognitud de la imagen, es decir, la longitud de la lista que contiene las 
                    filas de la imagen

    Returns:
        corte_pentagramas (list[tuple]): lista con la posición inicial y final para cada corte en la imagen
    """
    corte_pentagramas: list[tuple] = []
    if len(pentagramas) <= 1:
        corte_pentagramas.append((0, length_img - 1))
    else:
        for i in range(len(pentagramas)):
            if i == 0:
                corte_pentagramas.append(
                    (0, pentagramas[i][4] + (pentagramas[i + 1][0] - pentagramas[i][4]) // 2))
            elif i == len(pentagramas) - 1:
                corte_pentagramas.append(
                    (pentagramas[i - 1][4] + (pentagramas[i][0] - pentagramas[i - 1][4]) // 2, length_img - 1))
            else:
                corte_pentagramas.append((pentagramas[i - 1][4] + (pentagramas[i][0] - pentagramas[i - 1][4]) //
                                         2, pentagramas[i][4] + (pentagramas[i + 1][0] - pentagramas[i][4]) // 2))
    return corte_pentagramas


def buscar_pixel_negro_en_fila(row: list, UMBRAL_NEGRO: int, FRACCION_MINIMA_PIXELES_NEGROS: float):
    """
    Busca el primer pixel negro de la fila.
    Si no encuentra uno pasado la fracción mínima de píxeles negros requeridos, devuelve False

    Args:
        row (list): la fila de la imagen
        UMBRAL_NEGRO (int): Valor a partir del cual un pixel se puede considerar negro (0 - 255)
        FRACCION_MINIMA_PIXELES_NEGROS (float): Es la cantidad mínima respecto la longitud de la fila que 
                es necesaria para poder considerar una fila como una línea del pentagrama

    Returns: 
        index_pixel (int): índice del primer pixel negro encontrado en la fila
        found_black_pixel (bool): Si un pixel negro ha sido encontrado o no
    """
    # como mi condicion para que sea linea de pentagrama es que 3/4 de la fila sean pixeles negros,
    # solo busco algún pixel negro hasta 1/4 de la fila

    index_pixel: int = 0
    found_black_pixel: bool = False
    while not found_black_pixel and index_pixel < len(row)*(1 - FRACCION_MINIMA_PIXELES_NEGROS):
        if row[index_pixel] < UMBRAL_NEGRO:
            found_black_pixel = True
        index_pixel += 1

    return index_pixel, found_black_pixel


def contar_pixeles_negros_en_fila(start: int, row: list, UMBRAL_NEGRO: int) -> int:
    """
    Cuenta los píxemes negros que hay en una fila

    Args:
        start (int): el punto desde donde se debe empezar a contar
        row (list): la fila de la imagen de la cual queremos contar los pixeles negros
        UMBRAL_NEGRO (int): Valor a partir del cual un pixel se puede considerar negro (0 - 255)

    Returns:
        count (int): La cuenta de los pixeles negros que se encuentran en la fila
    """
    count: int = 0
    for i in range(start, len(row)):
        if row[i] < UMBRAL_NEGRO:
            count += 1
    return count


def encontrar_pentagramas(img: list, UMBRAL_NEGRO: int, FRACCION_MINIMA_PIXELES_NEGROS: float):
    '''
    Args: 
        img (list): imagen a procesar
        UMBRAL_NEGRO (int): Valor a partir del cual un pixel se puede considerar negro (0 - 255)
        FRACCION_MINIMA_PIXELES_NEGROS (float): Es la proporción mínima de píxeles negros que 
                        debe tener una fila de la imagen para ser considerada línea de pentagrama

    Returns: 
            pentagramas (lista): contiene las listas de las posiciones de las líneas de cada pentagrama
            corte_pentagrama (lista): lista de tuplas con jel inicio y el fin de las secciones de la imagen
                        que contienen un pentagrama. (desde la mitad del espacio entre dos pentagramas)
            distancia (int): distancia entre dos líneas de pentagrama
    '''

    distancia_linea_a_linea: int = 0
    distancias: list = []
    lineas: list = []

    for row in range(len(img)):

        index_pixel, found_black_pixel: bool = buscar_pixel_negro_en_fila(img[row], UMBRAL_NEGRO, FRACCION_MINIMA_PIXELES_NEGROS)

        if found_black_pixel:
            count = contar_pixeles_negros_en_fila(
                index_pixel, img[row], UMBRAL_NEGRO)

            if count > len(img[row]) * FRACCION_MINIMA_PIXELES_NEGROS:
                if len(lineas) > 0:
                    distancia_linea_a_linea = row - lineas[len(lineas) - 1]
                    distancias.append(distancia_linea_a_linea)
                lineas.append(row)

    # comprobar si se ha acabado el pentagrama mirado las distancias
    # más comunes y mayores que 1(a veces puede coger dos lineas seguidas)

    distancia: int = get_distancia_entre_lineas(distancias)

    pentagramas: list = lista_pentagramas(lineas, distancia)

    corte_pentagramas = get_corte_pentagramas(pentagramas, len(img))

    return pentagramas, corte_pentagramas, distancia
