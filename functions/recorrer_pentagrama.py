import cv2 as cv
import numpy as np
def recorrer_pentagrama(pentagrama, distancia, UMBRAL_NEGRO):
    # recorrer cada pentagrama verticalmente y horizontalmente
    kernel_size = distancia
    trozo_vertical = []
    show= True
    cv.imshow(str(pentagrama), pentagrama)

    # cv.imshow(str(pentagrama), cuadrado)
    cv.waitKey(0)
    for posicion_horizontal in range(0, len(pentagrama[0]), kernel_size * 4//3):

        for posicion_vertical in range(0, len(pentagrama), kernel_size//2):
            kernel = []
            
            fragmento_horizontal_kernel = []
            cuadrado = pentagrama[posicion_vertical:posicion_vertical + kernel_size, posicion_horizontal:posicion_horizontal + kernel_size * 4//3]
            cuadrado = np.asarray(cuadrado, dtype=np.uint8)
            
            if (cuadrado < UMBRAL_NEGRO).sum() > 0.5*(cuadrado <= 255).sum():#(cuadrado >= UMBRAL_NEGRO).sum():  
                posiciones = [posicion_vertical, posicion_vertical + kernel_size, posicion_horizontal,posicion_horizontal + kernel_size * 4//3]
                cv.imshow("cuadrado"+str(posicion_vertical) + str(posicion_horizontal), cuadrado)
                #cuadrado = agrandar_cuadrado(pentagrama, posiciones, UMBRAL_NEGRO)
                cv.imshow("AGRANDADo cuadrado"+str(posicion_vertical) + str(posicion_horizontal), cuadrado)
                show = False
    cv.waitKey(0)
    return #np.asarray(trozo_vertical, dtype=np.uint8)

def agrandar_derecha(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama):
    agrandar_derecha = True
    while agrandar_derecha:
        posiciones_cuadrado[3] += 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < 3:
            agrandar_derecha = False
            posiciones_cuadrado[3] -= 1
    return posiciones_cuadrado

def agrandar_izquierda(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama):
    agrandar_izquierda = True
    while agrandar_izquierda:
        posiciones_cuadrado[2] -= 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < 3:
            agrandar_izquierda = False
            posiciones_cuadrado[2] += 1
    return posiciones_cuadrado

def agrandar_arriba(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama):
    agrandar_arriba = True
    while agrandar_arriba:
        posiciones_cuadrado[0] -= 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < 3:
            agrandar_arriba = False
            posiciones_cuadrado[0] += 1
    return posiciones_cuadrado

def agrandar_abajo(agrandar_abajo, posiciones_cuadrado, suma_actual, UMBRAL_NEGRO, pentagrama):
    agrandar_derecha = True
    while agrandar_abajo:
        posiciones_cuadrado[1] += 1
        nuevo_cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
        # comparar con cuadrado anterior y ver si es mayor
        suma_nueva = (nuevo_cuadrado < UMBRAL_NEGRO).sum()
        if suma_nueva - suma_actual < 3:
            agrandar_abajo = False
            posiciones_cuadrado[1] -= 1
    return posiciones_cuadrado


def agrandar_cuadrado(pentagrama, posiciones_cuadrado, UMBRAL_NEGRO):
    cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
    suma_anterior = (cuadrado < UMBRAL_NEGRO).sum()
    agrandar = {"agrandando": True, "agrandar_derecha": True, "agrandar_izquierda": True, "agrandar_arriba": True, "agrandar_abajo": True}
    
    suma_actual = (cuadrado < UMBRAL_NEGRO).sum()
    posiciones_cuadrado = agrandar_derecha(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO)
    posiciones_cuadrado = agrandar_izquierda(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO)
    posiciones_cuadrado = agrandar_arriba(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO)
    posiciones_cuadrado = agrandar_abajo(posiciones_cuadrado, suma_actual, UMBRAL_NEGRO)
    return pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]
            
    # agrandamos horizontalmente
    # while agrandar_horizontalmente:  
    #     posiciones_cuadrado[2] -= 1
    #     posiciones_cuadrado[3] += 1 
    #     cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2] - 1 : posiciones_cuadrado[3] + 1]
    #     suma = (cuadrado < UMBRAL_NEGRO).sum()
    #     if suma - suma_anterior < 4:
    #         agrandar_horizontalmente = False
    #         posiciones_cuadrado[2] += 1
    #         posiciones_cuadrado[3] -= 1
    # while agrandar_verticalmente:  
    #     posiciones_cuadrado[0] -= 1
    #     posiciones_cuadrado[1] += 1 
    #     cuadrado = pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2] - 1 : posiciones_cuadrado[3] + 1]
    #     suma = (cuadrado < UMBRAL_NEGRO).sum()
    #     if suma - suma_anterior < 4:
    #         agrandar_horizontalmente = False
    #         posiciones_cuadrado[0] += 1
    #         posiciones_cuadrado[1] -= 1

    return pentagrama[posiciones_cuadrado[0] : posiciones_cuadrado[1], posiciones_cuadrado[2]: posiciones_cuadrado[3]]

"""
img = cv.imread("C:/Users/jurko/OneDrive - Universidad Pontificia Comillas/Documentos/iMAT/1_2022-2023/Programacion/Proyecto programacion/Lectura partituras python/imagenes/250px-Quarter_note_run.png")
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
pentagrama = (0, 288)
pentagrama = [205, 212, 219, 226, 233]
pentagrama = img[pentagrama[0]: pentagrama[-1]]
#cuadrado = np.asarray([[0,0,0,0,0],[0,0,0,0,0],[0,255,255,255,0],[0,255,255,255,0],[0,255,255,255,0],[0,0,0,0,0],[0,255,255,255,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]], dtype=np.uint8)
cv.imshow(str(pentagrama), pentagrama)
#pentagrama[0,0] = 0
# cv.imshow(str(pentagrama), cuadrado)
cv.waitKey(0)
# parte_cuadrado = [cuadrado[2][1:], cuadrado[3][1:]]
# print(parte_cuadrado)
# cv.imshow("dijf", np.asarray(parte_cuadrado))
trozo = recorrer_pentagrama(pentagrama, 6, 200)
#cv.imshow(str("trozo"), trozo)
cuadrado = np.array([np.array([255, 255, 255,0,255,255],dtype=np.uint8), np.array([255, 255, 255,255,255,255],dtype=np.uint8), np.array([255, 255, 255,255,0,255],dtype=np.uint8), np.array([255, 255, 255,255,255,255],dtype=np.uint8), np.array([255, 255, 255,255,255,255],dtype=np.uint8), np.array([255, 255, 255,255,255,255],dtype=np.uint8)])
print((( cuadrado < 255).sum() ))
cv.waitKey(0)
"""