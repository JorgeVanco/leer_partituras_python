import cv2 as cv
from functions.file_browser import file_browser
from functions.encontrar_pentagramas import encontrar_pentagramas
from functions.recorrer_pentagrama import recorrer_pentagrama
from functions.diferenciar_figuras import diferenciar_figuras


if __name__ == "__main__":
    # Se abre un menú para elegir la imagen
    path = file_browser()
    img = cv.imread(path)

    if img is None:
        print("Could not read the image.")
    h,w = img.shape[:2]
    #img = cv.resize(img, (w*2, h*2))

    color_img = img
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # img = cv.resize(img, tuple([i * 5 for i in img.shape[:2]]))
    # PARAMETROS
    UMBRAL_NEGRO:int = 200  # considero negro cualquier valor menor que 140
    FRACCION_MINIMA_PIXELES_NEGROS:float = 3/4
    notas:list = []
    str_notas:str = ""
    pentagramas, corte_pentagramas, distancia, grosor = encontrar_pentagramas(
        img, UMBRAL_NEGRO, FRACCION_MINIMA_PIXELES_NEGROS)
    image_rectangulos = img
    PUNTOS_MEDIO = []
    for index_pentagrama in range(len(corte_pentagramas)):
        figuras_en_pentagrama = recorrer_pentagrama(
            img[corte_pentagramas[index_pentagrama][0]: corte_pentagramas[index_pentagrama][-1]], distancia, UMBRAL_NEGRO, grosor)
    
        count = 0
        for figura, posiciones, posiciones_rectangulo in figuras_en_pentagrama:

            #Sumar desfase por distinto pentagrama
            posiciones[0] = corte_pentagramas[index_pentagrama][0] + posiciones[0]
            posiciones[1] = corte_pentagramas[index_pentagrama][0] + posiciones[1]

            posiciones_rectangulo[0] = corte_pentagramas[index_pentagrama][0] + posiciones_rectangulo[0]
            posiciones_rectangulo[1] = corte_pentagramas[index_pentagrama][0] + posiciones_rectangulo[1]



            start_point:tuple[int] = (posiciones[2], posiciones[0])
            end_point:tuple[int] = (posiciones[3], posiciones[1])

            start_point_rectangulo:tuple[int] = (posiciones_rectangulo[2], posiciones_rectangulo[0])
            end_point_rectangulo:tuple[int] = (posiciones_rectangulo[3], posiciones_rectangulo[1])

            color:tuple[int] = 0
            thickness:int = 1
            image_rectangulos = cv.rectangle(image_rectangulos, start_point, end_point, color, thickness)
            image_rectangulos = cv.rectangle(image_rectangulos, start_point_rectangulo, end_point_rectangulo, color, thickness)
            nota = diferenciar_figuras(
                figura, posiciones, pentagramas[index_pentagrama], distancia)  # pentagramas
            notas.append(nota)
            punto_medio = posiciones[0] + (posiciones[1] - posiciones[0]) // 2
            PUNTOS_MEDIO.append(( posiciones[2], punto_medio))
            str_notas += nota["nota"] + " "
            org = (posiciones[2] + (abs(posiciones[3] - posiciones[2])) // 2, corte_pentagramas[index_pentagrama][-1] - 20*(count%2)-5)
            if nota["nota"] != "otra figura":
                image_rectangulos = cv.putText(image_rectangulos, nota["nota"], org, cv.FONT_HERSHEY_SIMPLEX, 0.35, 0, 1, cv.LINE_AA)
            count += 1
        start_point = (0, pentagramas[index_pentagrama][0])
        end_point = (len(img[0]), pentagramas[index_pentagrama][-1])
        image_rectangulos = cv.rectangle(image_rectangulos, start_point, end_point, color, thickness)

    for pent in pentagramas:
        for coord in pent:
            color_img = cv.circle(color_img, (len(img[0]) - 80, coord), 2, (0,0,255),-1)  


    for point in PUNTOS_MEDIO:
        color_img = cv.circle(color_img, point, 2, (0,0,255),-1)  
    color_img = cv.resize(color_img, (w,h))
    
    cv.imshow("COLOR", color_img)



    # mejor guardarlo en un json
    # (h, w) = image_rectangulos.shape[:2]
    # percentage = 960 / w
    # if h* percentage >= 1080:
    #     percentage = 1
    # image_rectangulos = cv.resize(image_rectangulos, (int(960),int(h*percentage)))
    image_rectangulos = cv.resize(image_rectangulos, (w,h))
    cv.imshow("jafdsf", image_rectangulos)
    with open(f"./notas_partituras/notas_pruebas.txt", "w") as fh:
        fh.write(str(notas))
        fh.write(str_notas)

    k = cv.waitKey(0)


# escribir nombre figuras en imagenes
#intentar analizar las figuras a la vez que las voy buscando
# clave de sol, silencios,... por altura y anchura
# agrandar hasta < 3 -> en funcion del grosor de la linea del pentagrama