import pygame
import pygame_funcs.Buttons.Button as b
from pygame_funcs.main_pygame import main_pygame
from lectura_partituras.main_lectura_partituras import main_lectura_partituras
from pygame_funcs.ajustes import main_ajustes
from musica.musica import main_musica

from Classes.Errors import ImageNotSelected, ErrorPentagramas, ErrorPath


def main_menu():
    pygame.init()
    COLORS = {"GRAY":(150, 150, 150), "RED":(255, 0, 0), "BG": (20,20,20)}

    running = True
    w = 760
    h = 760
    screen = pygame.display.set_mode((w, h))

    buttons_width: int = 400
    
    x:int = w // 2 - buttons_width//2
    font = pygame.font.SysFont('Arxºial', 40)

    clock = pygame.time.Clock()


    while running:
        pygame.display.set_caption("Menú Lectura Partituras")
        time_delta = clock.tick(60)/1000.0

        button_lectura = b.Button(x, 30, buttons_width, 100, 'LEER PARTITURA', font, main_lectura_partituras)
        button_edit = b.Button(x, 140, buttons_width, 100, "EDITAR PARTITURA", font, main_pygame)
        button_music = b.Button(x, 250, buttons_width, 100, "TOCAR MÚSICA", font, main_musica)
        button_options = b.Button(x, 360, buttons_width, 100, 'AJUSTES', font, main_ajustes)
        button_instructions = b.Button(x, 470, buttons_width, 100, 'INSTRUCCIONES', font, lambda: True)
        button_quit = b.Button(x, 580, buttons_width, 100, 'QUIT', font, lambda: False)

        buttons = [button_options, button_lectura, button_music, button_edit, button_instructions, button_quit]


        screen = pygame.display.set_mode((w, h))
        screen.fill(COLORS["BG"])
        
        for button in buttons:
            try:
                running = button.process(screen)
            except ImageNotSelected as e:
                print(e)
            except pygame.error as e:
                print(e)
            except ErrorPentagramas as e:
                print(e)
                running = True
            except FileNotFoundError as e:
                print(e)
            except ErrorPath as e:
                print(e)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()

    pygame.quit()
