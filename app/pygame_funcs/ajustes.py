import pygame
import pygame_menu
from Classes.Ajustes import Ajustes
import pickle
import numpy as np
import os
from lectura_partituras.functions.functions import find_complete_path, get_ajustes


def set_corcheas(value, boolean, AJUSTES):
    AJUSTES.DETECTAR_CORCHEAS = boolean


def set_resize(value, boolean, AJUSTES):
    AJUSTES.CAMBIAR_SIZE = boolean


def set_umbral(value, AJUSTES):
    AJUSTES.UMBRAL_NEGRO = int(value)


def set_porcentaje_detectar_nota(value, AJUSTES):
    AJUSTES.PORCENTAJE_DETECTAR_NOTA = np.round(value, 3)


def set_porcentaje_diferenciar_negra_blanca(value, AJUSTES:Ajustes):
    AJUSTES.PORCENTAJE_DIFERENCIAR_NEGRA_BLANCA = np.round(value, 3)


def set_fraccion(value, AJUSTES):
    AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS = np.round(value, 3)


def save(AJUSTES, AJUSTES_DEFAULT, menu, screen, complete_path):
    saved: bool = False
    while not saved:
        try:
            with open(complete_path + "app/ajustes/ajustes.obj", "wb") as fh:
                pickle.dump(AJUSTES, fh)
            saved = True
        except FileNotFoundError:
            os.mkdir(complete_path + "app/ajustes")

    draw_menu(menu, screen, AJUSTES, AJUSTES_DEFAULT, complete_path)


def quit(menu):
    menu.disable()


def return_to_default_settings(AJUSTES, AJUSTES_DEFAULT, menu, screen, complete_path):
    for attribute in AJUSTES.__dict__:
        setattr(AJUSTES, attribute, getattr(AJUSTES_DEFAULT, attribute))
    draw_menu(menu, screen, AJUSTES, AJUSTES_DEFAULT, complete_path)


def draw_menu(menu, screen, AJUSTES, AJUSTES_DEFAULT, complete_path):
    menu.clear()
    menu.add.range_slider("Porcentaje para detectar una nota: "+str(AJUSTES.PORCENTAJE_DETECTAR_NOTA), default=AJUSTES.PORCENTAJE_DETECTAR_NOTA,
                            range_values=(0, 1), increment=0.1, onchange=lambda value: set_porcentaje_detectar_nota(value, AJUSTES))
    menu.add.range_slider("Porcentaje para diferenciar negras de blancas: "+str(AJUSTES.PORCENTAJE_DIFERENCIAR_NEGRA_BLANCA), default=AJUSTES.PORCENTAJE_DIFERENCIAR_NEGRA_BLANCA,
                            range_values=(0, 1), increment=0.1, onchange=lambda value: set_porcentaje_diferenciar_negra_blanca(value, AJUSTES))
    menu.add.range_slider("Umbral negro: "+str(AJUSTES.UMBRAL_NEGRO), default=AJUSTES.UMBRAL_NEGRO,
                            range_values=(0, 255), increment=1, onchange=lambda value: set_umbral(value, AJUSTES, menu, screen))
    menu.add.range_slider("Fracción mínima pixeles negros: "+str(AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS) + " ",
                            default=AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS, range_values=(0, 1), increment=0.1, onchange=lambda value: set_fraccion(value, AJUSTES))
    menu.add.selector('Detectar corcheas :'+str(AJUSTES.DETECTAR_CORCHEAS),
                        [('No', False), ('Sí', True)], default=AJUSTES.DETECTAR_CORCHEAS, onchange=lambda value, boolean: set_corcheas(value, boolean, AJUSTES))
    menu.add.selector('Cambiar tamaño partitura :'+str(AJUSTES.CAMBIAR_SIZE),
                        [('No', False), ('Sí', True)], default=AJUSTES.CAMBIAR_SIZE, onchange=lambda value, boolean: set_resize(value, boolean, AJUSTES))
    menu.add.button("Default settings", lambda: return_to_default_settings(
        AJUSTES, AJUSTES_DEFAULT, menu, screen, complete_path))
    menu.add.button('Save', lambda: save(
        AJUSTES, AJUSTES_DEFAULT, menu, screen, complete_path))

    menu.add.button('Return', lambda: quit(menu))


def main_ajustes():

    complete_path: str = find_complete_path(__file__)

    w: int = 1024
    h: int = 768
    screen = pygame.display.set_mode((w, h))

    my_image = pygame_menu.baseimage.BaseImage(
        image_path=complete_path + "app/pygame_funcs/imagenes_menu/escenario.png")

    my_theme = pygame_menu.Theme(background_color=my_image,  # transparent background
                                    title_background_color=(20, 20, 20), widget_font=pygame_menu.font.FONT_OPEN_SANS_BOLD, widget_font_color=(255, 255, 255))

    AJUSTES_DEFAULT: Ajustes = Ajustes()
    AJUSTES: Ajustes = get_ajustes()

    menu = pygame_menu.Menu('Ajustes', w, h,
                            theme=my_theme)

    draw_menu(menu, screen, AJUSTES, AJUSTES_DEFAULT, complete_path)

    menu.mainloop(screen)

    return True
