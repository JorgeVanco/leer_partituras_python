import pygame
import pygame_funcs.Buttons.Button as b
from pygame_funcs.main_pygame import main_pygame
from lectura_partituras.main_lectura_partituras import main_lectura_partituras
from pygame_funcs.ajustes import main_ajustes
from musica.musica import main_musica
from lectura_partituras.functions.functions import find_complete_path

from Classes.Errors import ImageNotSelected, ErrorPentagramas, ErrorPath


def main_menu():
    pygame.init()

    complete_path = find_complete_path(__file__)
    bg = pygame.image.load(complete_path + "app/pygame_funcs/imagenes_menu/escenario.png")

    running = True
    w = 1024
    h = 768
    screen = pygame.display.set_mode((w, h))

    buttons_width: int = 400
    
    x:int = w // 2 - buttons_width//2
    height:int = 100
    font = pygame.font.SysFont('microsoftjhengheimicrosoftjhengheiuibold', 40)

    clock = pygame.time.Clock()


    while running:
        pygame.display.set_caption("Menú Lectura Partituras")
        clock.tick(60)/1000.0

        button_lectura = b.Button(x, 50, buttons_width, height, 'LEER PARTITURA', font, main_lectura_partituras)
        button_edit = b.Button(x, 160, buttons_width, height, "EDITAR PARTITURA", font, main_pygame)
        button_music = b.Button(x, 270, buttons_width, height, "TOCAR MÚSICA", font, main_musica)
        button_options = b.Button(x, 380, buttons_width, height, 'AJUSTES', font, main_ajustes)
        button_instructions = b.Button(x, 490, buttons_width, height, 'INSTRUCCIONES', font, lambda: True)
        button_quit = b.Button(x, 600, buttons_width, height, 'QUIT', font, lambda: False)

        buttons = [button_options, button_lectura, button_music, button_edit, button_instructions, button_quit]


        screen = pygame.display.set_mode((w, h))
        screen.blit(bg, (0, 0))

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
