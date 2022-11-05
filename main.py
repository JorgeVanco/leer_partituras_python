import cv2 as cv
from functions.file_browser import file_browser
from functions.encontrar_pentagramas import encontrar_pentagramas
from functions.recorrer_pentagrama import recorrer_pentagrama

# Se abre un menú para elegir la imagen
path = file_browser()
img = cv.imread(path)


if img is None:
    print("Could not read the image.")
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

##PARAMETROS
UMBRAL_NEGRO  = 200  #considero negro cualquier valor menor que 140
FRACCION_MINIMA_PIXELES_NEGROS = 3/4
pentagramas, corte_pentagramas, distancia = encontrar_pentagramas(img, UMBRAL_NEGRO, FRACCION_MINIMA_PIXELES_NEGROS)
for pentagrama in corte_pentagramas:
    print(pentagrama)
    figuras_en_pentagrama = recorrer_pentagrama(img[pentagrama[0]: pentagrama[-1]], distancia, UMBRAL_NEGRO)
k = cv.waitKey(0)