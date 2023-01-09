import pygame
import pygame_menu
from Classes.Ajustes import Ajustes
import pickle
import numpy as np
from lectura_partituras.functions.functions import find_complete_path

def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def set_umbral(value, AJUSTES, menu, screen):
    AJUSTES.UMBRAL_NEGRO = int(value)



def set_fraccion(value, AJUSTES):
    AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS = np.round(value, 3)


def save(AJUSTES, AJUSTES_DEFAULT, menu, screen, complete_path):
    # Do the job here !

    with open(complete_path + "app/ajustes/ajustes.obj", "wb") as fh:
        pickle.dump(AJUSTES, fh)

    draw_menu(menu, screen, AJUSTES, AJUSTES_DEFAULT, complete_path)

def quit(menu):
    menu.disable()

def return_to_default_settings(AJUSTES, AJUSTES_DEFAULT, menu, screen, complete_path):
    for attribute in AJUSTES.__dict__:
        setattr(AJUSTES, attribute, getattr(AJUSTES_DEFAULT, attribute))
    draw_menu(menu, screen, AJUSTES, AJUSTES_DEFAULT, complete_path)
    

def draw_menu(menu, screen, AJUSTES, AJUSTES_DEFAULT, complete_path):
    menu.clear()
    menu.add.range_slider("Umbral negro: "+str(AJUSTES.UMBRAL_NEGRO), default=AJUSTES.UMBRAL_NEGRO, range_values=(0, 255), increment=1, onchange = lambda value:set_umbral(value, AJUSTES, menu, screen))
    menu.add.range_slider("Fracción mínima pixeles negros: "+str(AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS), default=AJUSTES.FRACCION_MINIMA_PIXELES_NEGROS, range_values=(0, 1), increment=0.1, onchange = lambda value:set_fraccion(value, AJUSTES))
    menu.add.selector('Detectar corcheas :', [('Sí', 1), ('No', 2)], onchange=set_difficulty)
    menu.add.button("Default settings", lambda: return_to_default_settings(AJUSTES, AJUSTES_DEFAULT, menu, screen, complete_path))
    menu.add.button('Save', lambda: save(AJUSTES, AJUSTES_DEFAULT, menu, screen, complete_path))
    menu.add.button('Quit', lambda: quit(menu))

def main_ajustes():
    # pygame.init()
    complete_path = find_complete_path()
    
    COLORS = {"GRAY": (150, 150, 150), "RED": (255, 0, 0), "BG": (20, 20, 20)}

    w = 760
    h = 760
    screen = pygame.display.set_mode((w, h))
    
    AJUSTES_DEFAULT = Ajustes()
    try:
        with open(complete_path + "app/ajustes/ajustes.obj", "rb") as fh:
            AJUSTES = pickle.load(fh)
    except FileNotFoundError:
        AJUSTES = AJUSTES_DEFAULT

        
    menu = pygame_menu.Menu('Welcome', w, h,
                        theme=pygame_menu.themes.THEME_DARK)

    # menu.add.text_input('Name :', default=str(AJUSTES))
    draw_menu(menu, screen, AJUSTES, AJUSTES_DEFAULT, complete_path)

    menu.mainloop(screen)
    
    

    return True