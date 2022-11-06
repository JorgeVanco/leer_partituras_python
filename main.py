import cv2 as cv
from functions.file_browser import file_browser
from functions.encontrar_pentagramas import encontrar_pentagramas
from functions.recorrer_pentagrama import recorrer_pentagrama
from functions.diferenciar_figuras import diferenciar_figuras

# Se abre un menú para elegir la imagen
path = file_browser()
img = cv.imread(path)


if img is None:
    print("Could not read the image.")
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

##PARAMETROS
UMBRAL_NEGRO  = 200  #considero negro cualquier valor menor que 140
FRACCION_MINIMA_PIXELES_NEGROS = 3/4
notas = []
pentagramas, corte_pentagramas, distancia = encontrar_pentagramas(img, UMBRAL_NEGRO, FRACCION_MINIMA_PIXELES_NEGROS)
for index_pentagrama in range(len(corte_pentagramas)):
    figuras_en_pentagrama = recorrer_pentagrama(img[corte_pentagramas[index_pentagrama][0]: corte_pentagramas[index_pentagrama][-1]], distancia, UMBRAL_NEGRO)
    for figura, posiciones in figuras_en_pentagrama:
        nota = diferenciar_figuras(figura, posiciones, pentagramas[index_pentagrama], distancia)
        notas.append(nota)

with open(f"./notas_partituras/notas_pruebas.txt", "w") as fh:
    fh.write(str(notas))
k = cv.waitKey(0)