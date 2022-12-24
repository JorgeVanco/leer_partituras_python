import cv2 as cv


def get_distancia(punto_medio:int, row:int) -> int:
    """
    Calcula la distancia desde el punto medio de la figura a la fila

    Args: 
        punto_medio (int): El punto medio de la figura
        row (int): La fila en la que nos encontramos, es la fila de la línea del pentagrama
    
    Returns:
        La distancia entre el punto medio y la fila (int)
    """
    return abs(row - punto_medio)


def encontrar_menor_distancia(punto_medio:int, rows_pentagrama:int) -> tuple[int]:
    """
    
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

        if menor_distancia and distancia_punto_medio_actual > menor_distancia:
            index_row = 11
        else:
            menor_distancia = distancia_punto_medio_actual
            row_menor_distancia = index_row
            index_row += 1
    return menor_distancia, row_menor_distancia


# medir las distancias a las distintas filas(con el la mitad entre ellas tambien)
def encontrar_posicion_en_pentagrama(punto_medio:float, rows_pentagrama:int, distancia:int) -> int:
    menor_distancia, row_menor_distancia = encontrar_menor_distancia(
        punto_medio, rows_pentagrama)

    # ver si es mayor la distancia que la (distancia entre pentagramas) /2 para saber la nota adecuada si sale por encima o por debajo del pentagrama
    if menor_distancia >= distancia / 2 - distancia/4:
        if row_menor_distancia == 1:
            row_menor_distancia -= menor_distancia // (distancia / 2)
        elif row_menor_distancia == 9:
            row_menor_distancia += menor_distancia // (distancia / 2)
    return row_menor_distancia


def diferenciar_figuras(figura, posiciones, rows_pentagrama, distancia) -> dict:

    NOTAS_MUSICALES = {0: "Do", 1: "Re", 2: "Mi", 
                        3: "Fa", 4: "Sol", 5: "La", 6: "Si"}

    # punto inferior menos punto superior entre 2
    altura:int = posiciones[1] - posiciones[0]
    altura_pentagrama:int = rows_pentagrama[-1] - rows_pentagrama[0]
    if  altura >= altura_pentagrama:
        # se quita las claves de sol, el tiempo, las lineas verticales
        if posiciones[3] - posiciones[2] > 1/3 * altura:
            # cv.imshow("clave de sol"+str(posiciones), figura)
            print("Clave de SOl", posiciones)
            cv.waitKey(0)
            return {"nota" : "clave de sol"}   # habria que diferencia entre clave de sol, de fa, ...

        return {"nota" : "otra figura"} 
    elif altura >= 0.5 * (altura_pentagrama):
        print("Posible silencio")
        # cv.imshow("silencio" + " "+str(posiciones), figura)

        return {"nota" : "silencio"}
    punto_medio = posiciones[0] + (posiciones[1] - posiciones[0]) / 2

    index_row_pentagrama = encontrar_posicion_en_pentagrama(
        punto_medio, rows_pentagrama, distancia)
    octava_alta = 11 - index_row_pentagrama >= 7
    octava_baja = 11 - index_row_pentagrama < 0
    # cv.imshow(NOTAS_MUSICALES[(11-index_row_pentagrama) %
    #         7] + " "+str(posiciones), figura)
    print(NOTAS_MUSICALES[(11-index_row_pentagrama) % 7])
    return {"nota": NOTAS_MUSICALES[(11-index_row_pentagrama) % 7],
            "octava_alta": octava_alta,
            "octava_baja": octava_baja}
