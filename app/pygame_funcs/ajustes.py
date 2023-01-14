import pygame
import pygame_menu
from Classes.Ajustes import Ajustes
import pickle
import numpy as np
import os
from lectura_partituras.functions.functions import find_complete_path, get_ajustes


def set_ajustes(value, ajuste:str, AJUSTES:Ajustes) -> None:
    """
    Asigna un nuevo valor al atributo del objeto de los ajustes

    Args:
        value (any): El nuevo valor
        ajuste (str): El nombre del atributo que se desea cambiar
        AJUSTES (Ajustes): El objeto de los ajustes
    """
    if ajuste == "detectar_corcheas":
        AJUSTES.DETECTAR_CORCHEAS = value
    elif ajuste == "cambiar_size":
        AJUSTES.CAMBIAR_SIZE = value
    elif ajuste == "umbral_negro":
        AJUSTES.UMBRAL_NEGRO = int(value)
    elif ajuste == "porcentaje_detectar_nota":
        AJUSTES.PORCENTAJE_DETECTAR_NOTA = float(np.round(value, 3))
    elif ajuste == "porcentaje_diferenciar_negra_blanca":
        AJUSTES.PORCENTAJE_DIFERENCIAR_NEGRA_BLANCA = float(np.round(value, 3))
    elif ajuste == "fraccion_minima_pixeles_negros":
        AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS = float(np.round(value, 3))
    elif ajuste == "tempo_partitura":
        AJUSTES.TEMPO_PARTITURA = int(value)

def save(AJUSTES:Ajustes, AJUSTES_DEFAULT:Ajustes, menu:pygame_menu.Menu, screen, complete_path:str) -> None:
    """
    Guarda los valores de los ajustes en un fichero de bytes

    Args:
        AJUSTES (Ajustes): El objeto de los ajustes
        AJUSTES_DEFAULT (Ajustes): El objeto de los ajustes con los valores predeterminados
        menu (pygame_menu.Menu): El objeto menu de pygame_menu
        screen: La pantalla de pygame
        complete_path (str): La ruta absoluta hasta el directorio app
    """
    saved: bool = False
    while not saved:
        try:
            with open(complete_path + "app/ajustes/ajustes.obj", "wb") as fh:
                pickle.dump(AJUSTES, fh)
            saved = True
        except FileNotFoundError:
            os.mkdir(complete_path + "app/ajustes")

    draw_menu(menu, screen, AJUSTES, AJUSTES_DEFAULT, complete_path)


def quit(menu:pygame_menu.Menu) -> None:
    """
    Cierra la ventana de ajustes

    Args:
        menu (pygame_menu.Menu): El objeto menu de pygame_menu
    """
    menu.disable()


def return_to_default_settings(AJUSTES:Ajustes, AJUSTES_DEFAULT:Ajustes, menu:pygame_menu.Menu, screen, complete_path:str) -> None:
    """
    Vuelve los valores de los ajustes a los valores por defecto

    Args:
        AJUSTES (Ajustes): El objeto de los ajustes
        AJUSTES_DEFAULT (Ajustes): El objeto de los ajustes con los valores predeterminados
        menu (pygame_menu.Menu): El objeto menu de pygame_menu
        screen: La pantalla de pygame
        complete_path (str): La ruta absoluta hasta el directorio app
    """
    for attribute in AJUSTES.__dict__:
        setattr(AJUSTES, attribute, getattr(AJUSTES_DEFAULT, attribute))
    save(AJUSTES, AJUSTES_DEFAULT, menu, screen, complete_path)
    draw_menu(menu, screen, AJUSTES, AJUSTES_DEFAULT, complete_path)


def draw_menu(menu, screen, AJUSTES:Ajustes, AJUSTES_DEFAULT:Ajustes, complete_path:str):
    """
    Dibuja todas las opciones de los ajustes en la pantalla

    Args:
        menu (pygame_menu.Menu): El objeto menu de pygame_menu
        screen: La pantalla de pygame
        AJUSTES (Ajustes): El objeto de los ajustes
        AJUSTES_DEFAULT (Ajustes): El objeto de los ajustes con los valores predeterminados
        complete_path (str): La ruta absoluta hasta el directorio app
    """
    menu.clear()
    menu.add.range_slider("Porcentaje para detectar una nota: "+str(AJUSTES.PORCENTAJE_DETECTAR_NOTA), default=AJUSTES.PORCENTAJE_DETECTAR_NOTA,
                            range_values=(0, 1), increment=0.05, onchange = lambda value: set_ajustes(value, "porcentaje_detectar_nota", AJUSTES))
    menu.add.range_slider("Porcentaje para diferenciar negras de blancas: "+str(AJUSTES.PORCENTAJE_DIFERENCIAR_NEGRA_BLANCA), default=AJUSTES.PORCENTAJE_DIFERENCIAR_NEGRA_BLANCA,
                            range_values=(0, 1), increment=0.05, onchange = lambda value: set_ajustes(value, "porcentaje_diferenciar_negra_blanca", AJUSTES))
    menu.add.range_slider("Umbral negro: "+str(AJUSTES.UMBRAL_NEGRO), default=AJUSTES.UMBRAL_NEGRO,
                            range_values=(0, 255), increment=1, onchange=lambda value: set_ajustes(value, "umbral_negro", AJUSTES))
    menu.add.range_slider("Fracción mínima pixeles negros: "+str(AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS) + " ",
                            default=AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS, range_values=(0, 1), increment=0.05, onchange=lambda value: set_ajustes(value, "fraccion_minima_pixeles_negros", AJUSTES))
    menu.add.selector('Detectar corcheas :'+str(AJUSTES.DETECTAR_CORCHEAS),
                        [('No', False), ('Sí', True)], default=AJUSTES.DETECTAR_CORCHEAS, onchange=lambda value, boolean: set_ajustes(boolean,"detectar_corcheas", AJUSTES))
    menu.add.selector('Cambiar tamaño partitura :'+str(AJUSTES.CAMBIAR_SIZE),
                        [('No', False), ('Sí', True)], default=AJUSTES.CAMBIAR_SIZE, onchange=lambda value, boolean: set_ajustes(boolean, "cambiar_size", AJUSTES))
    menu.add.range_slider("Tempo partitura: "+str(AJUSTES.TEMPO_PARTITURA), default=AJUSTES.TEMPO_PARTITURA,
                            range_values=(40, 255), increment=1, onchange=lambda value: set_ajustes(value, "tempo_partitura", AJUSTES))
    menu.add.button("Default settings", lambda: return_to_default_settings(
        AJUSTES, AJUSTES_DEFAULT, menu, screen, complete_path))
    
    menu.add.button('Save', lambda: save(
        AJUSTES, AJUSTES_DEFAULT, menu, screen, complete_path))

    menu.add.button('Return', lambda: quit(menu))



def main_ajustes() -> bool:
    """
    La lógica del menú de ajustes
    """
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
