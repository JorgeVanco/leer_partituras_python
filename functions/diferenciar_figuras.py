import cv2 as cv

def get_distancia(punto_medio, row):
    return abs(row - punto_medio)

def encontrar_menor_distancia(punto_medio, rows_pentagrama):
    menor_distancia = None
    row_menor_distancia = 0
    index_row = 1
    while index_row < 10: # un pentagrama tiene 5 lineas, no queremos llegar hasta la última con el bucle. Va de arriba a abajo
        
        #impares para las lineas del pentagrama, para para el medio
        if index_row % 2 == 1:
            punto_actual_del_pentagrama = rows_pentagrama[index_row - (index_row + 1)//2] # coge las lineas del pentagrama por orden
            
        else:
            punto_actual_del_pentagrama = rows_pentagrama[index_row // 2 - 1] + (rows_pentagrama[index_row // 2] - rows_pentagrama[index_row // 2 - 1]) // 2 # coge el punto medio entre las lineas del pentagrama
        
        distancia_punto_medio_actual = get_distancia(punto_medio, punto_actual_del_pentagrama)

        if menor_distancia and distancia_punto_medio_actual > menor_distancia:
            index_row = 11
        else:
            menor_distancia = distancia_punto_medio_actual
            row_menor_distancia = index_row
            index_row += 1
    return menor_distancia, row_menor_distancia
    

def encontrar_posicion_en_pentagrama(punto_medio, rows_pentagrama, distancia): # medir las distancias a las distintas filas(con el la mitad entre ellas tambien)
    menor_distancia, row_menor_distancia = encontrar_menor_distancia(punto_medio, rows_pentagrama)

    #ver si es mayor la distancia que la (distancia entre pentagramas) /2 para saber la nota adecuada si sale por encima o por debajo del pentagrama
    if menor_distancia >= distancia / 2 - distancia/4:
        if row_menor_distancia == 1:
            row_menor_distancia -= menor_distancia // (distancia / 2)
        elif row_menor_distancia == 9:
            row_menor_distancia += menor_distancia // (distancia / 2)
    return row_menor_distancia
    numero_nota_musical = 0


        
def diferenciar_figuras(figura, posiciones, rows_pentagrama, distancia):
    
    notas_musicales = {0: "Do", 1: "Re", 2: "Mi", 3: "Fa", 4: "Sol", 5: "La", 6: "Si"}

    punto_medio = posiciones[0] + (posiciones[1] - posiciones[0]) / 2 # punto inferior menos punto superior entre 2
    
    index_row_pentagrama = encontrar_posicion_en_pentagrama(punto_medio, rows_pentagrama, distancia)
    octava_alta = 11 - index_row_pentagrama >= 7
    octava_baja = 11 - index_row_pentagrama < 0
    cv.imshow(notas_musicales[(11-index_row_pentagrama) % 7] + " "+str(posiciones), figura)
    return {"nota": notas_musicales[(11-index_row_pentagrama) % 7],
            "octava_alta": octava_alta,
            "octava_baja": octava_baja}