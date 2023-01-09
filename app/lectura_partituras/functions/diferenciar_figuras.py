# from recorrer_pentagrama import agrandar_lado
# Estas 3 lineas son para que funciones el import
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from Classes.Notas import Nota

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

        if menor_distancia != None and distancia_punto_medio_actual > menor_distancia:
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
    if menor_distancia >= distancia / 4:
        if row_menor_distancia == 1:
            row_menor_distancia -= menor_distancia // (distancia / 2)
        elif row_menor_distancia == 9:
            row_menor_distancia += menor_distancia // (distancia / 2)
    return row_menor_distancia

def diferenciar_blanca_redonda(posiciones_cuadrado:list[int], posiciones_rectangulo:list[int]) -> str:
    is_blanca = abs(posiciones_rectangulo[1] - posiciones_rectangulo[0]) > 1.5*abs(posiciones_cuadrado[1] - posiciones_cuadrado[0])
    if is_blanca:
        return "blanca"
    return "redonda"

def diferenciar_entre_figuras_negras(posiciones_cuadrado:list[int], posiciones_rectangulo:list[int], pentagrama:list, numero_pixeles_negros:int, UMBRAL_NEGRO):
    if posiciones_cuadrado[3] - posiciones_cuadrado[2] < posiciones_rectangulo[3] - posiciones_rectangulo[2]:
        return "corchea"
    # agrandar_lado(posiciones_rectangulo, numero_pixeles_negros, UMBRAL_NEGRO, pentagrama)
    return "negra"

def encontrar_longitud_nota(figura, centro:tuple[int,int], UMBRAL_NEGRO:int, posiciones_cuadrado:list[int], posiciones_rectangulo:list[int], pentagrama:list) -> str:

    pixeles = len(figura) * len(figura[0])
    numero_pixeles_negros = (figura < UMBRAL_NEGRO).sum()
    porcentaje = numero_pixeles_negros / pixeles
    is_negra:bool = porcentaje > 0.65
    figura  = "negra"

    if is_negra:
        figura = diferenciar_entre_figuras_negras(posiciones_cuadrado, posiciones_rectangulo, pentagrama, numero_pixeles_negros, UMBRAL_NEGRO)
    else:
        figura = diferenciar_blanca_redonda(posiciones_cuadrado, posiciones_rectangulo)

    return figura


def get_octava(index_row_pentagrama: int):
    octava_alta = 11 - index_row_pentagrama >= 7
    octava_baja = 11 - index_row_pentagrama < 0

    if octava_alta:
        octava = 4
    elif octava_baja:
        octava = 2
    else:
        octava = 3

    return octava

def diferenciar_figuras(figura, posiciones_cuadrado, posiciones_rectangulo, rows_pentagrama, distancia, UMBRAL_NEGRO:int, pentagrama:list) -> Nota:

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

    punto_medio_y_figura:int = len(figura) // 2
    punto_medio_x_figura:int = len(figura[0]) // 2

    index_row_pentagrama = encontrar_posicion_en_pentagrama(
        punto_medio, rows_pentagrama, distancia)

    octava = get_octava(index_row_pentagrama)

    
    figura:str = encontrar_longitud_nota(figura, (punto_medio_x_figura,punto_medio_y_figura), UMBRAL_NEGRO, posiciones_cuadrado, posiciones_rectangulo, pentagrama)
    return Nota(NOTAS_MUSICALES[(11-index_row_pentagrama) % 7], octava, posiciones_rectangulo, figura)