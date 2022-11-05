def get_distancia_entre_lineas(distancias):   # devuelve la distancia más común entre las líneas
    conteo_distancias = {}
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

def lista_pentagramas(lineas, distancia):
    """
    Argumentos 
    
    """

    pentagramas = []
    pentagrama = []
    for linea in lineas:

        if len(pentagramas) > 0 and len(pentagrama) == 0:  # si ya hay algún pentagrama y estamos empezando otro nuevo, se coge la última línea
            ultima_linea_pentagramas = pentagramas[-1][-1]

        else: ultima_linea_pentagramas = linea - distancia   # si no, se coge esa línea menos la distancia

        if len(pentagrama) == 0 and linea - ultima_linea_pentagramas >= distancia:  # si es la primera línea del pentagrama y la diferencia coon la última línea es mayor o igual que la distancia
            pentagrama.append(linea)   #se añade la línea al pentagrama

        elif 0 < len(pentagrama) < 5:   # 
            if linea - pentagrama[len(pentagrama) -1] in range(distancia - 3, distancia + 5): #tiene que tener algo de margen porque no siempre son los mismos pixeles
                pentagrama.append(linea)

                if len(pentagrama) == 5:
                    pentagramas.append(pentagrama)
                    pentagrama = []
                    
    return pentagramas


def get_corte_pentagramas(pentagramas, length_img):
    corte_pentagramas = []
    if len(pentagramas) <= 1:
        corte_pentagramas.append((0, length_img - 1))
    else:
        for i in range(len(pentagramas)):
            if i == 0:
                corte_pentagramas.append((0, pentagramas[i][4] + (pentagramas[i + 1][0] - pentagramas[i][4]) // 2))
            elif i == len(pentagramas) - 1:
                corte_pentagramas.append((pentagramas[i -1][4] + (pentagramas[i][0] - pentagramas[i -1][4]) // 2, length_img - 1))
            else:
                corte_pentagramas.append((pentagramas[i -1][4] + (pentagramas[i][0] - pentagramas[i -1][4]) // 2, pentagramas[i][4] + (pentagramas[i + 1][0] - pentagramas[i][4]) // 2))
    return corte_pentagramas


def encontrar_pentagramas(img, UMBRAL_NEGRO, FRACCION_MINIMA_PIXELES_NEGROS):
    distancia_linea_a_linea = 0
    distancias = []
    lineas = []
    
    for row in range(len(img)):
        index_pixel = 0
        found_black_pixel = False
        # como mi condicion para que sea linea de pentagrama es que 3/4 de la fila sean pixeles negros, 
        # solo busco algún pixel negro hasta 1/4 de la fila
        while not found_black_pixel and index_pixel < len(img[row])*(1 - FRACCION_MINIMA_PIXELES_NEGROS):  
            if img[row][index_pixel] < UMBRAL_NEGRO:
                found_black_pixel = True
            index_pixel += 1

        #condition = [pixel < UMBRAL_NEGRO for pixel in img[row]]
        if found_black_pixel:#any(condition):  # pixeles negros en la fila

            count = 0
            for i in range(len(img[row])):
                if img[row][i] < UMBRAL_NEGRO:
                    count += 1
            if count > len(img[row]) * FRACCION_MINIMA_PIXELES_NEGROS:
                if len(lineas) > 0:
                    distancia_linea_a_linea = row - lineas[len(lineas) - 1]
                    distancias.append(distancia_linea_a_linea)
                lineas.append(row)

    # comprobar si se ha acabado el pentagrama mirado las distancias 
    # más comunes y mayores que 1(a veces puede coger dos lineas seguidas)
    
    distancia = get_distancia_entre_lineas(distancias)

    pentagramas = lista_pentagramas(lineas, distancia)

    corte_pentagramas = get_corte_pentagramas(pentagramas, len(img))

    return pentagramas, corte_pentagramas, distancia